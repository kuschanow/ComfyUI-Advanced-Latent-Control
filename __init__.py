from .nodes import *

NODE_CLASS_MAPPINGS = {
    "LatentMirror": LatentMirror,
    "LatentShift": LatentShift,
    "KSamplerMirroring": KSamplerMirroring,
    "KSamplerMirroringApart": KSamplerMirroringApart,
    "MirrorTransform": MirrorTransform,
    "ShiftTransform": ShiftTransform,
    "MultiplyTransform": MultiplyTransform,
    "LatentInterpolateTransform": LatentInterpolateTransform,
    "LatentAddTransform": LatentAddTransform,
    "OneTimeMirrorTransform": OneTimeMirrorTransform,
    "OneTimeMultiplyTransform": OneTimeMultiplyTransform,
    "OneTimeShiftTransform": OneTimeShiftTransform,
    "OneTimeLatentInterpolateTransform": OneTimeLatentInterpolateTransform,
    "OneTimeLatentAddTransform": OneTimeLatentAddTransform,
    "TransformsCombine": TransformsCombine,
    "TransformOffset": TransformOffset,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LatentMirror": "Latent mirror",
    "LatentShift": "Latent shift",
    "KSamplerMirroring": "KSampler with transforms (Latent Control)",
    "KSamplerMirroringApart": "KSampler (Latent Control)",
    "MirrorTransform": "Mirror transform",
    "ShiftTransform": "Shift transform",
    "MultiplyTransform": "Multiply transform",
    "LatentInterpolateTransform": "Latent interpolate transform",
    "LatentAddTransform": "Latent add transform",
    "OneTimeMirrorTransform": "Mirror transform (one time)",
    "OneTimeMultiplyTransform": "Shift transform (one time)",
    "OneTimeShiftTransform": "Multiply transform (one time)",
    "OneTimeLatentInterpolateTransform": "Latent interpolate transform (one time)",
    "OneTimeLatentAddTransform": "Latent add transform (one time)",
    "TransformsCombine": "Combine transforms",
    "TransformOffset": "Transform offset",
}

