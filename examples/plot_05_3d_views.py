"""
Viewing 3D Axes
===============

Matplotview has built-in support for viewing 3D axes and plots.
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotview import view

X = Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
Z = np.sin(np.sqrt(X ** 2 + Y ** 2))

# Make some 3D plots...
fig, (ax1, ax2) = plt.subplots(1, 2, subplot_kw=dict(projection="3d"))

# Plot our surface
ax1.plot_surface(X, Y, Z, cmap="plasma")

# Axes 2 is now viewing axes 1.
view(ax2, ax1)

# Update the limits, and set the elevation higher, so we get a better view of the inside of the surface.
ax2.view_init(elev=80)
ax2.set_xlim(-10, 10)
ax2.set_ylim(-10, 10)
ax2.set_zlim(-2, 2)

fig.show()