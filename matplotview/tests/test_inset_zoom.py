import numpy as np
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import check_figures_equal
from matplotview import view, inset_zoom_axes

# Tolerance needed because the way the auto-zoom axes handles images is
# entirely different, leading to a slightly different result.
@check_figures_equal(tol=3)
def test_auto_zoom_inset(fig_test, fig_ref):
    np.random.seed(1)
    im_data = np.random.rand(30, 30)

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

