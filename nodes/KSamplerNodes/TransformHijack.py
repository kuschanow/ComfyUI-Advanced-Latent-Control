from .TransformContext import TransformContext


class TransformHijack:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required" : {
                "latent": ("LATENT",),
                "transforms": ("TRANSFORM",)
            },
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "func"

    CATEGORY = "sampling/transforms"

    _context = None
    _hijack_node_id = None

    def func(self, latent, transforms):
        latent["transforms"] = transforms

        if TransformHijack._context is None:
            TransformHijack._hijack_node_id = id
            TransformHijack._context = TransformContext()
        else:
            return (latent,)

        TransformHijack._context.hijack()
        return (latent,)
