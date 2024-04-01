import torch
import nodes
import comfy
from latent_preview import prepare_callback as preview_callback


class TransformContext:
    original_sample_function = nodes.common_ksampler

    def get_transform_sample_function(self):
        def prepare_callback(model, steps, x0_output_dict=None, transforms=None):
            def transform_callback(step, x0, x, total_steps):
                if transforms is None:
                    return

                for transform in transforms:
                    for i in range(x0.size()[0]):
                        x0[i] = transform["function"](step, x0[i].unsqueeze(0), total_steps, transform["params"])

            preview = preview_callback(model, steps, x0_output_dict)

            def callback(step, x0, x, total_steps):
                transform_callback(step, x0, x, total_steps)
                preview(step, x0, x, total_steps)

            return callback

        def sample(model, seed, steps, cfg, sampler_name, scheduler, positive, negative, latent, denoise=1.0,
                          disable_noise=False, start_step=None, last_step=None, force_full_denoise=False):
            latent_image = latent["samples"]
            if disable_noise:
                noise = torch.zeros(latent_image.size(), dtype=latent_image.dtype, layout=latent_image.layout, device="cpu")
            else:
                batch_inds = latent["batch_index"] if "batch_index" in latent else None
                noise = comfy.sample.prepare_noise(latent_image, seed, batch_inds)

            noise_mask = None
            if "noise_mask" in latent:
                noise_mask = latent["noise_mask"]

            callback = prepare_callback(model, steps, transforms=latent["transforms"])
            disable_pbar = not comfy.utils.PROGRESS_BAR_ENABLED
            samples = comfy.sample.sample(model, noise, steps, cfg, sampler_name, scheduler, positive, negative, latent_image,
                                          denoise=denoise, disable_noise=disable_noise, start_step=start_step,
                                          last_step=last_step,
                                          force_full_denoise=force_full_denoise, noise_mask=noise_mask, callback=callback,
                                          disable_pbar=disable_pbar, seed=seed)
            out = latent.copy()
            out["samples"] = samples
            self.unhijack()
            return (out,)

        return sample

    def hijack(self):
        nodes.common_ksampler = self.get_transform_sample_function()

    def unhijack(self):
        nodes.common_ksampler = TransformContext.original_sample_function

    def __enter__(self):
        self.hijack()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.unhijack()
