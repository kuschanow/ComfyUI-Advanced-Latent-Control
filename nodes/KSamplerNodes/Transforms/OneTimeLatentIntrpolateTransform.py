from .utils import latent_interpolate_transform


class OneTimeLatentInterpolateTransform:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "latent": ("LATENT",),
                "step": ("INT", {"default": 1, "min": 1, "max": 10000}),
                "factor": ("FLOAT", {"default": 0.5, "min": 0, "max": 1, "step": 0.01}),
                "multiplier": ("FLOAT", {"default": 1, "min": -10, "max": 10, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("TRANSFORM",)
    FUNCTION = "process"

    CATEGORY = "sampling/transforms"

    def process(self,
                latent,
                step=1,
                factor=0.5,
                multiplier=1):
        return ([{
            "params": {
                "latent": latent["samples"][0],
                "step": step,
                "factor": factor,
                "multiplier": multiplier,
            },
            "function": self.func
        }],)

    def func(self, step, x0, total_steps, params):
        x = x0

        if step + 1 == params["step"]:
            x = latent_interpolate_transform(x0, params)

        return x
