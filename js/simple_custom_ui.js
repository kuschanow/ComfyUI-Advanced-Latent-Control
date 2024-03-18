import { app } from "/scripts/app.js";
import { $el } from "/scripts/ui.js";

function get_position_style(ctx, widget_width, y, node_height) {
    const MARGIN = 4;

    const elRect = ctx.canvas.getBoundingClientRect();
    const transform = new DOMMatrix()
        .scaleSelf(elRect.width / ctx.canvas.width, elRect.height / ctx.canvas.height)
        .multiplySelf(ctx.getTransform())
        .translateSelf(MARGIN, MARGIN + y);

    return {
        transformOrigin: '0 0',
        transform: transform,
        left: `0px`,
        top: `0px`,
        position: "absolute",
        maxWidth: `${widget_width - MARGIN*2}px`,
        maxHeight: `${node_height - MARGIN*2}px`,
        width: `auto`,
        height: `auto`,
    }
}

app.registerExtension({
    name: "Comfy.LatentControl.test",
    async beforeRegisterNodeDef (nodeType, nodeData, app){
        if (nodeData.name === "UITestNode") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                onNodeCreated?.apply(this, arguments);

                const widget = {
                    type: "HTML",
                    name: "flying",
                    draw(ctx, node, widget_width, y, widget_height) {
                        Object.assign(this.inputEl.style, get_position_style(ctx, widget_width, y, node.size[1])); // assign the required style when we are drawn
                    },
                };

                widget.inputEl = $el("p", "Hello World");
                document.body.appendChild(widget.inputEl);

                this.addCustomWidget(widget);
                this.onRemoved = function () { widget.inputEl.remove(); };
                this.serialize_widgets = false;
            }
        }
    },
});

