from .utils import shift_transform, get_offset_list


class ShiftTransform:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "start_at": ("FLOAT", {"default": 0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "stop_at": ("FLOAT", {"default": 0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "mode": (["replace", "combine"], {"default": "replace"}),
                "x_shift": ("FLOAT", {"default": 0, "min": -1, "max": 1, "step": 0.01}),
                "y_shift": ("FLOAT", {"default": 0, "min": -1, "max": 1, "step": 0.01}),
            },
            "optional": {
                "offset_optional": ("OFFSET",),
            }
        }

    RETURN_TYPES = ("TRANSFORM",)
    FUNCTION = "process"

    CATEGORY = "sampling/transforms"

    def process(self,
                offset_optional,
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
                "offset": offset_optional,
            },
            "function": self.func
        }],)

    def func(self, step, x0, total_steps, params):
        x = x0

        offset_list = get_offset_list(params["offset"], total_steps)

        if total_steps * params["start_at"] <= step + 1 <= total_steps * params["stop_at"] and offset_list[step]:
            x = shift_transform(x0, params)

        return x
