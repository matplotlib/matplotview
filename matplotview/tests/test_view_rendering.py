import numpy as np
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import check_figures_equal
from matplotview import view, inset_zoom_axes, stop_viewing


@check_figures_equal(tol=6)
def test_double_plot(fig_test, fig_ref):
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

    # Reference...
    ax_ref1, ax_ref2 = fig_ref.subplots(1, 2)

    ax_ref1.plot([i for i in range(10)], "r")
    ax_ref1.add_patch(plt.Circle((3, 3), 1, ec="black", fc="blue"))
    ax_ref1.text(10, 10, "Hello World!", size=14)
    ax_ref1.imshow(im_data, origin="lower", cmap="Blues", alpha=0.5,
                   interpolation="nearest")
    ax_ref2.plot([i for i in range(10)], "r")
    ax_ref2.add_patch(plt.Circle((3, 3), 1, ec="black", fc="blue"))
    ax_ref2.text(10, 10, "Hello World!", size=14)
    ax_ref2.imshow(im_data, origin="lower", cmap="Blues", alpha=0.5,
                   interpolation="nearest")


# Tolerance needed because the way the auto-zoom axes handles images is
# entirely different, leading to a slightly different result.
@check_figures_equal(tol=3.5)
def test_auto_zoom_inset(fig_test, fig_ref):
    np.random.seed(1)
    im_data = np.random.rand(30, 30)

    # Test Case...
    ax_test = fig_test.gca()
    ax_test.plot([i for i in range(10)], "r")
    ax_test.add_patch(plt.Circle((3, 3), 1, ec="black", fc="blue"))
    ax_test.imshow(im_data, origin="lower", cmap="Blues", alpha=0.5,
                   interpolation="nearest")
    axins_test = inset_zoom_axes(ax_test, [0.5, 0.5, 0.48, 0.48],
                                 scale_lines=False)
    axins_test.set_xlim(1, 5)
    axins_test.set_ylim(1, 5)
    ax_test.indicate_inset_zoom(axins_test, edgecolor="black")

    # Reference
    ax_ref = fig_ref.gca()
    ax_ref.plot([i for i in range(10)], "r")
    ax_ref.add_patch(plt.Circle((3, 3), 1, ec="black", fc="blue"))
    ax_ref.imshow(im_data, origin="lower", cmap="Blues", alpha=0.5,
                  interpolation="nearest")
    axins_ref = ax_ref.inset_axes([0.5, 0.5, 0.48, 0.48])
    axins_ref.set_xlim(1, 5)
    axins_ref.set_ylim(1, 5)
    axins_ref.plot([i for i in range(10)], "r")
    axins_ref.add_patch(plt.Circle((3, 3), 1, ec="black", fc="blue"))
    axins_ref.imshow(im_data, origin="lower", cmap="Blues", alpha=0.5,
                     interpolation="nearest")
    ax_ref.indicate_inset_zoom(axins_ref, edgecolor="black")


@check_figures_equal(tol=3.5)
def test_plotting_in_view(fig_test, fig_ref):
    np.random.seed(1)
    im_data = np.random.rand(30, 30)
    arrow_s = dict(arrowstyle="->")

    # Test Case...
    ax_test = fig_test.gca()
    ax_test.imshow(im_data, origin="lower", cmap="Blues", alpha=0.5,
                   interpolation="nearest")
    axins_test = inset_zoom_axes(ax_test, [0.5, 0.5, 0.48, 0.48],
                                 scale_lines=False)
    axins_test.set_xlim(1, 5)
    axins_test.set_ylim(1, 5)
    axins_test.annotate(
        "Interesting", (3, 3), (0, 0),
        textcoords="axes fraction", arrowprops=arrow_s
    )
    ax_test.indicate_inset_zoom(axins_test, edgecolor="black")

    # Reference
    ax_ref = fig_ref.gca()
    ax_ref.imshow(im_data, origin="lower", cmap="Blues", alpha=0.5,
                  interpolation="nearest")
    axins_ref = ax_ref.inset_axes([0.5, 0.5, 0.48, 0.48])
    axins_ref.set_xlim(1, 5)
    axins_ref.set_ylim(1, 5)
    axins_ref.imshow(im_data, origin="lower", cmap="Blues", alpha=0.5,
                     interpolation="nearest")
    axins_ref.annotate(
        "Interesting", (3, 3), (0, 0),
        textcoords="axes fraction", arrowprops=arrow_s
    )
    ax_ref.indicate_inset_zoom(axins_ref, edgecolor="black")


