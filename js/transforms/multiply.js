import { app } from "/scripts/app.js";
import {addCanvas, computeCanvasSize} from "../utils.js";

const multiplyWidget = {
	type: "customCanvas",
	name: "Multiply-Canvas",
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

		const visible = true
		const t = ctx.getTransform();
		const margin = 10

		const widgetHeight = node.canvasHeight
		const width = 32
		const height = 32

		const scale = Math.min((widgetWidth - margin * 2) / width, (widgetHeight - margin * 2) / height)

		Object.assign(this.canvas.style, {
			left: `${t.e}px`,
			top: `${t.f + (widgetY * t.d)}px`,
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
			xOffset += (widgetWidth - backgroundWidth) / 2 - margin
		}
		let yOffset = margin
		if (backgroundHeight < widgetHeight) {
			yOffset += (widgetHeight - backgroundHeight) / 2 - margin
		}

		let widgetX = xOffset
		widgetY = widgetY + yOffset

		const multiplayer = node.widgets[3].value
		const operationType = node.widgets[2].value

		const widgetMargin = 10

		const x = widgetX + widgetMargin
		const y = widgetY + widgetMargin

		function drawFractionAndMultiply(x, y) {
			ctx.font = `${Math.min(backgroundWidth, backgroundHeight)/4}px Consolas`;
			ctx.fillStyle = "#2383ef"
			ctx.fillText(`${multiplayer.toFixed(2)} ×`, x, y);
		}

		function drawReplaceShape(x, y) {

		}

		function drawCombineShape(x, y) {

		}

		drawFractionAndMultiply(x, y);
		if (operationType === 'replace') {
			drawReplaceShape(x, y);
		} else {
			drawCombineShape(x, y);
		}
	},
};


app.registerExtension({
    name: "Comfy.LatentControl.Transform.Multiply",
    async beforeRegisterNodeDef (nodeType, nodeData, app){
        if (nodeData.name === "MultiplyTransform") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;

                addCanvas(this, app, multiplyWidget)

				return r;
			}
        }
    },
});
