import inspect
from inspect import signature


def dynamic_doc_string(**kwargs):
    def convert(func):
        default_vals = {
            k: v.default for k, v in signature(func).parameters.items()
            if(v.default is not inspect.Parameter.empty)
        }
        default_vals.update(kwargs)
        func.__doc__ = func.__doc__.format(**default_vals)

        return func

    return convert


def get_interpolation_list_str():
    from matplotlib.image import _interpd_
    return ", ".join([
        f"'{k}'" if(i != len(_interpd_) - 1) else f"or '{k}'"
        for i, k in enumerate(_interpd_)
    ])
