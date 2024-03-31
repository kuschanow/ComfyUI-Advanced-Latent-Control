import { app } from "/scripts/app.js";
import {computeCanvasSize, generatePattern, recursiveLinkUpstream} from "./utils.js";

function drawSquares(ctx, widgetX, widgetY, squareSize, pattern) {
	pattern.forEach((value, index) => {
		const x = widgetX + index * squareSize; // координата x для квадратика

		// Устанавливаем цвет заливки и обводки
		ctx.fillStyle = value === 1 ? "#222223" : "#00000000";
		ctx.strokeStyle = "#222223"; // Цвет обводки для всех квадратиков
		ctx.lineWidth = Math.floor(squareSize / 16);

		if (value === 1) {
			// Если значение 1, закрашиваем квадрат
			ctx.fillRect(x, widgetY, squareSize, squareSize);
		}

		// Рисуем обводку для всех квадратиков
		ctx.strokeRect(x, widgetY, squareSize, squareSize);

		// Добавляем текст в квадратик
		if (squareSize >= 24) {
			ctx.font = `bold ${squareSize/3}px Arial`; // Размер шрифта адаптируем под размер квадратика
			ctx.textAlign = "center";
			ctx.textBaseline = "middle";
			ctx.text
			ctx.fillStyle = value === 1 ? "#dbdbdc" : "#222223"; // Цвет текста, чтобы он контрастировал с фоном квадратика
			ctx.fillText(value.toString(), x + squareSize/2, widgetY + squareSize/2); // Позиционируем текст по центру квадратика
		}
	});
}

function addOffsetCanvas(node, app) {
	const widget = {
		type: "customCanvas",
		name: "Offset-Canvas",
		get value() {
			return this.canvas.value;
		},
		set value(x) {
			this.canvas.value = x;
		},
		draw: function (ctx, node, widgetWidth, widgetY) {
			if (!node.canvasHeight) {
				computeCanvasSize(node, node.size)
			}

			let patterns = []

			if (node.type === "OffsetCombine") {
				const inputList = [...Array(node.inputs.length).keys()]
				for (let i of inputList) {
					const connectedNodes = recursiveLinkUpstream(node, node.inputs[i].type, 0, i)
					if (connectedNodes.length !== 0) {
						for (let [node_ID, depth] of connectedNodes) {
							const connectedNode = node.graph._nodes_by_id[node_ID]
							if (connectedNode.type !== "OffsetCombine") {
								const pattern = {
									process_every: connectedNode.widgets[0].value,
									offset: connectedNode.widgets[1].value,
									mode: connectedNode.widgets[2].value
								}
								patterns.push(pattern)
							}
						}
					}
				}
			} else {
				const pattern = {
					process_every: node.widgets[0].value,
					offset: node.widgets[1].value,
					mode: node.widgets[2].value}
				patterns.push(pattern)
			}

			const pattern = generatePattern(patterns)

			const visible = true
			const t = ctx.getTransform();
			const margin = 10

			const widgetHeight = node.canvasHeight
			const width = pattern.length * 32
			const height = 32

			const scale = Math.min((widgetWidth-margin*2)/width, (widgetHeight-margin*2)/height)

			Object.assign(this.canvas.style, {
				left: `${t.e}px`,
				top: `${t.f + (widgetY*t.d)}px`,
				width: `${widgetWidth * t.a}px`,
				height: `${widgetHeight * t.d}px`,
				position: "absolute",
				zIndex: 1,
				fontSize: `${t.d * 10.0}px`,
				pointerEvents: "none",
			});

			this.canvas.hidden = !visible;

            let backgroundWidth = width * scale
            let backgroundHeight = height * scale

			let xOffset = margin
			if (backgroundWidth < widgetWidth) {
				xOffset += (widgetWidth-backgroundWidth)/2 - margin
			}
			let yOffset = margin
			if (backgroundHeight < widgetHeight) {
				yOffset += (widgetHeight-backgroundHeight)/2 - margin
			}

			let widgetX = xOffset
			widgetY = widgetY + yOffset

            // Вычисляем размер квадратика, основываясь на ширине канваса и количестве элементов в списке
            const squareSize = backgroundWidth / pattern.length;

            // Рисуем квадратики
			drawSquares(ctx, widgetX, widgetY, squareSize, pattern)
		},
	};

	widget.canvas = document.createElement("canvas");
	widget.canvas.className = "latent-control-custom-canvas";

	widget.parent = node;
	document.body.appendChild(widget.canvas);

	node.addCustomWidget(widget);

	app.canvas.onDrawBackground = function () {
		for (let n in app.graph._nodes) {
			n = graph._nodes[n];
			for (let w in n.widgets) {
				let wid = n.widgets[w];
				if (Object.hasOwn(wid, "canvas")) {
					wid.canvas.style.left = -8000 + "px";
					wid.canvas.style.position = "absolute";
				}
			}
		}
	};

	node.onResize = function (size) {
		computeCanvasSize(node, size);
	}

	return { minWidth: 200, minHeight: 200, widget }
}

app.registerExtension({
    name: "Comfy.LatentControl.TransformOffset",
    async beforeRegisterNodeDef (nodeType, nodeData, app){
        if (nodeData.name === "TransformOffset") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;

                addOffsetCanvas(this, app)

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

                addOffsetCanvas(this, app)

				return r;
			}
        }
    },
});

