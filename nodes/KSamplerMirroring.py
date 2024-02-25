import comfy.samplers
import torch
from .utils.sampler_callback import prepare_callback


MIRROR_DIRECTIONS = ["none", "vertically", "horizontally", "both", "90 degree rotation", "180 degree rotation"]
MODE = ["replace", "combine"]

class KSamplerMirroring:
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

    def sample(self, model, seed, steps, cfg, sampler_name, scheduler, positive, negative, latent_image, denoise=1.0, start_mirror_at=0, stop_mirror_at=0, mirror_mode="replace", mirror_direction="none", start_shift_at=0, stop_shift_at=0, shift_mode="replace", x_shift=0, y_shift=0, start_multiplier_at=0, stop_multiplier_at=0, multiplier_mode="combine", multiplier=1):
        return common_ksampler(
            model,
            seed,
            steps,
            cfg,
            sampler_name,
            scheduler,
            positive,
            negative,
            latent_image,
            {
                "start_mirror_at": start_mirror_at,
                "stop_mirror_at": stop_mirror_at,
                "mirror_mode": mirror_mode,
                "mirror_direction": mirror_direction,
                "start_shift_at": start_shift_at,
                "stop_shift_at": stop_shift_at,
                "shift_mode": shift_mode,
                "x_shift": x_shift,
                "y_shift": y_shift,
                "start_multiplier_at": start_multiplier_at,
                "stop_multiplier_at": stop_multiplier_at,
                "multiplier_mode": multiplier_mode,
                "multiplier": multiplier,
            },
            denoise=denoise)

def common_ksampler(model, seed, steps, cfg, sampler_name, scheduler, positive, negative, latent, mirroring_params, denoise=1.0, disable_noise=False, start_step=None, last_step=None, force_full_denoise=False):
    latent_image = latent["samples"]
    if disable_noise:
        noise = torch.zeros(latent_image.size(), dtype=latent_image.dtype, layout=latent_image.layout, device="cpu")
    else:
        batch_inds = latent["batch_index"] if "batch_index" in latent else None
        noise = comfy.sample.prepare_noise(latent_image, seed, batch_inds)

    noise_mask = None
    if "noise_mask" in latent:
        noise_mask = latent["noise_mask"]

    callback = prepare_callback(model, steps, mirroring_params)
    disable_pbar = not comfy.utils.PROGRESS_BAR_ENABLED
    samples = comfy.sample.sample(model, noise, steps, cfg, sampler_name, scheduler, positive, negative, latent_image,
                                  denoise=denoise, disable_noise=disable_noise, start_step=start_step, last_step=last_step,
                                  force_full_denoise=force_full_denoise, noise_mask=noise_mask, callback=callback, disable_pbar=disable_pbar, seed=seed)
    out = latent.copy()
    out["samples"] = samples
    return (out, )


