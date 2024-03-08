import torch


def multiply_transform(x0, params) -> list:
    x = x0

    if params["mode"] == "replace":
        x *= params["multiplier"]
    elif params["mode"] == "combine":
        x = (x * params["multiplier"] + x) / 2

    return x


def shift_transform(x0, params) -> list:
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


def mirror_transform(x0, params) -> list:
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