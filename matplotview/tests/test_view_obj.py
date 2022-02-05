import matplotlib.pyplot as plt
import pickle
from matplotview import view, view_wrapper, inset_zoom_axes
import numpy as np

def to_image(figure):
    figure.canvas.draw()
    img = np.frombuffer(figure.canvas.tostring_rgb(), dtype=np.uint8)
    return img.reshape(figure.canvas.get_width_height()[::-1] + (3,))


def test_obj_comparison():
    from matplotlib.axes import Subplot, Axes

    view_class1 = view_wrapper(Subplot)
    view_class2 = view_wrapper(Subplot)
    view_class3 = view_wrapper(Axes)

    assert view_class1 is view_class2
    assert view_class1 == view_class2
    assert view_class2 != view_class3


def test_subplot_view_pickle():
    np.random.seed(1)
    im_data = np.random.rand(30, 30)

    # Test case...
    fig_test, (ax_test1, ax_test2) = plt.subplots(1, 2)

    ax_test1.plot([i for i in range(10)], "r")
    ax_test1.add_patch(plt.Circle((3, 3), 1, ec="black", fc="blue"))
    ax_test1.text(10, 10, "Hello World!", size=14)
    ax_test1.imshow(im_data, origin="lower", cmap="Blues", alpha=0.5,
                   interpolation="nearest")
    ax_test2 = view(ax_test2, ax_test1)
    ax_test2.set_aspect(ax_test1.get_aspect())
    ax_test2.set_xlim(ax_test1.get_xlim())
    ax_test2.set_ylim(ax_test1.get_ylim())

    img_expected = to_image(fig_test)

    saved_fig = pickle.dumps(fig_test)
    plt.clf()

    fig_test = pickle.loads(saved_fig)
    img_result = to_image(fig_test)

    assert np.all(img_expected == img_result)


def test_zoom_plot_pickle():
    np.random.seed(1)
    plt.clf()
    im_data = np.random.rand(30, 30)

    # Test Case...
    fig_test = plt.gcf()
    ax_test = fig_test.gca()
    ax_test.plot([i for i in range(10)], "r")
    ax_test.add_patch(plt.Circle((3, 3), 1, ec="black", fc="blue"))
    ax_test.imshow(im_data, origin="lower", cmap="Blues", alpha=0.5,
                   interpolation="nearest")
    axins_test = inset_zoom_axes(ax_test, [0.5, 0.5, 0.48, 0.48])
    axins_test.set_linescaling(False)
    axins_test.set_xlim(1, 5)
    axins_test.set_ylim(1, 5)
    ax_test.indicate_inset_zoom(axins_test, edgecolor="black")

    fig_test.savefig("before.png")
    img_expected = to_image(fig_test)

    saved_fig = pickle.dumps(fig_test)
    plt.clf()

    fig_test = pickle.loads(saved_fig)
    fig_test.savefig("after.png")
    img_result = to_image(fig_test)

    assert np.all(img_expected == img_result)