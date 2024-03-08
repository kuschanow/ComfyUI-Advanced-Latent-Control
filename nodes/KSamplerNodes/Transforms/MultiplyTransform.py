from .utils import multiply_transform, get_offset_list


class MultiplyTransform:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "start_at": ("FLOAT", {"default": 0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "stop_at": ("FLOAT", {"default": 0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "mode": (["replace", "combine"], {"default": "combine"}),
                "multiplier": ("FLOAT", {"default": 1, "min": -10, "max": 10, "step": 0.01}),
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
                mode="combine",
                multiplier=1):
        return ([{
            "params": {
                "start_at": start_at,
                "stop_at": stop_at,
                "mode": mode,
                "multiplier": multiplier,
                "offset": offset_optional,
            },
            "function": self.func
        }],)

    def func(self, step, x0, total_steps, params):
        x = x0

        offset_list = get_offset_list(params["offset"], total_steps)

        if total_steps * params["start_at"] <= step + 1 <= total_steps * params["stop_at"] and offset_list[step]:
            x = multiply_transform(x0, params)

        return x
