export function computeCanvasSize(node, size) {
	if (node.widgets[0].last_y == null) return;

	const MIN_SIZE = 64;

	const inputs = node.inputs === undefined ? 0 : node.inputs.length
	const outputs = node.outputs === undefined ? 0 : node.outputs.length

	let y = LiteGraph.NODE_WIDGET_HEIGHT * Math.max(inputs, outputs) + 5;
	let freeSpace = size[1] - y;

	// Compute the height of all non customtext widgets
	let widgetHeight = 0;
	for (let i = 0; i < node.widgets.length; i++) {
		const w = node.widgets[i];
		if (w.type !== "customCanvas") {
			if (w.computeSize) {
				widgetHeight += w.computeSize()[1] + 4;
			} else {
				widgetHeight += LiteGraph.NODE_WIDGET_HEIGHT + 5;
			}
		}
	}

	// See how large the canvas can be
	freeSpace -= widgetHeight;

	// There isnt enough space for all the widgets, increase the size of the node
	if (freeSpace < MIN_SIZE) {
		freeSpace = MIN_SIZE;
		node.size[1] = y + widgetHeight + freeSpace;
		node.graph.setDirtyCanvas(true);
	}

	// Position each of the widgets
	for (const w of node.widgets) {
		w.y = y;
		if (w.type === "customCanvas") {
			y += freeSpace;
		} else if (w.computeSize) {
			y += w.computeSize()[1] + 4;
		} else {
			y += LiteGraph.NODE_WIDGET_HEIGHT + 4;
		}
	}

	node.canvasHeight = freeSpace;
}

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

export function recursiveLinkUpstream(node, type, depth, index=null) {
	depth += 1
	let connections = []
	if (node.type === "OffsetCombine") {
		const inputList = [...Array(node.inputs.length).keys()]
		for (let i of inputList) {
			const link = node.inputs[i].link
			if (link) {
				const nodeID = node.graph.links[link].origin_id
				const slotID = node.graph.links[link].origin_slot
				const connectedNode = node.graph._nodes_by_id[nodeID]

				if (connectedNode.outputs[slotID].type === type) {

					connections.push([connectedNode.id, depth])

					if (connectedNode.inputs) {
						const index = (connectedNode.type === "OffsetCombine") ? 0 : null
						connections = connections.concat(recursiveLinkUpstream(connectedNode, type, depth, index))
					}
				}
			}
		}
	}

	return connections
}
