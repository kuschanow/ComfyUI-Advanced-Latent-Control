from .transform_functions import latent_interpolate_transform


class LatentInterpolateTransform:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "latent": ("LATENT",),
                "offset": ("OFFSET",),
                "start_at": ("FLOAT", {"default": 0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "stop_at": ("FLOAT", {"default": 0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "factor": ("FLOAT", {"default": 0.5, "min": 0, "max": 1, "step": 0.01}),
                "multiplier": ("FLOAT", {"default": 1, "min": -10, "max": 10, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("TRANSFORM",)
    FUNCTION = "process"

    CATEGORY = "sampling/transforms"

    def process(self,
                offset,
                latent,
                start_at=0,
                stop_at=0,
                factor=0.5,
                multiplier=1):
        return ([{
            "params": {
                "latent": latent["samples"][0],
                "start_at": start_at,
                "stop_at": stop_at,
                "factor": factor,
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
            return latent_interpolate_transform(x0, params)
