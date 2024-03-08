from .transform_functions import latent_add_transform


class OneTimeLatentAddTransform:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "latent": ("LATENT",),
                "step": ("INT", {"default": 1, "min": 1, "max": 10000}),
                "multiplier": ("FLOAT", {"default": 1, "min": -10, "max": 10, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("TRANSFORM",)
    FUNCTION = "process"

    CATEGORY = "sampling/transforms"

    def process(self,
                latent,
                step=1,
                multiplier=1):
        return ([{
            "params": {
                "latent": latent["samples"][0],
                "step": step,
                "multiplier": multiplier,
            },
            "function": self.func
        }],)

    def func(self, step, x0, total_steps, params):
        if step == params["step"]:
            return latent_add_transform(x0, params)
