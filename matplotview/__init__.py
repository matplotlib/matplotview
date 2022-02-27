from typing import Optional, Iterable, Type, Union
from matplotlib.artist import Artist
from matplotlib.axes import Axes
from matplotview._view_axes import view_wrapper, ViewSpecification


__all__ = ["view", "inset_zoom_axes", "ViewSpecification"]


def view(
    axes: Axes,
    axes_to_view: Axes,
    image_interpolation: str = "nearest",
    render_depth: Optional[int] = None,
    filter_set: Optional[Iterable[Union[Type[Artist], Artist]]] = None,
    scale_lines: bool = True
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

    render_depth: optional int, positive, defaults to None
        The number of recursive draws allowed for this view, this can happen
        if the view is a child of the axes (such as an inset axes) or if
        two views point at each other. If None, uses the default render depth
        of 5, unless the axes passed is already a view axes, in which case the
        render depth the view already has will be used.

    filter_set: Iterable[Union[Type[Artist], Artist]] or None
        An optional filter set, which can be used to select what artists
        are drawn by the view. Any artists or artist types in the set are not
        drawn.

    scale_lines: bool, defaults to True
        Specifies if lines should be drawn thicker based on scaling in the
        view.
    """
    view_obj = view_wrapper(type(axes)).from_axes(axes, render_depth)
    view_obj.view_specifications[axes_to_view] = ViewSpecification(
        image_interpolation,
        filter_set,
        scale_lines
    )
    return view_obj


def inset_zoom_axes(
    axes: Axes,
    bounds: Iterable,
    *,
    image_interpolation: str = "nearest",
    render_depth: Optional[int] = None,
    filter_set: Optional[Iterable[Union[Type[Artist], Artist]]] = None,
    scale_lines: bool = True,
    transform=None,
    zorder: int = 5,
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

    render_depth: optional int, positive, defaults to None
        The number of recursive draws allowed for this view, this can happen
        if the view is a child of the axes (such as an inset axes) or if
        two views point at each other. If None, uses the default render depth
        of 5, unless the axes passed is already a view axes, in which case the
        render depth the view already has will be used.

    filter_set: Iterable[Union[Type[Artist], Artist]] or None
        An optional filter set, which can be used to select what artists
        are drawn by the view. Any artists or artist types in the set are not
        drawn.

    scale_lines: bool, defaults to True
        Specifies if lines should be drawn thicker based on scaling in the
        view.

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
        render_depth, filter_set, scale_lines
    )
