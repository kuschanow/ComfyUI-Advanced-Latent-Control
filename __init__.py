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
    "LatentMirror": "LatentMirror",
    "LatentShift": "LatentShift",
    "KSamplerMirroring": "KSampler (Latent Control)",
    "KSamplerMirroringApart": "KSampler with apart transforms (Latent Control)",
    "MirrorTransform": "Mirror Transform",
    "ShiftTransform": "Shift Transform",
    "MultiplyTransform": "Multiply Transform",
    "TransformsCombine": "Combine Transforms",
}
