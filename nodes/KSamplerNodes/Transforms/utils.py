import torch
import comfy

def multiply_transform(x0, params):
    x = x0

    if params["mode"] == "replace":
        x *= params["multiplier"]
    elif params["mode"] == "combine":
        x = (x * params["multiplier"] + x) / 2

    return x


def shift_transform(x0, params):
    x = x0

    if params["mode"] == "replace":
        if params["x_shift"] != 0:
            x = torch.roll(x, shifts=int(x.size()[2] * params["x_shift"]), dims=[2])
        if params["y_shift"] != 0:
            x = torch.roll(x, shifts=int(x.size()[1] * params["y_shift"]), dims=[1])
    elif params["mode"] == "combine":
        if params["x_shift"] != 0:
            x = (torch.roll(x, shifts=int(x.size()[2] * params["x_shift"]), dims=[2]) + x) / 2
        if params["y_shift"] != 0:
            x = (torch.roll(x, shifts=int(x.size()[1] * params["y_shift"]), dims=[1]) + x) / 2

    return x


def mirror_transform(x0, params):
    x = x0

    if params["mode"] == "replace":
        if params["direction"] == "vertically":
            x = torch.flip(x, [1])
        elif params["direction"] == "horizontally":
            x = torch.flip(x, [2])
        elif params["direction"] == "both":
            x = torch.flip(x, [1, 2])
        elif params["direction"] == "90 degree rotation":
            x = torch.rot90(x, dims=[1, 2])
        elif params["direction"] == "180 degree rotation":
            x = torch.rot90(torch.rot90(x, dims=[1, 2]), dims=[1, 2])
    elif params["mode"] == "combine":
        if params["direction"] == "vertically":
            x = (torch.flip(x, [1]) + x) / 2
        elif params["direction"] == "horizontally":
            x = (torch.flip(x, [2]) + x) / 2
        elif params["direction"] == "both":
            x = (torch.flip(x, [1, 2]) + x) / 2
        elif params["direction"] == "90 degree rotation":
            x = (torch.rot90(x, dims=[1, 2]) + x) / 2
        elif params["direction"] == "180 degree rotation":
            x = (torch.rot90(torch.rot90(x, dims=[1, 2]), dims=[1, 2]) + x) / 2

    return x


def latent_interpolate_transform(x0, params):
    latent = params["latent"]

    if x0.shape != latent.shape:
        latent.permute(0, 3, 1, 2)
        latent = comfy.utils.common_upscale(latent, x0.shape[3], x0.shape[2], 'bicubic')
        latent.permute(0, 2, 3, 1)

    x = x0 * params["factor"] + latent * (1 - params["factor"])
    x *= params["multiplier"]

    return x


def latent_add_transform(x0, params):
    latent = params["latent"]

    if x0.shape != latent.shape:
        latent.permute(0, 3, 1, 2)
        latent = comfy.utils.common_upscale(latent, x0.shape[3], x0.shape[2], 'bicubic')
        latent.permute(0, 2, 3, 1)

    x = x0 + latent
    x *= params["multiplier"]

    return x


def get_offset_list(offsets, total_steps):
    if offsets is None:
        return [True for _ in range(total_steps)]

    def list_without_offset(offset):
        return [
            True if x % offset["process_every"] == 0 else False
            for x in
            range(total_steps)
        ] if offset["mode"] == "process_every" else [
                False if x % offset["process_every"] == 0 else True
                for x in
                range(total_steps)
        ]
    def list_with_offset(offset):
        _list = list_without_offset(offset)
        return _list[-offset["offset"]:] + _list[:-offset["offset"]]

    lists = [
        list_with_offset(offset)
        for offset in
        offsets
    ]

    return [any(values) for values in zip(*lists)]
