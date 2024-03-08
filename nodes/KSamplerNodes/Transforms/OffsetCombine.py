


class OffsetCombine:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "offset1": ("OFFSET", ),
                "offset2": ("OFFSET", ),
            }
        }

    RETURN_TYPES = ("OFFSET",)
    FUNCTION = "combine"

    CATEGORY = "sampling/transforms"

    def combine(self, offset1, offset2):
        return (offset1 + offset2,)
