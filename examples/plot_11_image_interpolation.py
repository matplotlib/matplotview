"""
Image Interpolation Methods
===========================

:meth:`matplotview.view` and :meth:`matplotview.inset_zoom_axes` support specifying an
image interpolation method via the `image_interpolation` parameter. This image interpolation
method is used to resize images when displaying them in the view.
"""
import matplotlib.pyplot as plt
from matplotview import view
import numpy as np

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

fig.suptitle("Different interpolations when zoomed in on the bottom left corner.")

ax1.set_title("Original")
ax1.imshow(np.random.rand(100, 100), cmap="Blues", origin="lower")
ax1.add_patch(plt.Rectangle((0, 0), 10, 10, ec="red", fc=(0, 0, 0, 0)))

for ax, interpolation, title in zip([ax2, ax3, ax4], ["nearest", "bilinear", "bicubic"], ["Nearest (Default)", "Bilinear", "Cubic"]):
    ax.set_title(title)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect("equal")
    view(ax, ax1, image_interpolation=interpolation)

fig.tight_layout()
fig.show()

#%%
# If you want to avoid interpolation artifacts, you can use `pcolormesh` instead of `imshow`.

import matplotlib.pyplot as plt
from matplotview import view
import numpy as np

fig, (ax1, ax2) = plt.subplots(1, 2)

ax1.set_title("Original")
ax1.pcolormesh(np.random.rand(100, 100), cmap="Blues")
ax1.add_patch(plt.Rectangle((0, 0), 10, 10, ec="red", fc=(0, 0, 0, 0)))
ax1.set_aspect("equal")

ax2.set_title("Zoomed in View")
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.set_aspect("equal")
view(ax2, ax1)

fig.tight_layout()
fig.show()