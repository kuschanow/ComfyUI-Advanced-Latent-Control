from .nodes import *


WEB_DIRECTORY = "js"

NODE_CLASS_MAPPINGS = {
    "LatentMirror": LatentMirror,
    "LatentShift": LatentShift,
    "LatentNormalize": LatentNormalize,
    "TransformSampler": TSampler,
    "TransformSamplerAdvanced": TSamplerAdvanced,
    "TransformHijack": TransformHijack,
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
    "OffsetCombine": OffsetCombine,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LatentMirror": "Latent mirror",
    "LatentShift": "Latent shift",
    "LatentNormalize": "Latent normalize",
    "TransformSampler": "TSampler (Latent Control)",
    "TransformSamplerAdvanced": "TSampler Advanced (Latent Control)",
    "TransformHijack": "Transform Hijack",
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
    "OffsetCombine": "Combine offsets",
}

