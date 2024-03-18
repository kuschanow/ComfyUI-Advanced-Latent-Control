import os
import filecmp
import shutil

import __main__

from_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "js")

to_folder = os.path.join(
    os.path.dirname(os.path.realpath(__main__.__file__)),
    "web" + os.sep + "extensions" + os.sep + "Latent_Control")

if not os.path.exists(to_folder):
    print('Making the "web\extensions\Latent_Control" folder')
    os.mkdir(to_folder)

result = filecmp.dircmp(from_folder, to_folder)

if result.left_only or result.diff_files:
    print('Update to javascripts files detected')
    file_list = list(result.left_only)
    file_list.extend(x for x in result.diff_files if x not in file_list)

    for file in file_list:
        print(f'Copying {file} to extensions folder')
        src_file = os.path.join(from_folder, file)
        dst_file = os.path.join(to_folder, file)
        if os.path.exists(dst_file):
            os.remove(dst_file)
        #print("disabled")
        shutil.copy(src_file, dst_file)

WEB_DIRECTORY = "js"

from .nodes import *

NODE_CLASS_MAPPINGS = {
    "UITestNode": UITestNode,
    "LatentMirror": LatentMirror,
    "LatentShift": LatentShift,
    "LatentNormalize": LatentNormalize,
    "TSamplerWithTransform": TSamplerWithTransform,
    "TransformSampler": TransformSampler,
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
    "UITestNode": "UITestNode",
    "LatentMirror": "Latent mirror",
    "LatentShift": "Latent shift",
    "LatentNormalize": "Latent normalize",
    "TSamplerWithTransform": "TSampler with transforms (Latent Control)",
    "TransformSampler": "TSampler (Latent Control)",
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

