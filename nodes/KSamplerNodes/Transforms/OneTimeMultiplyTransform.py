from .utils import multiply_transform


class OneTimeMultiplyTransform:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "step": ("INT", {"default": 1, "min": 1, "max": 10000}),
                "mode": (["replace", "combine"], {"default": "combine"}),
                "multiplier": ("FLOAT", {"default": 1, "min": -10, "max": 10, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("TRANSFORM",)
    FUNCTION = "process"

    CATEGORY = "sampling/transforms"

    def process(self,
                step=1,
                mode="combine",
                multiplier=1):
        return ([{
                "params": {
                    "step": step,
                    "mode": mode,
                    "multiplier": multiplier,
                },
                "function": self.func
            }],)

    def func(self, step, x0, total_steps, params):
        x = x0

        if step + 1 == params["step"]:
            x = multiply_transform(x0, params)

        return x
