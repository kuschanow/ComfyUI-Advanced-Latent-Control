from itertools import chain


class OffsetCombine:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "offset1": ("OFFSET", ),
                "offset2": ("OFFSET", ),
                "offset": ("INT", {"default": 0, "min": -10000, "max": 10000}),
            }
        }

    RETURN_TYPES = ("OFFSET",)
    FUNCTION = "combine"

    CATEGORY = "sampling/transforms"

    def combine(self, offset, **kwargs):
        offsets = sum(chain([v for k, v in kwargs.items()]), [])

        for o in offsets:
            o["offset"] += offset

        return (offsets,)
