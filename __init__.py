from .nodes import *

NODE_CLASS_MAPPINGS = {
    "LatentMirror": LatentMirror,
    "LatentShift": LatentShift,
    "KSamplerMirroring": KSamplerMirroring,
    "KSamplerMirroringApart": KSamplerMirroringApart,
    "MirrorTransform": MirrorTransform,
    "ShiftTransform": ShiftTransform,
    "MultiplyTransform": MultiplyTransform,
    "OneTimeMirrorTransform": OneTimeMirrorTransform,
    "OneTimeMultiplyTransform": OneTimeMultiplyTransform,
    "OneTimeShiftTransform": OneTimeShiftTransform,
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
    "OneTimeMirrorTransform": "Mirror transform (one time)",
    "OneTimeMultiplyTransform": "Shift transform (one time)",
    "OneTimeShiftTransform": "Multiply transform (one time)",
    "TransformsCombine": "Combine transforms",
}

