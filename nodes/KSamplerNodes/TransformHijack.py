from .transform_apply import attach_transforms


class TransformHijack:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
                "transforms": ("TRANSFORM",),
            },
        }

    RETURN_TYPES = ("MODEL",)
    FUNCTION = "func"

    CATEGORY = "sampling/transforms"

    def func(self, model, transforms):
        return (attach_transforms(model, transforms),)