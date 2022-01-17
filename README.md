# matplotview
#### A library for creating lightweight views of matplotlib axes.

matplotview provides a simple interface for creating "views" of matplotlib
axes, providing a simple way of displaying overviews and zoomed views of 
data without plotting data twice.

## Usage

matplotview provides two methods, `view`, and `inset_zoom_axes`. The `view`
method accepts two `Axes`, and makes the first axes a view of the second. The
`inset_zoom_axes` method provides the same functionality as `Axes.inset_axes`,
but the returned inset axes is configured to be a view of the parent axes.

## Examples

An example of two axes showing the same plot.
```python
from matplotview import view
import matplotlib.pyplot as plt
import numpy as np

fig, (ax1, ax2) = plt.subplots(1, 2)

# Plot a line, circle patch, some text, and an image...
ax1.plot([i for i in range(10)], "r")
ax1.add_patch(plt.Circle((3, 3), 1, ec="black", fc="blue"))
ax1.text(10, 10, "Hello World!", size=20)
ax1.imshow(np.random.rand(30, 30), origin="lower", cmap="Blues", alpha=0.5,
           interpolation="nearest")

# Turn axes 2 into a view of axes 1.
view(ax2, ax1)
# Modify the second axes data limits to match the first axes...
ax2.set_aspect(ax1.get_aspect())
ax2.set_xlim(ax1.get_xlim())
ax2.set_ylim(ax1.get_ylim())

fig.tight_layout()
fig.show()
```
![First example plot results, two views of the same plot.](https://user-images.githubusercontent.com/47544550/149814592-dd815f95-c3ef-406d-bd7e-504859c836bf.png)

An inset axes example .
```python
from matplotlib import cbook
import matplotlib.pyplot as plt
import numpy as np
from matplotview import inset_zoom_axes

def get_demo_image():
    z = cbook.get_sample_data("axes_grid/bivariate_normal.npy", np_load=True)
    # z is a numpy array of 15x15
    return z, (-3, 4, -4, 3)

fig, ax = plt.subplots(figsize=[5, 4])

# Make the data...
Z, extent = get_demo_image()
Z2 = np.zeros((150, 150))
ny, nx = Z.shape
Z2[30:30+ny, 30:30+nx] = Z

ax.imshow(Z2, extent=extent, interpolation='nearest', origin="lower")

# Creates an inset axes with automatic view of the parent axes...
axins = inset_zoom_axes(ax, [0.5, 0.5, 0.47, 0.47])
# Set limits to sub region of the original image
x1, x2, y1, y2 = -1.5, -0.9, -2.5, -1.9
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
axins.set_xticklabels([])
axins.set_yticklabels([])

ax.indicate_inset_zoom(axins, edgecolor="black")

fig.show()
```
![Second example plot results, an inset axes showing a zoom view of an image.](https://user-images.githubusercontent.com/47544550/149814558-c2b1228d-2e5d-41be-86c0-f5dd01d42884.png)