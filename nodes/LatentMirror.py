import torch
from nodes import PreviewImage

MIRROR_DIRECTIONS = ["vertically", "horizontally", "both"]

class LatentMirror:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": { 
                "latent": ("LATENT",),
                "direction": (MIRROR_DIRECTIONS,),
                "multiplier": ("FLOAT",{
                    "default": 1.0,
                    "min": -10.0,
                    "max": 10.0,
                    "step": 0.01
                })
            },
            "optional": {
                "vae_optional": ("VAE",)
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "mirror"

    CATEGORY = "latent/advanced"

    def mirror(self, latent, direction, multiplier, vae_optional = None):
        l = latent.copy()
        if direction == "vertically" or direction == "both":
            l["samples"] = torch.flip(l["samples"], dims=[2]) + l["samples"]
        if direction == "horizontally" or direction == "both":
            l["samples"] = torch.flip(l["samples"], dims=[3]) + l["samples"]

        l["samples"] *= multiplier

        if vae_optional:
            return {"result": (l,), "ui": PreviewImage().save_images(vae_optional.decode(l["samples"]))["ui"]}

        return (l,)
