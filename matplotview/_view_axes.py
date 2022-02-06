import functools
import itertools
from typing import Type, List, Optional, Callable, Any
from matplotlib.axes import Axes
from matplotlib.transforms import Bbox
import matplotlib.docstring as docstring
from matplotview._transform_renderer import _TransformRenderer
from matplotlib.artist import Artist
from matplotlib.backend_bases import RendererBase

DEFAULT_RENDER_DEPTH = 5

class _BoundRendererArtist:
    """
    Provides a temporary wrapper around a given artist, inheriting its
    attributes and values, while overloading draw to use a fixed
    TransformRenderer. This is used to render an artist to a view without
    having to implement a new draw for every Axes type.
    """
    def __init__(
        self,
        artist: Artist,
        renderer: _TransformRenderer,
        clip_box: Bbox
    ):
        self._artist = artist
        self._renderer = renderer
        self._clip_box = clip_box

    def __getattribute__(self, item: str) -> Any:
        try:
            return super().__getattribute__(item)
        except AttributeError:
            return self._artist.__getattribute__(item)

    def __setattr__(self, key: str, value: Any):
        try:
            super().__setattr__(key, value)
        except AttributeError:
            self._artist.__setattr__(key, value)

    def draw(self, renderer: RendererBase):
        # Disable the artist defined clip box, as the artist might be visible
        # under the new renderer even if not on screen...
        clip_box_orig = self._artist.get_clip_box()
        clip_path_orig = self._artist.get_clip_path()

        full_extents = self._artist.get_window_extent(self._renderer)
        self._artist.set_clip_box(None)
        self._artist.set_clip_path(None)

        # If we are working with a 3D object, swap out it's axes with
        # this zoom axes (swapping out the 3d transform) and reproject it.
        if(hasattr(self._artist, "do_3d_projection")):
            self.do_3d_projection()

        # Check and see if the passed limiting box and extents of the
        # artist intersect, if not don't bother drawing this artist.
        # First 2 checks are a special case where we received a bad clip box.
        # (those can happen when we try to get the bounds of a map projection)
        if(
            self._clip_box.width == 0 or self._clip_box.height == 0 or
            Bbox.intersection(full_extents, self._clip_box) is not None
        ):
            self._artist.draw(self._renderer)

        # Re-enable the clip box... and clip path...
        self._artist.set_clip_box(clip_box_orig)
        self._artist.set_clip_path(clip_path_orig)

    def do_3d_projection(self) -> float:
        # Get the 3D projection function...
        do_3d_projection = getattr(self._artist, "do_3d_projection")

        # Intentionally replace the axes of the artist with the view axes,
        # as the do_3d_projection pulls the 3D transform (M) from the axes.
        # Then reproject, and restore the original axes.
        ax = self._artist.axes
        self._artist.axes = None  # Set to None first to avoid exception...
        self._artist.axes = self._renderer.bounding_axes
        res = do_3d_projection()  # Returns a z-order value...
        self._artist.axes = None
        self._artist.axes = ax

        return res

def _view_from_pickle(builder, args):
    """
    PRIVATE: Construct a View wrapper axes given an axes builder and class.
    """
    res = builder(*args)
    res.__class__ = view_wrapper(type(res))
    return res

