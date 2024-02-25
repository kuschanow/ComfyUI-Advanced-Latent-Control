from .nodes import LatentMirror, LatentShift, KSamplerMirroring

NODE_CLASS_MAPPINGS = {
    "LatentMirror": LatentMirror,
    "LatentShift": LatentShift,
    "KSamplerMirroring": KSamplerMirroring,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LatentMirror": "LatentMirror",
    "LatentShift": "LatentShift",
    "KSamplerMirroring": "KSampler (Latent Control)"
}
