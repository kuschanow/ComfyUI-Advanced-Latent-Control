import torch


class LatentShift:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required":{
                "latent": ("LATENT",),
                "x_shift": ("FLOAT",{
                    "default": 0,
                    "min": -1,
                    "max": 1,
                    "step": 0.01
                }),
                "y_shift": ("FLOAT", {
                    "default": 0,
                    "min": -1,
                    "max": 1,
                    "step": 0.01
                }),
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "shift"

    CATEGORY = "latent/advanced"

    def shift(self, latent, x_shift, y_shift):
        l = latent.copy()

        if x_shift != 0:
            l["samples"] = torch.roll(l["samples"], shifts=int(l["samples"].size()[3] * x_shift), dims=[3])
        if y_shift != 0:
            l["samples"] = torch.roll(l["samples"], shifts=int(l["samples"].size()[2] * y_shift), dims=[2])

        return (l,)
