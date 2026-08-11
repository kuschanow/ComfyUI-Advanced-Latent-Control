function gcd(a, b) {
    // Функция для вычисления наибольшего общего делителя (НОД)
    while (b !== 0) {
        let t = b;
        b = a % b;
        a = t;
    }
    return a;
}

function lcm(a, b) {
    // Функция для вычисления наименьшего общего кратного (НОК)
    return (a * b) / gcd(a, b);
}

function findPatternLength(rules) {
    // Вычисление длины цикла как НОК всех process_every
    return rules.map(rule => rule.process_every).reduce((acc, val) => lcm(acc, val), 1);
}

export function generatePattern(rules) {
    let length = findPatternLength(rules); // Определение длины паттерна
    let pattern = new Array(length).fill(0);

    rules.forEach(rule => {
        let offset = rule.offset % rule.process_every;

        for (let i = 0; i < length; i++) {
			let value = ((i + offset) % rule.process_every === 0) === (rule.mode === "process_every") ? 1 : 0;
			pattern[i] = pattern[i] || value;
        }
    });

    return pattern;
}

export function recursiveLinkUpstream(node, slot_type, node_type, depth) {
	depth += 1
	let connections = []
	const inputList = [...Array(node.inputs.length).keys()]
	for (let i of inputList) {
		const link = node.inputs[i].link
		if (link) {
			const nodeID = node.graph.links[link].origin_id
			const slotID = node.graph.links[link].origin_slot
			const connectedNode = node.graph._nodes_by_id[nodeID]

			if (connectedNode.outputs[slotID].type === slot_type) {

				connections.push([connectedNode.id, depth])

				if (connectedNode.inputs) {
					const index = (connectedNode.type === node_type) ? 0 : null
					connections = connections.concat(recursiveLinkUpstream(connectedNode, slot_type, node_type, depth))
				}
			}
		}
	}

	return connections
}

export function renameNodeInputs(node, name) {
	for (let i=0; i < node.inputs.length; i++) {
		node.inputs[i].name = `${name}${i + 1}`
	}
}

export function removeNodeInputs(node, indexesToRemove) {
	indexesToRemove.sort((a, b) => b - a);

	for (let i of indexesToRemove) {
		if (node.inputs.length <= 2) { console.log("too short"); continue } // if only 2 left
		node.removeInput(i)
	}

	node.setSize(node.computeSize())
	node.graph?.setDirtyCanvas(true, true)
}

const MARGIN_X = 15;         // side padding — matches the node's standard widgets
const MARGIN_Y = 10;         // top/bottom padding around the grid (node-local px)
const MIN_SQUARE = 24;       // smallest square that still shows the row on tiny/long patterns
const MAX_SQUARE = 72;       // largest square, so a short pattern doesn't blow up
const MIN_NODE_WIDTH = 220;  // enough width for the squares to read

// Square side that fits the given (full node) width and column count. Squares
// shrink to fit a long pattern (down to 1px) and are capped so a short one stays
// reasonable. Guarantees squareSize * cols <= width - 2*MARGIN_X, i.e. no overflow.
function fitSquareSize(width, cols) {
	const availWidth = width - MARGIN_X * 2;
	return Math.max(1, Math.min(availWidth / Math.max(cols, 1), MAX_SQUARE));
}

/**
 * Adds a self-contained canvas widget that draws a pattern preview directly onto
 * the LiteGraph node context. Works with the current ComfyUI frontend (Nodes v2):
 * it paints in node-local coordinates, so it scales and positions correctly with
 * zoom and DPI — no DOM overlay and no manual ctx.getTransform() math.
 *
 * The preview auto-sizes to the space available inside the node: computeSize()
 * reports exactly the height the grid needs for the current width and pattern
 * length, so the node reserves the right amount of room, the squares grow/shrink
 * as the node gets wider/narrower or the pattern longer/shorter, and the drawing
 * always stays inside the node body.
 *
 * @param node        the LiteGraph node
 * @param name        widget name
 * @param getPattern  (node) => number[]  the 0/1 pattern to render
 * @param drawSquares (ctx, startX, startY, squareSize, pattern) => void
 */
export function addCustomCanvasWidget(node, name, getPattern, drawSquares) {
	const widget = {
		type: "customCanvas",
		name,
		value: undefined,
		options: { serialize: false },
		computeSize() {
			// Use the real node width, not the passed value: LiteGraph feeds a
			// widened width to selected nodes, which would inflate the reserve.
			const nodeWidth = node.size[0];
			const cols = getPattern(node).length || 1;
			const rowHeight = Math.max(fitSquareSize(nodeWidth, cols), MIN_SQUARE);
			return [nodeWidth, rowHeight + MARGIN_Y * 2];
		},
		draw(ctx, node, width, widgetY) {
			const pattern = getPattern(node);
			if (!pattern || !pattern.length) return;

			// Use node.size[0] rather than the `width` argument: on a selected node
			// LiteGraph passes an enlarged width, which would push the grid right and
			// peg the square size at its cap. node.size[0] is stable in both states.
			const nodeWidth = node.size[0];
			const cols = pattern.length;
			const squareSize = fitSquareSize(nodeWidth, cols);

			// Same band height computeSize reserved -> the grid stays inside the node.
			const bandHeight = Math.max(squareSize, MIN_SQUARE) + MARGIN_Y * 2;
			const gridWidth = squareSize * cols;

			const startX = (nodeWidth - gridWidth) / 2;
			const startY = widgetY + (bandHeight - squareSize) / 2;

			// Light backing drawn first so empty cells stay readable on dark nodes.
			ctx.fillStyle = "#ffffffcc";
			ctx.fillRect(startX, startY, gridWidth, squareSize);

			drawSquares(ctx, startX, startY, squareSize, pattern);
		},
	};

	node.addCustomWidget(widget);

	// Widen a touch and reserve the preview height on creation. On workflow load
	// LiteGraph applies the saved size after onNodeCreated, so this does not fight
	// persisted sizes.
	node.size[0] = Math.max(node.size[0], MIN_NODE_WIDTH);
	node.setSize(node.computeSize());

	return widget;
}


