import { app } from "/scripts/app.js";
import {addCustomCanvasWidget, generatePattern, recursiveLinkUpstream, renameNodeInputs, removeNodeInputs} from "./utils.js";

function drawSquares(ctx, startX, startY, squareSize, pattern) {
	const inset = Math.max(1, Math.floor(squareSize / 16));
	const cell = squareSize - inset;

	pattern.forEach((value, index) => {
		const x = startX + index * squareSize + inset / 2;
		const y = startY + inset / 2;

		ctx.lineWidth = inset;
		ctx.strokeStyle = "#222223";

		if (value === 1) {
			ctx.fillStyle = "#222223";
			ctx.fillRect(x, y, cell, cell);
		}

		ctx.strokeRect(x, y, cell, cell);

		if (squareSize >= 24) {
			ctx.font = `bold ${squareSize / 3}px Arial`;
			ctx.textAlign = "center";
			ctx.textBaseline = "middle";
			ctx.fillStyle = value === 1 ? "#dbdbdc" : "#222223";
			ctx.fillText(value.toString(), x + cell / 2, y + cell / 2);
		}
	});
}

// Builds the 0/1 preview pattern from the node's own widgets, or (for
// OffsetCombine) from every upstream offset node feeding into it.
function getOffsetPattern(node) {
	let patterns = []

	if (node.type === "OffsetCombine") {
		const connectedNodes = recursiveLinkUpstream(node, node.inputs[0].type, node.type, 0)
		for (let [node_ID] of connectedNodes) {
			const connectedNode = node.graph._nodes_by_id[node_ID]
			if (connectedNode && connectedNode.type !== "OffsetCombine") {
				patterns.push({
					process_every: connectedNode.widgets[0].value,
					offset: connectedNode.widgets[1].value + node.widgets[0].value,
					mode: connectedNode.widgets[2].value,
				})
			}
		}
	} else {
		patterns.push({
			process_every: node.widgets[0].value,
			offset: node.widgets[1].value,
			mode: node.widgets[2].value,
		})
	}

	if (patterns.length === 0) return []

	return generatePattern(patterns)
}

app.registerExtension({
    name: "Comfy.LatentControl.TransformOffset",
    async beforeRegisterNodeDef (nodeType, nodeData, app){
        if (nodeData.name === "TransformOffset") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;

                addCustomCanvasWidget(this, "Offset-Canvas", getOffsetPattern, drawSquares)

				return r;
			}
        }
    },
});

app.registerExtension({
    name: "Comfy.LatentControl.OffsetCombine",
    async beforeRegisterNodeDef (nodeType, nodeData, app){
        if (nodeData.name === "OffsetCombine") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;

                addCustomCanvasWidget(this, "Offset-Canvas", getOffsetPattern, drawSquares)

				this.getExtraMenuOptions = function(_, options) {
					options.unshift(
						{
							content: `add offset`,
							callback: () => {
								this.addInput("offset", "OFFSET")

								renameNodeInputs(this, "offset")

								this.setDirtyCanvas(true);
							},
						},
						{
							content: `remove offset`,
							callback: () => {
								removeNodeInputs(this, [this.inputs.length-1])
								renameNodeInputs(this, "offset")
							},
						},
						{
							content: "remove all unconnected offsets",
							callback: () => {
								let indexesToRemove = []

								for (let i = 0; i < this.inputs.length; i++) {
									if (!this.inputs[i].link) {
										indexesToRemove.push(i)
									}
								}

								if (indexesToRemove.length) {
									removeNodeInputs(this, indexesToRemove)
								}
								renameNodeInputs(this, "offset")
							},
						},
					);
				}

				return r;
			}
        }
    },
});