# Cache classes so grabbing the same type twice leads to actually getting the
# same type (and type comparisons work).
@functools.lru_cache(None)
def view_wrapper(axes_class: Type[Axes]) -> Type[Axes]:
    """
    Construct a View axes, which subclasses, or wraps a specific Axes subclass.
    A View axes can be configured to display the contents of another Axes
    within the same Figure.

    Parameters
    ----------
    axes_class: Type[Axes]
        An axes type to construct a new ViewAxes wrapper class for.

    Returns
    -------
    View[axes_class]:
        The view axes wrapper for a given axes class, capable of displaying
        another axes contents...
    """
    @docstring.interpd
    class View(axes_class):
        """
        An axes which automatically displays elements of another axes. Does not
        require Artists to be plotted twice.
        """
        def __init__(
            self,
            axes_to_view: Axes,
            *args,
            image_interpolation: str = "nearest",
            render_depth: int = DEFAULT_RENDER_DEPTH,
            filter_function: Optional[Callable[[Artist], bool]] = None,
            **kwargs
        ):
            """
            Construct a new view axes.

            Parameters
            ----------
            axes_to_view: `~.axes.Axes`
                The axes to create a view of.

            *args
                Additional arguments to be passed to the Axes class this
                ViewAxes wraps.

            image_interpolation: string
                Supported options are 'antialiased', 'nearest', 'bilinear',
                'bicubic', 'spline16', 'spline36', 'hanning', 'hamming',
                'hermite', 'kaiser', 'quadric', 'catrom', 'gaussian', 'bessel',
                'mitchell', 'sinc', 'lanczos', or 'none'. The default value is
                'nearest'. This determines the interpolation used when
                attempting to render a view of an image.

            render_depth: int, positive, defaults to 10
                The number of recursive draws allowed for this view, this can
                happen if the view is a child of the axes (such as an inset
                axes) or if two views point at each other. Defaults to 10.

            filter_function: callable(Artist) -> bool or None
                An optional filter function, which can be used to select what
                artists are drawn by the view. If the function returns True,
                the element is drawn, otherwise it isn't. Defaults to None,
                or drawing all artists.

            **kwargs
                Other optional keyword arguments supported by the Axes
                constructor this ViewAxes wraps:

                %(Axes:kwdoc)s

            Returns
            -------
            View
                The new zoom view axes instance...
            """
            super().__init__(axes_to_view.figure, *args, **kwargs)
            self._init_vars(
                axes_to_view, image_interpolation,
                render_depth, filter_function
            )

        def _init_vars(
            self,
            axes_to_view: Axes,
            image_interpolation: str,
            render_depth: int,
            filter_function: Optional[Callable[[Artist], bool]]
        ):
            if(render_depth < 1):
                raise ValueError(f"Render depth of {render_depth} is invalid.")
            if(filter_function is not None and not callable(filter_function)):
                raise ValueError(
                    f"The filter function must be a callable or None!"
                )

            self.__view_axes = axes_to_view
            # The current render depth is stored in the figure, so the number
            # of recursive draws is even in the case of multiple axes drawing
            # each other in the same figure.
            self.figure._current_render_depth = getattr(
                self.figure, "_current_render_depth", 0
            )
            self.__image_interpolation = image_interpolation
            self.__max_render_depth = render_depth
            self.__filter_function = filter_function
            self.__scale_lines = True
            self.__renderer = None

        def get_children(self) -> List[Artist]:
            # We overload get_children to return artists from the view axes
            # in addition to this axes when drawing. We wrap the artists
            # in a BoundRendererArtist, so they are drawn with an alternate
            # renderer, and therefore to the correct location.
            if(self.__renderer is not None):
                mock_renderer = _TransformRenderer(
                    self.__renderer, self.__view_axes.transData,
                    self.transData, self, self.__image_interpolation,
                    self.__scale_lines
                )

                x1, x2 = self.get_xlim()
                y1, y2 = self.get_ylim()
                axes_box = Bbox.from_extents(x1, y1, x2, y2).transformed(
                    self.__view_axes.transData
                )

                init_list = super().get_children()
                init_list.extend([
                    _BoundRendererArtist(a, mock_renderer, axes_box)
                    for a in itertools.chain(
                        self.__view_axes._children,
                        self.__view_axes.child_axes
                    ) if(self.__filter_function is None
                         or self.__filter_function(a))
                ])

                return init_list
            else:
                return super().get_children()

        def draw(self, renderer: RendererBase = None):
            # It is possible to have two axes which are views of each other
            # therefore we track the number of recursions and stop drawing
            # at a certain depth
            if(self.figure._current_render_depth >= self.__max_render_depth):
                return
            self.figure._current_render_depth += 1
            # Set the renderer, causing get_children to return the view's
            # children also...
            self.__renderer = renderer

            super().draw(renderer)

            # Get rid of the renderer...
            self.__renderer = None
            self.figure._current_render_depth -= 1

        def get_axes_to_view(self) -> Axes:
            """
            Get the axes this view will display.

            Returns
            -------
            Axes
                The axes being viewed.
            """
            return self.__view_axes

        def set_axes_to_view(self, ax: Axes):
            """
            Set the axes this view will display.

            Parameters
            ----------
            ax: Axes
                The new axes to be viewed.
            """
            self.__view_axes = ax

        def get_image_interpolation(self) -> str:
            """
            Get the current image interpolation used for rendering views of
            images. Supported options are 'antialiased', 'nearest', 'bilinear',
            'bicubic', 'spline16', 'spline36', 'hanning', 'hamming',
            'hermite', 'kaiser', 'quadric', 'catrom', 'gaussian', 'bessel',
            'mitchell', 'sinc', 'lanczos', or 'none'. The default value is
            'nearest'.

            Returns
            -------
            string
                The current image interpolation used when rendering views of
                images in this view axes.
            """
            return self.__image_interpolation

        def set_image_interpolation(self, val: str):
            """
            Set the current image interpolation used for rendering views of
            images. Supported options are 'antialiased', 'nearest', 'bilinear',
            'bicubic', 'spline16', 'spline36', 'hanning', 'hamming',
            'hermite', 'kaiser', 'quadric', 'catrom', 'gaussian', 'bessel',
            'mitchell', 'sinc', 'lanczos', or 'none'. The default value is
            'nearest'.

            Parameters
            ----------
            val: string
                A new image interpolation mode.
            """
            self.__image_interpolation = val

        def get_max_render_depth(self) -> int:
            """
            Get the max recursive rendering depth for this view axes.

            Returns
            -------
            int
                A positive non-zero integer, the number of recursive redraws
                this view axes will allow.
            """
            return self.__max_render_depth

        def set_max_render_depth(self, val: int):
            """
            Set the max recursive rendering depth for this view axes.

            Parameters
            ----------
            val: int
                The number of recursive draws of views this view axes will
                allow. Zero and negative values are invalid, and will raise a
                ValueError.
            """
            if(val <= 0):
                raise ValueError(f"Render depth must be positive, not {val}.")
            self.__max_render_depth = val

        def get_linescaling(self) -> bool:
            """
            Get if line width scaling is enabled.

            Returns
            -------
            bool
                If line width scaling is enabled returns True, otherwise False.
            """
            return self.__scale_lines

        def set_linescaling(self, value: bool):
            """
            Set whether line widths should be scaled when rendering a view of
            an axes.

            Parameters
            ----------
            value: bool
                If true, scale line widths in the view to match zoom level.
                Otherwise don't.
            """
            self.__scale_lines = value

        def get_filter_function(self) -> Optional[Callable[[Artist], bool]]:
            """
            Get the current artist filtering function.

            Returns
            -------
            function, optional
                The filter function, which accepts an artist and returns true
                if it should be drawn, otherwise false. Can also be none,
                meaning all artists should be drawn from the other axes.
            """
            return self.__filter_function

        def set_filter_function(self, f: Optional[Callable[[Artist], bool]]):
            """
            Set the artist filtering function.

            Returns
            -------
            f: function, optional
                A filter function, which accepts an artist and returns true
                if it should be drawn, otherwise false. Can also be set to
                None, meaning all artists should be drawn from the other axes.
            """
            self.__filter_function = f

        def __reduce__(self):
            builder, args = super().__reduce__()[:2]

            if(self.__new__ == builder):
                builder = super().__new__()

            cls = type(self)
            args = tuple(
                arg if(arg != cls) else cls.__bases__[0] for arg in args
            )

            return (
                _view_from_pickle,
                (builder, args),
                self.__getstate__()
            )

        def __getstate__(self):
            state = super().__getstate__()
            state["__renderer"] = None
            # We don't support pickling the filter...
            state["__filter_function"] = None
            return state

        @classmethod
        def from_axes(
            cls,
            axes: Axes,
            axes_to_view: Axes,
            image_interpolation: str = "nearest",
            render_depth: int = DEFAULT_RENDER_DEPTH,
            filter_function: Optional[Callable[[Artist], bool]] = None
        ) -> Axes:
            """
            Convert an Axes into a View in-place. This is used by public
            APIs to construct views, and using this method directly
            is not recommended. Instead use `view` which resolves types
            automatically.

            Parameters
            ----------
            axes: Axes
                The axes to convert to a view wrapping the same axes type.

            axes_to_view: `~.axes.Axes`
                The axes to create a view of.

            image_interpolation: string
                Supported options are 'antialiased', 'nearest', 'bilinear',
                'bicubic', 'spline16', 'spline36', 'hanning', 'hamming',
                'hermite', 'kaiser', 'quadric', 'catrom', 'gaussian', 'bessel',
                'mitchell', 'sinc', 'lanczos', or 'none'. The default value is
                'nearest'. This determines the interpolation used when
                attempting to render a view of an image.

            render_depth: int, positive, defaults to 10
                The number of recursive draws allowed for this view, this can
                happen if the view is a child of the axes (such as an inset
                axes) or if two views point at each other. Defaults to 10.

            filter_function: callable(Artist) -> bool or None
                An optional filter function, which can be used to select what
                artists are drawn by the view. If the function returns True,
                the element is drawn, otherwise it isn't. Defaults to None,
                or drawing all artists.

            Returns
            -------
            View
                The same axes passed in, which is now a View type which wraps
                the axes original type (View[axes_original_class]).

            Raises
            ------
            TypeError
                If the provided axes to convert has an Axes type which does
                not match the axes class this view type wraps.ss
            """
            if(type(axes) != axes_class):
                raise TypeError(
                    f"Can't convert {type(axes).__name__} to {cls.__name__}"
                )

            axes.__class__ = cls
            axes._init_vars(
                axes_to_view, image_interpolation,
                render_depth, filter_function
            )
            return axes

    View.__name__ = f"{View.__name__}[{axes_class.__name__}]"
    View.__qualname__ = f"{View.__qualname__}[{axes_class.__name__}]"

    return View