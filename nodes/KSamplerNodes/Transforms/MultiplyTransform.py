from .transform_functions import multiply_transform


class MultiplyTransform:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "offset": ("OFFSET",),
                "start_at": ("FLOAT", {"default": 0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "stop_at": ("FLOAT", {"default": 0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "mode": (["replace", "combine"], {"default": "combine"}),
                "multiplier": ("FLOAT", {"default": 1, "min": -10, "max": 10, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("TRANSFORM",)
    FUNCTION = "process"

    CATEGORY = "sampling/transforms"

    def process(self,
                offset,
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
                "offset": offset,
                "offset_status": offset["process_every"] - offset["offset"] - 1,
            },
            "function": self.func
        }],)

    def func(self, step, x0, total_steps, params):
        if (total_steps * params["start_at"] <= step <= total_steps * params["stop_at"] and
           (params["offset_status"] == 0 if params["offset"]["mode"] == "process_every" else params["offset_status"] != 0)):
            if params["offset_status"] == 0:
                params["offset_status"] = params["offset"]["process_every"] - 1
            else:
                params["offset_status"] -= 1
            return multiply_transform(x0, params)
