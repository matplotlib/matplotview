from matplotlib.axes import Axes
from matplotlib.transforms import Bbox
import matplotlib.docstring as docstring
from matplotview._transform_renderer import _TransformRenderer


def view_wrapper(axes_class):
    @docstring.interpd
    class ViewAxesImpl(axes_class):
        """
        An axes which automatically displays elements of another axes. Does not
        require Artists to be plotted twice.
        """
        __module__ = axes_class.__module__
        # The number of allowed recursions in the draw method
        MAX_RENDER_DEPTH = 1

        def __init__(
            self,
            axes_to_view,
            rect,
            zorder=5,
            image_interpolation="nearest",
            **kwargs
        ):
            """
            Construct a new view axes.

            Parameters
            ----------
            axes_to_view: `~.axes.Axes`
                The axes to zoom in on which this axes will be nested inside.

            rect: [left, bottom, width, height]
                The Axes is built in the rectangle *rect*.

            zorder: int
                An integer, the z-order of the axes. Defaults to 5.

            image_interpolation: string
                Supported options are 'antialiased', 'nearest', 'bilinear',
                'bicubic', 'spline16', 'spline36', 'hanning', 'hamming',
                'hermite', 'kaiser', 'quadric', 'catrom', 'gaussian', 'bessel',
                'mitchell', 'sinc', 'lanczos', or 'none'. The default value is
                'nearest'. This determines the interpolation used when
                attempting to render a view of an image.

            **kwargs
                Other optional keyword arguments:

                %(Axes:kwdoc)s

            Returns
            -------
            `~.axes.ZoomViewAxes`
                The new zoom view axes instance...
            """
            super().__init__(axes_to_view.figure, rect, zorder=zorder,
                             **kwargs)
            self._init_vars(axes_to_view, image_interpolation)


        def _init_vars(
            self,
            axes_to_view,
            image_interpolation="nearest"
        ):
            self.__view_axes = axes_to_view
            self.__image_interpolation = image_interpolation
            self._render_depth = 0
            self.__scale_lines = True

        def draw(self, renderer=None):
            if(self._render_depth >= self.MAX_RENDER_DEPTH):
                return
            self._render_depth += 1

            super().draw(renderer)

            if(not self.get_visible()):
                return

            axes_children = [
                *self.__view_axes.collections,
                *self.__view_axes.patches,
                *self.__view_axes.lines,
                *self.__view_axes.texts,
                *self.__view_axes.artists,
                *self.__view_axes.images,
                *self.__view_axes.child_axes
            ]

            # Sort all rendered items by their z-order so they render in layers
            # correctly...
            axes_children.sort(key=lambda obj: obj.get_zorder())

            artist_boxes = []
            # We need to temporarily disable the clip boxes of all of the
            # artists, in order to allow us to continue rendering them it even
            # if it is outside of the parent axes (they might still be visible
            # in this zoom axes).
            for a in axes_children:
                artist_boxes.append(a.get_clip_box())
                a.set_clip_box(a.get_window_extent(renderer))

            # Construct mock renderer and draw all artists to it.
            mock_renderer = _TransformRenderer(
                renderer, self.__view_axes.transData, self.transData, self,
                self.__image_interpolation, self.__scale_lines
            )
            x1, x2 = self.get_xlim()
            y1, y2 = self.get_ylim()
            axes_box = Bbox.from_extents(x1, y1, x2, y2).transformed(
                self.__view_axes.transData
            )

            for artist in axes_children:
                if(
                    (artist is not self)
                    and (
                        Bbox.intersection(
                            artist.get_window_extent(renderer), axes_box
                        ) is not None
                    )
                ):
                    artist.draw(mock_renderer)

            # Reset all of the artist clip boxes...
            for a, box in zip(axes_children, artist_boxes):
                a.set_clip_box(box)

            # We need to redraw the splines if enabled, as we have finally
            # drawn everything... This avoids other objects being drawn over
            # the splines.
            if(self.axison and self._frameon):
                for spine in self.spines.values():
                    spine.draw(renderer)

            self._render_depth -= 1

        def get_linescaling(self):
            """
            Get if line width scaling is enabled.

            Returns
            -------
            bool
                If line width scaling is enabled returns True, otherwise False.
            """
            return self.__scale_lines

        def set_linescaling(self, value):
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

        @classmethod
        def from_axes(cls, axes, axes_to_view, image_interpolation="nearest"):
            axes.__class__ = cls
            axes._init_vars(axes_to_view, image_interpolation)
            return axes

    new_name = f"{ViewAxesImpl.__name__}[{axes_class.__name__}]"
    ViewAxesImpl.__name__ = ViewAxesImpl.__qualname__ = new_name

    return ViewAxesImpl

ViewAxes = view_wrapper(Axes)