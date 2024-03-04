from .nodes import LatentMirror, LatentShift, KSamplerMirroring, KSamplerMirroringApart, MirrorTransform, ShiftTransform, MultiplyTransform, TransformsCombine

NODE_CLASS_MAPPINGS = {
    "LatentMirror": LatentMirror,
    "LatentShift": LatentShift,
    "KSamplerMirroring": KSamplerMirroring,
    "KSamplerMirroringApart": KSamplerMirroringApart,
    "MirrorTransform": MirrorTransform,
    "ShiftTransform": ShiftTransform,
    "MultiplyTransform": MultiplyTransform,
    "TransformsCombine": TransformsCombine,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LatentMirror": "Latent mirror",
    "LatentShift": "Latent shift",
    "KSamplerMirroring": "KSampler with transforms (Latent Control)",
    "KSamplerMirroringApart": "KSampler (Latent Control)",
    "MirrorTransform": "Mirror transform",
    "ShiftTransform": "Shift transform",
    "MultiplyTransform": "Multiply transform",
    "TransformsCombine": "Combine transforms",
}
