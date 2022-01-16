from matplotlib.backend_bases import RendererBase
from matplotlib.transforms import Bbox, IdentityTransform, Affine2D
from matplotlib.path import Path
import matplotlib._image as _image
import numpy as np
from matplotlib.image import _interpd_


class _TransformRenderer(RendererBase):
    """
    A matplotlib renderer which performs transforms to change the final
    location of plotted elements, and then defers drawing work to the
    original renderer.
    """

    def __init__(
        self,
        base_renderer,
        mock_transform,
        transform,
        bounding_axes,
        image_interpolation="nearest",
        scale_linewidths=True
    ):
        """
        Constructs a new TransformRender.

        Parameters
        ----------
        base_renderer: `~matplotlib.backend_bases.RenderBase`
            The renderer to use for drawing objects after applying transforms.

        mock_transform: `~matplotlib.transforms.Transform`
            The transform or coordinate space which all passed
            paths/triangles/images will be converted to before being placed
            back into display coordinates by the main transform. For example
            if the parent axes transData is passed, all objects will be
            converted to the parent axes data coordinate space before being
            transformed via the main transform back into coordinate space.

        transform: `~matplotlib.transforms.Transform`
            The main transform to be used for plotting all objects once
            converted into the mock_transform coordinate space. Typically this
            is the child axes data coordinate space (transData).

        bounding_axes: `~matplotlib.axes.Axes`
            The axes to plot everything within. Everything outside of this
            axes will be clipped.

        image_interpolation: string
            Supported options are 'antialiased', 'nearest', 'bilinear',
            'bicubic', 'spline16', 'spline36', 'hanning', 'hamming', 'hermite',
            'kaiser', 'quadric', 'catrom', 'gaussian', 'bessel', 'mitchell',
            'sinc', 'lanczos', or 'none'. The default value is 'nearest'. This
            determines the interpolation used when attempting to render a
            zoomed version of an image.

        scale_linewidths: bool, default is True
            Specifies if line widths should be scaled, in addition to the
            paths themselves.

        Returns
        -------
        `~._zoom_axes._TransformRenderer`
            The new transform renderer.
        """
        super().__init__()
        self.__renderer = base_renderer
        self.__mock_trans = mock_transform
        self.__core_trans = transform
        self.__bounding_axes = bounding_axes
        self.__scale_widths = scale_linewidths

        try:
            self.__img_inter = _interpd_[image_interpolation.lower()]
        except KeyError:
            raise ValueError(
                f"Invalid Interpolation Mode: {image_interpolation}"
            )

    def _scale_gc(self, gc):
        transfer_transform = self._get_transfer_transform(IdentityTransform())
        new_gc = self.__renderer.new_gc()
        new_gc.copy_properties(gc)

        unit_box = Bbox.from_bounds(0, 0, 1, 1)
        unit_box = transfer_transform.transform_bbox(unit_box)
        mult_factor = np.sqrt(unit_box.width * unit_box.height)

        new_gc.set_linewidth(gc.get_linewidth() * mult_factor)
        new_gc._hatch_linewidth = gc.get_hatch_linewidth() * mult_factor

        return new_gc

    def _get_axes_display_box(self):
        """
        Private method, get the bounding box of the child axes in display
        coordinates.
        """
        return self.__bounding_axes.patch.get_bbox().transformed(
            self.__bounding_axes.transAxes
        )

    def _get_transfer_transform(self, orig_transform):
        """
        Private method, returns the transform which translates and scales
        coordinates as if they were originally plotted on the child axes
        instead of the parent axes.

        Parameters
        ----------
        orig_transform: `~matplotlib.transforms.Transform`
            The transform that was going to be originally used by the
            object/path/text/image.

        Returns
        -------
        `~matplotlib.transforms.Transform`
            A matplotlib transform which goes from original point data ->
            display coordinates if the data was originally plotted on the
            child axes instead of the parent axes.
        """
        # We apply the original transform to go to display coordinates, then
        # apply the parent data transform inverted to go to the parent axes
        # coordinate space (data space), then apply the child axes data
        # transform to go back into display space, but as if we originally
        # plotted the artist on the child axes....
        return (
            orig_transform + self.__mock_trans.inverted() + self.__core_trans
        )

    # We copy all of the properties of the renderer we are mocking, so that
    # artists plot themselves as if they were placed on the original renderer.
    @property
    def height(self):
        return self.__renderer.get_canvas_width_height()[1]

    @property
    def width(self):
        return self.__renderer.get_canvas_width_height()[0]

    def get_text_width_height_descent(self, s, prop, ismath):
        return self.__renderer.get_text_width_height_descent(s, prop, ismath)

    def get_canvas_width_height(self):
        return self.__renderer.get_canvas_width_height()

    def get_texmanager(self):
        return self.__renderer.get_texmanager()

    def get_image_magnification(self):
        return self.__renderer.get_image_magnification()

    def _get_text_path_transform(self, x, y, s, prop, angle, ismath):
        return self.__renderer._get_text_path_transform(x, y, s, prop, angle,
                                                        ismath)

    def option_scale_image(self):
        return False

    def points_to_pixels(self, points):
        return self.__renderer.points_to_pixels(points)

    def flipy(self):
        return self.__renderer.flipy()

    def new_gc(self):
        return self.__renderer.new_gc()

    # Actual drawing methods below:
    def draw_path(self, gc, path, transform, rgbFace=None):
        # Convert the path to display coordinates, but if it was originally
        # drawn on the child axes.
        path = path.deepcopy()
        path.vertices = self._get_transfer_transform(transform).transform(
            path.vertices
        )
        bbox = self._get_axes_display_box()

        # We check if the path intersects the axes box at all, if not don't
        # waste time drawing it.
        if(not path.intersects_bbox(bbox, True)):
            return

        if(self.__scale_widths):
            gc = self._scale_gc(gc)

        # Change the clip to the sub-axes box
        gc.set_clip_rectangle(bbox)

        self.__renderer.draw_path(gc, path, IdentityTransform(), rgbFace)

    def _draw_text_as_path(self, gc, x, y, s, prop, angle, ismath):
        # If the text field is empty, don't even try rendering it...
        if((s is None) or (s.strip() == "")):
            return

        # Call the super class instance, which works for all cases except one
        # checked above... (Above case causes error)
        super()._draw_text_as_path(gc, x, y, s, prop, angle, ismath)

    def draw_gouraud_triangle(self, gc, points, colors, transform):
        # Pretty much identical to draw_path, transform the points and adjust
        # clip to the child axes bounding box.
        points = self._get_transfer_transform(transform).transform(points)
        path = Path(points, closed=True)
        bbox = self._get_axes_display_box()

        if(not path.intersects_bbox(bbox, True)):
            return

        if(self.__scale_widths):
            gc = self._scale_gc(gc)

        gc.set_clip_rectangle(bbox)

        self.__renderer.draw_gouraud_triangle(gc, path.vertices, colors,
                                              IdentityTransform())

    # Images prove to be especially messy to deal with...
    def draw_image(self, gc, x, y, im, transform=None):
        mag = self.get_image_magnification()
        shift_data_transform = self._get_transfer_transform(
            IdentityTransform()
        )
        axes_bbox = self._get_axes_display_box()
        # Compute the image bounding box in display coordinates....
        # Image arrives pre-magnified.
        img_bbox_disp = Bbox.from_bounds(x, y, im.shape[1], im.shape[0])
        # Now compute the output location, clipping it with the final axes
        # patch.
        out_box = img_bbox_disp.transformed(shift_data_transform)
        clipped_out_box = Bbox.intersection(out_box, axes_bbox)

        if(clipped_out_box is None):
            return

        # We compute what the dimensions of the final output image within the
        # sub-axes are going to be.
        x, y, out_w, out_h = clipped_out_box.bounds
        out_w, out_h = int(np.ceil(out_w * mag)), int(np.ceil(out_h * mag))

        if((out_w <= 0) or (out_h <= 0)):
            return

        # We can now construct the transform which converts between the
        # original image (a 2D numpy array which starts at the origin) to the
        # final zoomed image.
        img_trans = (
            Affine2D().scale(1/mag, 1/mag)
            .translate(img_bbox_disp.x0, img_bbox_disp.y0)
            + shift_data_transform
            + Affine2D().translate(-clipped_out_box.x0, -clipped_out_box.y0)
            .scale(mag, mag)
        )

        # We resize and zoom the original image onto the out_arr.
        out_arr = np.zeros((out_h, out_w, im.shape[2]), dtype=im.dtype)
        trans_msk = np.zeros((out_h, out_w), dtype=im.dtype)

        _image.resample(im, out_arr, img_trans, self.__img_inter, alpha=1)
        _image.resample(im[:, :, 3], trans_msk, img_trans, self.__img_inter,
                        alpha=1)
        out_arr[:, :, 3] = trans_msk

        if(self.__scale_widths):
            gc = self._scale_gc(gc)

        gc.set_clip_rectangle(clipped_out_box)

        x, y = clipped_out_box.x0, clipped_out_box.y0

        if(self.option_scale_image()):
            self.__renderer.draw_image(gc, x, y, out_arr, None)
        else:
            self.__renderer.draw_image(gc, x, y, out_arr)

