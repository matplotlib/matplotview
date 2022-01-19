from typing import Callable, Optional, Iterable
from matplotlib.artist import Artist
from matplotlib.axes import Axes
from matplotview._view_axes import view_wrapper, DEFAULT_RENDER_DEPTH

def view(
    axes: Axes,
    axes_to_view: Axes,
    image_interpolation: str = "nearest",
    render_depth: int = DEFAULT_RENDER_DEPTH,
    filter_function: Optional[Callable[[Artist], bool]] = None
) -> Axes:
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

    image_interpolation: string, default of "nearest"
        The image interpolation method to use when displaying scaled images
        from the axes being viewed. Defaults to "nearest". Supported options
        are 'antialiased', 'nearest', 'bilinear', 'bicubic', 'spline16',
        'spline36', 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric',
        'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos',
        or 'none'

    render_depth: int, positive, defaults to 5
        The number of recursive draws allowed for this view, this can happen
        if the view is a child of the axes (such as an inset axes) or if
        two views point at each other. Defaults to 5.

    filter_function: callable(Artist) -> bool or None
        An optional filter function, which can be used to select what artists
        are drawn by the view. If the function returns True, the element is
        drawn, otherwise it isn't. Defaults to None, or drawing all artists.
    """
    return view_wrapper(type(axes)).from_axes(
        axes, axes_to_view, image_interpolation,
        render_depth, filter_function
    )


def inset_zoom_axes(
    axes: Axes,
    bounds: Iterable,
    *,
    image_interpolation="nearest",
    render_depth: int = DEFAULT_RENDER_DEPTH,
    filter_function: Optional[Callable[[Artist], bool]] = None,
    transform=None,
    zorder=5,
    **kwargs
) -> Axes:
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

    render_depth: int, positive, defaults to 5
        The number of recursive draws allowed for this view, this can happen
        if the view is a child of the axes (such as an inset axes) or if
        two views point at each other. Defaults to 5.

    filter_function: callable(Artist) -> bool or None
        An optional filter function, which can be used to select what artists
        are drawn by the view. If the function returns True, the element is
        drawn, otherwise it isn't. Defaults to None, or drawing all artists.

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
    return view(
        inset_ax, axes, image_interpolation,
        render_depth, filter_function
    )
