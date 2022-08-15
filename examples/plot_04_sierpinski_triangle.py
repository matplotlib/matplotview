"""
Sierpiński Triangle With Recursive Views
========================================

Matplotview's views support recursive drawing of other views and themselves to a
configurable depth. This feature allows matplotview to be used to generate fractals,
such as a sierpiński triangle as shown in the following example.
"""

import matplotlib.pyplot as plt
import matplotview as mpv
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from matplotlib.transforms import Affine2D

# We'll plot a white upside down triangle inside of black one, and then use
# 3 views to draw all the rest of the recursions of the sierpiński triangle.
outside_color = "black"
inner_color = "white"

t = Affine2D().scale(-0.5)

outer_triangle = Path.unit_regular_polygon(3)
inner_triangle = t.transform_path(outer_triangle)
b = outer_triangle.get_extents()

fig, ax = plt.subplots(1)
ax.set_aspect(1)

ax.add_patch(PathPatch(outer_triangle, fc=outside_color, ec=[0] * 4))
ax.add_patch(PathPatch(inner_triangle, fc=inner_color, ec=[0] * 4))
ax.set_xlim(b.x0, b.x1)
ax.set_ylim(b.y0, b.y1)

ax_locs = [
    [0, 0, 0.5, 0.5],
    [0.5, 0, 0.5, 0.5],
    [0.25, 0.5, 0.5, 0.5]
]

for loc in ax_locs:
    # Here we limit the render depth to 6 levels in total for each zoom view....
    inax = mpv.inset_zoom_axes(ax, loc, render_depth=6)
    inax.set_xlim(b.x0, b.x1)
    inax.set_ylim(b.y0, b.y1)
    inax.axis("off")
    inax.patch.set_visible(False)

fig.show()