import comfy.samplers
from .TransformSampler import TransformSampler
from .Transforms import MirrorTransform, ShiftTransform, MultiplyTransform


MIRROR_DIRECTIONS = ["none", "vertically", "horizontally", "both", "90 degree rotation", "180 degree rotation"]
MODE = ["replace", "combine"]

class TSamplerWithTransform:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "steps": ("INT", {"default": 20, "min": 1, "max": 10000}),
                "cfg": ("FLOAT", {"default": 8.0, "min": 0.0, "max": 100.0, "step":0.1, "round": 0.01}),
                "sampler_name": (comfy.samplers.KSampler.SAMPLERS, ),
                "scheduler": (comfy.samplers.KSampler.SCHEDULERS, ),
                "positive": ("CONDITIONING", ),
                "negative": ("CONDITIONING", ),
                "latent_image": ("LATENT", ),
                "denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "start_mirror_at": ("FLOAT", {"default": 0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "stop_mirror_at": ("FLOAT", {"default": 0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "mirror_mode": (MODE,),
                "mirror_direction": (MIRROR_DIRECTIONS, {"default": "none"}),
                "start_shift_at": ("FLOAT", {"default": 0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "stop_shift_at": ("FLOAT", {"default": 0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "shift_mode": (MODE, {"default": "replace"}),
                "x_shift": ("FLOAT", {"default": 0, "min": -1, "max": 1, "step": 0.01}),
                "y_shift": ("FLOAT", {"default": 0, "min": -1, "max": 1, "step": 0.01}),
                "start_multiplier_at": ("FLOAT", {"default": 0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "stop_multiplier_at": ("FLOAT", {"default": 0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "multiplier_mode": (MODE, {"default": "combine"}),
                "multiplier": ("FLOAT", {"default": 1, "min": -10, "max": 10, "step": 0.01}),
             }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "sample"

    CATEGORY = "sampling"

    def sample(self,
               model,
               seed,
               steps,
               cfg,
               sampler_name,
               scheduler,
               positive,
               negative,
               latent_image,
               denoise=1.0,
               start_mirror_at=0,
               stop_mirror_at=0,
               mirror_mode="replace",
               mirror_direction="none",
               start_shift_at=0,
               stop_shift_at=0,
               shift_mode="replace",
               x_shift=0,
               y_shift=0,
               start_multiplier_at=0,
               stop_multiplier_at=0,
               multiplier_mode="combine",
               multiplier=1):

        transforms = (
            MirrorTransform().process(start_mirror_at, stop_mirror_at, mirror_mode, mirror_direction) +
            ShiftTransform().process(start_shift_at, stop_shift_at, shift_mode, x_shift, y_shift) +
            MultiplyTransform().process(start_multiplier_at, stop_multiplier_at, multiplier_mode, multiplier))[0]

        return TransformSampler().sample(
            model,
            seed,
            steps,
            cfg,
            sampler_name,
            scheduler,
            positive,
            negative,
            latent_image,
            transform_optional=transforms,
            denoise=denoise)


