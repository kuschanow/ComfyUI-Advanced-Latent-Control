from .utils import latent_add_transform, get_offset_list
import comfy
import torch


class LatentAddTransform:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "latent": ("LATENT",),
                "start_at": ("FLOAT", {"default": 0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "stop_at": ("FLOAT", {"default": 0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "multiplier": ("FLOAT", {"default": 1, "min": -10, "max": 10, "step": 0.01}),
            },
            "optional":{
                "offset_optional": ("OFFSET",),
            }
        }

    RETURN_TYPES = ("TRANSFORM",)
    FUNCTION = "process"

    CATEGORY = "sampling/transforms"

    def process(self,
                latent,
                start_at=0,
                stop_at=0,
                multiplier=1,
                offset_optional=None):
        return ([{
            "params": {
                "latent": latent["samples"][0].unsqueeze(0),
                "start_at": start_at,
                "stop_at": stop_at,
                "multiplier": multiplier,
                "offset": offset_optional,
            },
            "function": self.func
        }],)

    def func(self, step, x0, total_steps, params):
        x = x0

        offset_list = get_offset_list(params["offset"], total_steps)

        if total_steps * params["start_at"] <= step+1 <= total_steps * params["stop_at"] and offset_list[step]:
            x = latent_add_transform(x0, params)

        return x
