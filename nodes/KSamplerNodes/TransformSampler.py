from .TransformContext import TransformContext
from nodes import KSampler, KSamplerAdvanced


def insert_transform_input(input_types):
    input_types["optional"] = {"transform_optional": ("TRANSFORM",)}
    return input_types


class Transforms:
    clazz = None

    @classmethod
    def INPUT_TYPES(cls):
        return insert_transform_input(cls.clazz.INPUT_TYPES())

    FUNCTION = "func"

    def __init__(self):
        self.original_function_name = self.clazz.FUNCTION

    def func(self, **kwargs):
        ctx = TransformContext()
        ctx.hijack()
        latent = kwargs["latent_image"]
        latent["transforms"] = kwargs.pop("transform_optional")
        kwargs["latent_image"] = latent
        out = getattr(self, self.clazz.FUNCTION)(**kwargs)
        return out


def variations_factory(original_class: type, name=None) -> type:
    name = name or original_class.__name__ + "Transform"
    return type(name, (Transforms, original_class), {'clazz': original_class})

TSampler = variations_factory(KSampler)
TSamplerAdvanced = variations_factory(KSamplerAdvanced)
