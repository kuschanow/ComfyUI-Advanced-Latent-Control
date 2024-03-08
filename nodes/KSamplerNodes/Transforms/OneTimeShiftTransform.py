from .transform_functions import shift_transform


class OneTimeShiftTransform:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "step": ("INT", {"default": 1, "min": 1, "max": 10000}),
                "mode": (["replace", "combine"], {"default": "replace"}),
                "x_shift": ("FLOAT", {"default": 0, "min": -1, "max": 1, "step": 0.01}),
                "y_shift": ("FLOAT", {"default": 0, "min": -1, "max": 1, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("TRANSFORM",)
    FUNCTION = "process"

    CATEGORY = "sampling/transforms"

    def process(self,
                step=1,
                mode="replace",
                x_shift=0,
                y_shift=0):
        return ([{
                "params": {
                    "step": step,
                    "mode": mode,
                    "x_shift": x_shift,
                    "y_shift": y_shift,
                },
                "function": self.func
            }],)

    def func(self, step, x0, total_steps, params):
        if step == params["step"]:
            return shift_transform(x0, params)