@check_figures_equal()
def test_3d_view(fig_test, fig_ref):
    # The data...
    X = Y = np.arange(-5, 5, 0.25)
    X, Y = np.meshgrid(X, Y)
    Z = np.sin(np.sqrt(X ** 2 + Y ** 2))

    # Test Case...
    ax1_test, ax2_test = fig_test.subplots(
        1, 2, subplot_kw=dict(projection="3d")
    )
    ax1_test.plot_surface(X, Y, Z, cmap="plasma")
    view(ax2_test, ax1_test)
    ax2_test.view_init(elev=80)
    ax2_test.set_xlim(-10, 10)
    ax2_test.set_ylim(-10, 10)
    ax2_test.set_zlim(-2, 2)

    # Reference
    ax1_ref, ax2_ref = fig_ref.subplots(
        1, 2, subplot_kw=dict(projection="3d")
    )
    ax1_ref.plot_surface(X, Y, Z, cmap="plasma")
    ax2_ref.plot_surface(X, Y, Z, cmap="plasma")
    ax2_ref.view_init(elev=80)
    ax2_ref.set_xlim(-10, 10)
    ax2_ref.set_ylim(-10, 10)
    ax2_ref.set_zlim(-2, 2)


@check_figures_equal()
def test_polar_view(fig_test, fig_ref):
    r = np.arange(0, 2, 0.01)
    theta = 2 * np.pi * r

    # Test Case with polar coordinate system...
    ax_t1, ax_t2 = fig_test.subplots(1, 2, subplot_kw=dict(projection="polar"))
    ax_t1.plot(theta, r)
    ax_t1.set_rmax(2)
    view(ax_t2, ax_t1, scale_lines=False)
    ax_t2.set_rmax(1)

    # Reference...
    ax_r1, ax_r2 = fig_ref.subplots(1, 2, subplot_kw=dict(projection="polar"))
    ax_r1.plot(theta, r)
    ax_r1.set_rmax(2)
    ax_r2.plot(theta, r)
    ax_r2.set_rmax(1)


@check_figures_equal()
def test_map_projection_view(fig_test, fig_ref):
    x = np.linspace(-2.5, 2.5, 20)
    y = np.linspace(-1, 1, 20)

    def circ_gen():
        return plt.Circle((1.5, 0.25), 0.7, ec="black", fc="blue")

    # Test case...
    ax_t1 = fig_test.add_subplot(1, 2, 1, projection="hammer")
    ax_t2 = fig_test.add_subplot(1, 2, 2, projection="lambert")
    ax_t1.grid(True)
    ax_t2.grid(True)
    ax_t1.plot(x, y)
    ax_t1.add_patch(circ_gen())
    view(ax_t2, ax_t1)

    # Reference...
    ax_r1 = fig_ref.add_subplot(1, 2, 1, projection="hammer")
    ax_r2 = fig_ref.add_subplot(1, 2, 2, projection="lambert")
    ax_r1.grid(True)
    ax_r2.grid(True)
    ax_r1.plot(x, y)
    ax_r1.add_patch(circ_gen())
    ax_r2.plot(x, y)
    ax_r2.add_patch(circ_gen())


