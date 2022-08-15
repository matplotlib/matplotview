from typing import Optional, Iterable, Type, Union
from matplotlib.artist import Artist
from matplotlib.axes import Axes
from matplotlib.transforms import Transform
from matplotview._view_axes import (
    view_wrapper,
    ViewSpecification,
    DEFAULT_RENDER_DEPTH
)
from matplotview._docs import dynamic_doc_string, get_interpolation_list_str


__all__ = ["view", "stop_viewing", "inset_zoom_axes"]


@dynamic_doc_string(
    render_depth=DEFAULT_RENDER_DEPTH,
    interp_list=get_interpolation_list_str()
)
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
    the second axes. If this axes is already viewing the passed axes (This
    function is called twice with the same axes arguments) this function
    will update the settings of the viewing instead of creating a new view.

    Parameters
    ----------
    axes: Axes
        The axes to turn into a view of another axes.

    axes_to_view: Axes
        The axes to display the contents of in the first axes, the 'viewed'
        axes.

    image_interpolation: string, default of '{image_interpolation}'
        The image interpolation method to use when displaying scaled images
        from the axes being viewed. Defaults to '{image_interpolation}'.
        Supported options are {interp_list}.

    render_depth: optional int, positive, defaults to None
        The number of recursive draws allowed for this view, this can happen
        if the view is a child of the axes (such as an inset axes) or if
        two views point at each other. If None, uses the default render depth
        of {render_depth}, unless the axes passed is already a view axes, in
        which case the render depth the view already has will be used.

    filter_set: Iterable[Union[Type[Artist], Artist]] or None
        An optional filter set, which can be used to select what artists
        are drawn by the view. Any artists or artist types in the set are not
        drawn.

    scale_lines: bool, defaults to {scale_lines}
        Specifies if lines should be drawn thicker based on scaling in the
        view.

    Returns
    -------
    axes
        The modified `~.axes.Axes` instance which is now a view.
        The modification occurs in-place.

    See Also
    --------
    matplotview.stop_viewing: Delete or stop an already constructed view.
    matplotview.inset_zoom_axes: Convenience method for creating inset axes
                                 that are views of the parent axes.
    """
    view_obj = view_wrapper(type(axes)).from_axes(axes, render_depth)
    view_obj.view_specifications[axes_to_view] = ViewSpecification(
        image_interpolation,
        filter_set,
        scale_lines
    )
    return view_obj


def stop_viewing(view: Axes, axes_of_viewing: Axes) -> Axes:
    """
    Terminate the viewing of a specified axes.

    Parameters
    ----------
    view: Axes
        The axes the is currently viewing the `axes_of_viewing`...

    axes_of_viewing: Axes
        The axes that the view should stop viewing.

    Returns
    -------
    view
        The view, which has now been modified in-place.

    Raises
    ------
    AttributeError
        If the provided `axes_of_viewing` is not actually being
        viewed by the specified view.

    See Also
    --------
    matplotview.view: To create views.
    """
    view = view_wrapper(type(view)).from_axes(view)
    del view.view_specifications[axes_of_viewing]
    return view


@dynamic_doc_string(
    render_depth=DEFAULT_RENDER_DEPTH,
    interp_list=get_interpolation_list_str()
)
def inset_zoom_axes(
    axes: Axes,
    bounds: Iterable,
    *,
    image_interpolation: str = "nearest",
    render_depth: Optional[int] = None,
    filter_set: Optional[Iterable[Union[Type[Artist], Artist]]] = None,
    scale_lines: bool = True,
    transform: Transform = None,
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
        Defaults to {zorder} (same as `.Axes.legend`).  Adjust higher or lower
        to change whether it is above or below data plotted on the
        parent Axes.

    image_interpolation: string
        Supported options are {interp_list}. The default value is
        '{image_interpolation}'. This determines the interpolation
        used when attempting to render a zoomed version of an image.

    render_depth: optional int, positive, defaults to None
        The number of recursive draws allowed for this view, this can happen
        if the view is a child of the axes (such as an inset axes) or if
        two views point at each other. If None, uses the default render depth
        of {render_depth}, unless the axes passed is already a view axes,
        in which case the render depth the view already has will be used.

    filter_set: Iterable[Union[Type[Artist], Artist]] or None
        An optional filter set, which can be used to select what artists
        are drawn by the view. Any artists or artist types in the set are not
        drawn.

    scale_lines: bool, defaults to {scale_lines}
        Specifies if lines should be drawn thicker based on scaling in the
        view.

    **kwargs
        Other keyword arguments are passed on to the child `.Axes`.

    Returns
    -------
    ax
        The created `~.axes.Axes` instance.

    See Also
    --------
    matplotview.view: For creating views in generalized cases.
    """
    inset_ax = axes.inset_axes(
        bounds, transform=transform, zorder=zorder, **kwargs
    )
    return view(
        inset_ax, axes, image_interpolation,
        render_depth, filter_set, scale_lines
    )
