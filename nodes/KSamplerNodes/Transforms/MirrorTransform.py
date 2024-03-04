import torch


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
            }
        }

    RETURN_TYPES = ("TRANSFORM",)
    FUNCTION = "process"

    CATEGORY = "sampling/transforms"

    def process(self,
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
                "function": self.func
            }],)

    def func(self, step, x0, total_steps, params) -> list:
        x = x0

        if total_steps * params["start_at"] <= step <= total_steps * params["stop_at"]:
            if params["mode"] == "replace":
                if params["direction"] == "vertically":
                    x = torch.flip(x, [1])
                elif params["direction"] == "horizontally":
                    x = torch.flip(x, [2])
                elif params["direction"] == "both":
                    x = torch.flip(x, [1, 2])
                elif params["direction"] == "90 degree rotation":
                    x = torch.rot90(x, dims=[1, 2])
                elif params["direction"] == "180 degree rotation":
                    x = torch.rot90(torch.rot90(x, dims=[1, 2]), dims=[1, 2])
            elif params["mode"] == "combine":
                if params["direction"] == "vertically":
                    x = (torch.flip(x, [1]) + x) / 2
                elif params["direction"] == "horizontally":
                    x = (torch.flip(x, [2]) + x) / 2
                elif params["direction"] == "both":
                    x = (torch.flip(x, [1, 2]) + x) / 2
                elif params["direction"] == "90 degree rotation":
                    x = (torch.rot90(x, dims=[1, 2]) + x) / 2
                elif params["direction"] == "180 degree rotation":
                    x = (torch.rot90(torch.rot90(x, dims=[1, 2]), dims=[1, 2]) + x) / 2

        return x
