class TransformOffset:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "process_every": ("INT", {"default": 1, "min": 1, "max": 10000}),
                "offset": ("INT", {"default": 0, "min": -10000, "max": 10000}),
                "mode": (["process_every", "skip_every"],)
            }
        }

    RETURN_TYPES = ("OFFSET",)
    FUNCTION = "process"

    CATEGORY = "sampling/transforms"

    def process(self, process_every = 1, offset = 0, mode = "process_every"):
        return (
            {
                "process_every": process_every,
                "offset": offset % process_every,
                "mode": mode
            }
        )

