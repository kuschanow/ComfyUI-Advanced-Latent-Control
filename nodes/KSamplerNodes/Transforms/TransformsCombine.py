


class TransformsCombine:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "transform1": ("TRANSFORM", ),
                "transform2": ("TRANSFORM", ),
            }
        }

    RETURN_TYPES = ("TRANSFORM",)
    FUNCTION = "combine"

    CATEGORY = "sampling/transforms"

    def combine(self, transform1, transform2):
        return (transform1 + transform2,)
