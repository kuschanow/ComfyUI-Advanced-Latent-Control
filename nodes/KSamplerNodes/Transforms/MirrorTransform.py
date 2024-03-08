from .transform_functions import mirror_transform


DIRECTIONS = ["vertically", "horizontally", "both", "90 degree rotation", "180 degree rotation"]

class MirrorTransform:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "offset": ("OFFSET",),
                "start_at": ("FLOAT", {"default": 0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "stop_at": ("FLOAT", {"default": 0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "mode": (["replace", "combine"],),
                "direction": (DIRECTIONS, {"default": "horizontally"}),
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
                direction="horizontally",):
        return ([{
            "params": {
                "start_at": start_at,
                "stop_at": stop_at,
                "mode": mode,
                "direction": direction,
            },
            "offset": offset,
            "offset_status": offset["process_every"] - offset["offset"] - 1,
            "function": self.func
        }],)

    def func(self, step, x0, total_steps, params) -> list:
        if (total_steps * params["start_at"] <= step <= total_steps * params["stop_at"] and
           (params["offset_status"] == 0 if params["offset"]["mode"] == "process_every" else params["offset_status"] != 0)):
            return mirror_transform(x0, params)
