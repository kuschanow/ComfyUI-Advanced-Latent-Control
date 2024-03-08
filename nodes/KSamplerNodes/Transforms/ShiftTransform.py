from .transform_functions import shift_transform


class ShiftTransform:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "offset": ("OFFSET",),
                "start_at": ("FLOAT", {"default": 0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "stop_at": ("FLOAT", {"default": 0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "mode": (["replace", "combine"], {"default": "replace"}),
                "x_shift": ("FLOAT", {"default": 0, "min": -1, "max": 1, "step": 0.01}),
                "y_shift": ("FLOAT", {"default": 0, "min": -1, "max": 1, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("TRANSFORM",)
    FUNCTION = "process"

    CATEGORY = "sampling/transforms"

    def process(self,
                offset,
                start_at=0,
                stop_at=0,
                mode="replace",
                x_shift=0,
                y_shift=0):
        return ([{
            "params": {
                "start_at": start_at,
                "stop_at": stop_at,
                "mode": mode,
                "x_shift": x_shift,
                "y_shift": y_shift,
            },
            "offset": offset,
            "offset_status": offset["process_every"] - offset["offset"] - 1,
            "function": self.func
        }],)

    def func(self, step, x0, total_steps, params) -> list:
        if (total_steps * params["start_at"] <= step <= total_steps * params["stop_at"] and
           (params["offset_status"] == 0 if params["offset"]["mode"] == "process_every" else params["offset_status"] != 0)):
            return shift_transform(x0, params)
