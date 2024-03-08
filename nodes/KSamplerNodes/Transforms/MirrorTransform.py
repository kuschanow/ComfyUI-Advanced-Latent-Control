from .utils import mirror_transform, get_offset_list


DIRECTIONS = ["vertically", "horizontally", "both", "90 degree rotation", "180 degree rotation"]

class MirrorTransform:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "start_at": ("FLOAT", {"default": 0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "stop_at": ("FLOAT", {"default": 0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "mode": (["replace", "combine"],),
                "direction": (DIRECTIONS, {"default": "horizontally"}),
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
                direction="horizontally",):
        return ([{
            "params": {
                "start_at": start_at,
                "stop_at": stop_at,
                "mode": mode,
                "direction": direction,
                "offset": offset_optional,
            },
            "function": self.func
        }],)

    def func(self, step, x0, total_steps, params):
        x = x0

        offset_list = get_offset_list(params["offset"], total_steps)

        if total_steps * params["start_at"] <= step+1 <= total_steps * params["stop_at"] and offset_list[step]:
            x = mirror_transform(x0, params)

        return x
