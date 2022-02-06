import matplotlib.pyplot as plt
from matplotlib.testing.decorators import check_figures_equal
from matplotview.tests.utils import plotting_test, matches_post_pickle
from matplotview import view, view_wrapper, inset_zoom_axes, DEFAULT_RENDER_DEPTH
import numpy as np


def test_obj_comparison():
    from matplotlib.axes import Subplot, Axes

    view_class1 = view_wrapper(Subplot)
    view_class2 = view_wrapper(Subplot)
    view_class3 = view_wrapper(Axes)

    assert view_class1 is view_class2
    assert view_class1 == view_class2
    assert view_class2 != view_class3


@check_figures_equal(tol=5.6)
def test_getters_and_setters(fig_test, fig_ref):
    np.random.seed(1)
    im_data1 = np.random.rand(30, 30)
    im_data2 = np.random.rand(20, 20)

    ax1, ax2, ax3 = fig_test.subplots(1, 3)
    ax1.imshow(im_data1, origin="lower", interpolation="nearest")
    ax2.imshow(im_data2, origin="lower", interpolation="nearest")
    ax2.plot([i for i in range(10)])
    line = ax2.plot([i for i in range(10, 0, -1)])[0]
    view(ax3, ax1)
    ax3.set_xlim(0, 30)
    ax3.set_ylim(0, 30)
    ax3.set_aspect(1)

    # Assert all getters return default or set values...
    assert ax3.get_axes_to_view() is ax1
    assert ax3.get_image_interpolation() == "nearest"
    assert ax3.get_max_render_depth() == DEFAULT_RENDER_DEPTH
    assert ax3.get_linescaling() == True
    assert ax3.get_filter_function() is None

    # Attempt setting to different values...
    ax3.set_axes_to_view(ax2)
    # If this doesn't change pdf backend gets error > 5.6....
    ax3.set_image_interpolation("bicubic")
    ax3.set_max_render_depth(10)
    ax3.set_linescaling(False)
    ax3.set_filter_function(lambda a: a != line)

    # Compare against new thing...
    ax1, ax2, ax3 = fig_ref.subplots(1, 3)
    ax1.imshow(im_data1, origin="lower", interpolation="nearest")
    ax2.imshow(im_data2, origin="lower", interpolation="nearest")
    ax2.plot([i for i in range(10)])
    ax2.plot([i for i in range(10, 0, -1)])
    ax3.imshow(im_data2, origin="lower", interpolation="nearest")
    ax3.plot([i for i in range(10)])
    ax3.set_xlim(0, 30)
    ax3.set_ylim(0, 30)

@plotting_test()
def test_subplot_view_pickle(fig_test):
    np.random.seed(1)
    im_data = np.random.rand(30, 30)

    # Test case...
    ax_test1, ax_test2 = fig_test.subplots(1, 2)

    ax_test1.plot([i for i in range(10)], "r")
    ax_test1.add_patch(plt.Circle((3, 3), 1, ec="black", fc="blue"))
    ax_test1.text(10, 10, "Hello World!", size=14)
    ax_test1.imshow(im_data, origin="lower", cmap="Blues", alpha=0.5,
                   interpolation="nearest")
    ax_test2 = view(ax_test2, ax_test1)
    ax_test2.set_aspect(ax_test1.get_aspect())
    ax_test2.set_xlim(ax_test1.get_xlim())
    ax_test2.set_ylim(ax_test1.get_ylim())

    assert matches_post_pickle(fig_test)

@plotting_test()
def test_zoom_plot_pickle(fig_test):
    np.random.seed(1)
    im_data = np.random.rand(30, 30)
    arrow_s = dict(arrowstyle="->")

    # Test Case...
    ax_test = fig_test.gca()
    ax_test.plot([i for i in range(10)], "r")
    ax_test.add_patch(plt.Circle((3, 3), 1, ec="black", fc="blue"))
    ax_test.imshow(im_data, origin="lower", cmap="Blues", alpha=0.5,
                   interpolation="nearest")
    axins_test = inset_zoom_axes(ax_test, [0.5, 0.5, 0.48, 0.48])
    axins_test.set_linescaling(False)
    axins_test.set_xlim(1, 5)
    axins_test.set_ylim(1, 5)
    axins_test.annotate(
        "Interesting", (3, 3), (0, 0),
        textcoords="axes fraction", arrowprops=arrow_s
    )
    ax_test.indicate_inset_zoom(axins_test, edgecolor="black")

    assert matches_post_pickle(fig_test)

@plotting_test()
def test_3d_view_pickle(fig_test):
    X = Y = np.arange(-5, 5, 0.25)
    X, Y = np.meshgrid(X, Y)
    Z = np.sin(np.sqrt(X ** 2 + Y ** 2))

    ax1_test, ax2_test = fig_test.subplots(
        1, 2, subplot_kw=dict(projection="3d")
    )
    ax1_test.plot_surface(X, Y, Z, cmap="plasma")
    view(ax2_test, ax1_test)
    ax2_test.view_init(elev=80)
    ax2_test.set_xlim(-10, 10)
    ax2_test.set_ylim(-10, 10)
    ax2_test.set_zlim(-2, 2)

    assert matches_post_pickle(fig_test)