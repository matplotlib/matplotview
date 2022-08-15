"""
View With Annotations
=====================

Matplotview's views are also regular matplotlib `Axes <https://matplotlib.org/stable/api/axes_api.html#module-matplotlib.axes>`_,
meaning they support regular plotting on top of their viewing capabilities, allowing
for annotations, as shown below.
"""

# All the same as from the prior inset axes example...
from matplotlib import cbook
import matplotlib.pyplot as plt
import numpy as np
from matplotview import inset_zoom_axes


def get_demo_image():
    z = cbook.get_sample_data("axes_grid/bivariate_normal.npy", np_load=True)
    return z, (-3, 4, -4, 3)


fig, ax = plt.subplots()

Z, extent = get_demo_image()
Z2 = np.zeros((150, 150))
ny, nx = Z.shape
Z2[30:30 + ny, 30:30 + nx] = Z

ax.imshow(Z2, extent=extent, interpolation='nearest', origin="lower")

axins = inset_zoom_axes(ax, [0.5, 0.5, 0.47, 0.47])

x1, x2, y1, y2 = -1.5, -0.9, -2.5, -1.9
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)

# We'll annotate the 'interesting' spot in the view....
axins.annotate(
    "Interesting Feature", (-1.3, -2.25), (0.1, 0.1),
    textcoords="axes fraction", arrowprops=dict(arrowstyle="->")
)

axins.set_xticklabels([])
axins.set_yticklabels([])

ax.indicate_inset_zoom(axins, edgecolor="black")

fig.show()