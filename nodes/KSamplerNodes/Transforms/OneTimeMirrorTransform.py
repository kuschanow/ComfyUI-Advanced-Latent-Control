from .transform_functions import mirror_transform


DIRECTIONS = ["vertically", "horizontally", "both", "90 degree rotation", "180 degree rotation"]

class OneTimeMirrorTransform:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "step": ("INT", {"default": 1, "min": 1, "max": 10000}),
                "mode": (["replace", "combine"],),
                "direction": (DIRECTIONS, {"default": "horizontally"}),
            }
        }

    RETURN_TYPES = ("TRANSFORM",)
    FUNCTION = "process"

    CATEGORY = "sampling/transforms"

    def process(self,
                step=1,
                mode="replace",
                direction="horizontally",):
        return ([{
                "params": {
                    "step": step,
                    "mode": mode,
                    "direction": direction,
                },
                "function": self.func
            }],)

    def func(self, step, x0, total_steps, params):
        if step == params["step"]:
            return mirror_transform(x0, params)
