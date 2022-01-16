from matplotview._view_axes import view_wrapper

def view(axes, axes_to_view, image_interpolation="nearest"):
    """
    Convert an axes into a view of another axes, displaying the contents of
    the second axes.

    Parameters
    ----------
    axes: Axes
        The axes to turn into a view of another axes.

    axes_to_view: Axes
        The axes to display the contents of in the first axes, the 'viewed'
        axes.

    image_interpolation:
        The image interpolation method to use when displaying scaled images
        from the axes being viewed. Defaults to "nearest". Supported options
        are 'antialiased', 'nearest', 'bilinear', 'bicubic', 'spline16',
        'spline36', 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric',
        'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos',
        or 'none'
    """
    return view_wrapper(type(axes)).from_axes(axes, axes_to_view, image_interpolation)


def inset_zoom_axes(axes, bounds, *, image_interpolation="nearest", transform=None, zorder=5, **kwargs):
    """
    Add a child inset Axes to an Axes, which automatically plots
    artists contained within the parent Axes.

    Parameters
    ----------
    axes: Axes
        The axes to insert a new inset zoom axes inside.

    bounds: [x0, y0, width, height]
        Lower-left corner of inset Axes, and its width and height.

    transform: `.Transform`
        Defaults to `ax.transAxes`, i.e. the units of *rect* are in
        Axes-relative coordinates.

    zorder: number
        Defaults to 5 (same as `.Axes.legend`).  Adjust higher or lower
        to change whether it is above or below data plotted on the
        parent Axes.

    image_interpolation: string
        Supported options are 'antialiased', 'nearest', 'bilinear',
        'bicubic', 'spline16', 'spline36', 'hanning', 'hamming', 'hermite',
        'kaiser', 'quadric', 'catrom', 'gaussian', 'bessel', 'mitchell',
        'sinc', 'lanczos', or 'none'. The default value is 'nearest'. This
        determines the interpolation used when attempting to render a
        zoomed version of an image.

    **kwargs
        Other keyword arguments are passed on to the child `.Axes`.

    Returns
    -------
    ax
        The created `~.axes.Axes` instance.

    Examples
    --------
    See `Axes.inset_axes` method for examples.
    """
    inset_ax = axes.inset_axes(
        bounds, transform=transform, zorder=zorder, **kwargs
    )
    return view(inset_ax, axes, image_interpolation)