@check_figures_equal()
def test_double_view(fig_test, fig_ref):
    # Test case...
    ax_test1, ax_test2, ax_test3 = fig_test.subplots(1, 3)

    ax_test1.add_patch(plt.Circle((1, 1), 1.5, ec="black", fc=(0, 0, 1, 0.5)))
    ax_test3.add_patch(plt.Circle((3, 1), 1.5, ec="black", fc=(1, 0, 0, 0.5)))

    ax_test2 = view(
        view(ax_test2, ax_test1, scale_lines=False),
        ax_test3, scale_lines=False
    )

    ax_test2.set_aspect(1)
    ax_test2.set_xlim(-0.5, 4.5)
    ax_test2.set_ylim(-0.5, 2.5)

    # Reference...
    ax_ref1, ax_ref2, ax_ref3 = fig_ref.subplots(1, 3)

    ax_ref1.add_patch(plt.Circle((1, 1), 1.5, ec="black", fc=(0, 0, 1, 0.5)))
    ax_ref3.add_patch(plt.Circle((3, 1), 1.5, ec="black", fc=(1, 0, 0, 0.5)))

    ax_ref2.add_patch(plt.Circle((1, 1), 1.5, ec="black", fc=(0, 0, 1, 0.5)))
    ax_ref2.add_patch(plt.Circle((3, 1), 1.5, ec="black", fc=(1, 0, 0, 0.5)))
    ax_ref2.set_aspect(1)
    ax_ref2.set_xlim(-0.5, 4.5)
    ax_ref2.set_ylim(-0.5, 2.5)

    for ax in (ax_test1, ax_test3, ax_ref1, ax_ref3):
        ax.set_aspect(1)
        ax.relim()
        ax.autoscale_view()


@check_figures_equal()
def test_stop_viewing(fig_test, fig_ref):
    np.random.seed(1)
    data = np.random.randint(0, 10, 10)

    # Test case... Create a view and stop it...
    ax1_test, ax2_test = fig_test.subplots(1, 2)

    ax1_test.plot(data)
    ax1_test.text(0.5, 0.5, "Hello")

    view(ax2_test, ax1_test)
    stop_viewing(ax2_test, ax1_test)

    # Reference, just don't plot anything at all in the second axes...
    ax1_ref, ax2_ref = fig_ref.subplots(1, 2)

    ax1_ref.plot(data)
    ax1_ref.text(0.5, 0.5, "Hello")


@check_figures_equal()
def test_log_line(fig_test, fig_ref):
    data = [i for i in range(1, 10)]

    # Test case... Create a view and stop it...
    ax1_test, ax2_test = fig_test.subplots(1, 2)

    ax1_test.set(xscale="log", yscale="log")
    ax1_test.plot(data, "-o")

    view(ax2_test, ax1_test, scale_lines=False)
    ax2_test.set_xlim(-1, 10)
    ax2_test.set_ylim(-1, 10)

    # Reference, just don't plot anything at all in the second axes...
    ax1_ref, ax2_ref = fig_ref.subplots(1, 2)

    ax1_ref.set(xscale="log", yscale="log")
    ax1_ref.plot(data, "-o")
    ax2_ref.plot(data, "-o")
    ax2_ref.set_xlim(-1, 10)
    ax2_ref.set_ylim(-1, 10)


@check_figures_equal()
def test_log_scatter(fig_test, fig_ref):
    data = [i for i in range(1, 11)]

    # Test case... Create a view and stop it...
    ax1_test, ax2_test = fig_test.subplots(1, 2)

    ax1_test.set(xscale="log", yscale="log")
    ax1_test.scatter(data, data)

    view(ax2_test, ax1_test, scale_lines=False)
    ax2_test.set_xlim(-5, 15)
    ax2_test.set_ylim(-5, 15)

    # Reference, just don't plot anything at all in the second axes...
    ax1_ref, ax2_ref = fig_ref.subplots(1, 2)

    ax1_ref.set(xscale="log", yscale="log")
    ax1_ref.scatter(data, data)
    ax2_ref.scatter(data, data)
    ax2_ref.set_xlim(-5, 15)
    ax2_ref.set_ylim(-5, 15)


@check_figures_equal()
def test_log_scatter_with_colors(fig_test, fig_ref):
    data = [i for i in range(1, 11)]
    colors = list("rgbrgbrgbr")

    # Test case... Create a view and stop it...
    ax1_test, ax2_test = fig_test.subplots(1, 2)

    ax1_test.set(xscale="log", yscale="log")
    ax1_test.scatter(data, data, color=colors)

    view(ax2_test, ax1_test, scale_lines=False)
    ax2_test.set_xlim(-5, 15)
    ax2_test.set_ylim(-5, 15)

    # Reference, just don't plot anything at all in the second axes...
    ax1_ref, ax2_ref = fig_ref.subplots(1, 2)

    ax1_ref.set(xscale="log", yscale="log")
    ax1_ref.scatter(data, data, color=colors)
    ax2_ref.scatter(data, data, color=colors)
    ax2_ref.set_xlim(-5, 15)
    ax2_ref.set_ylim(-5, 15)
