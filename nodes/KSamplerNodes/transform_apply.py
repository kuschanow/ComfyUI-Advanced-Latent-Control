import torch


def apply_transforms_to_x0(x0, step, total_steps, transforms):
    x = x0.clone()

    for transform in transforms:
        for i in range(x.size()[0]):
            x[i] = transform["function"](step, x[i].unsqueeze(0), total_steps, transform["params"])

    return x


def _find_step(sigma, sigmas):
    # sigma is a scalar tensor for the current model evaluation, sigmas is the full
    # schedule. High order samplers evaluate the model at intermediate sigmas that are
    # not part of the schedule; for those we return None so the transform is applied
    # exactly once per step (parity with the old per-step callback).
    diff = torch.abs(sigmas - sigma.to(sigmas.device))
    idx = int(torch.argmin(diff).item())
    if diff[idx] <= 1e-4 * max(1.0, float(sigmas[idx].abs())):
        return idx
    return None


def make_post_cfg_function(transforms):
    def post_cfg_function(args):
        denoised = args["denoised"]

        if not transforms:
            return denoised

        sigmas = args["model_options"].get("transformer_options", {}).get("sample_sigmas", None)
        if sigmas is None:
            return denoised

        step = _find_step(args["sigma"], sigmas)
        if step is None:
            return denoised

        total_steps = len(sigmas) - 1

        return apply_transforms_to_x0(denoised, step, total_steps, transforms)

    return post_cfg_function


def attach_transforms(model, transforms):
    m = model.clone()
    m.set_model_sampler_post_cfg_function(make_post_cfg_function(transforms))
    return m