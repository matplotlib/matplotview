from matplotview._view_axes import view_wrapper

def view(axes, axes_to_view, image_interpolation="nearest"):
    return view_wrapper(type(axes)).from_axes(axes, axes_to_view, image_interpolation)

def zoom_inset_axes(axes, bounds, *, image_interpolation="nearest", transform=None, zorder=5, **kwargs):
    inset_ax = axes.inset_axes(bounds, transform, zorder, **kwargs)
    return view(inset_ax, axes, image_interpolation)
