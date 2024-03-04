import torch


class MultiplyTransform:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "start_multiplier_at": ("FLOAT", {"default": 0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "stop_multiplier_at": ("FLOAT", {"default": 0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "multiplier_mode": (["replace", "combine"], {"default": "combine"}),
                "multiplier": ("FLOAT", {"default": 1, "min": -10, "max": 10, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("TRANSFORM",)
    FUNCTION = "process"

    CATEGORY = "sampling/transforms"

    def process(self,
                start_at=0,
                stop_at=0,
                mode="combine",
                multiplier=1):
        return ([{
                "params": {
                    "start_at": start_at,
                    "stop_at": stop_at,
                    "mode": mode,
                    "multiplier": multiplier,
                },
                "function": self.func
            }],)

    def func(self, step, x0, total_steps, params) -> list:
        x = x0

        if total_steps * params["start_at"] <= step <= total_steps * params["stop_at"]:
            if params["mode"] == "replace":
                x *= params["multiplier"]
            elif params["mode"] == "combine":
                x = (x * params["multiplier"] + x) / 2

        return x
