import torch
from nodes import PreviewImage

class LatentNormalize:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "latent": ("LATENT",),
                "vae": ("VAE",)
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "normalize"

    CATEGORY = "latent/advanced"

    def normalize(self, latent, vae):
        image = vae.decode(latent["samples"])
        sample = vae.encode(image[:,:,:,:3])
        return {"result": ({"samples": sample},), "ui": PreviewImage().save_images(image)["ui"]}
