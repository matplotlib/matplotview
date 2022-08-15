"""
Viewing Polar Axes
==================

Views also support viewing polar axes.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotview import view

# Create the data...
r = np.arange(0, 2, 0.01)
theta = 2 * np.pi * r

fig, (ax, ax2) = plt.subplots(1, 2, subplot_kw=dict(projection='polar'))

ax.plot(theta, r)
ax.set_rmax(2)
ax.set_rticks([0.5, 1, 1.5, 2])  # Less radial ticks
ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
# Include a grid
ax.grid(True)

# ax2 is now zoomed in on ax.
view(ax2, ax)

fig.tight_layout()

fig.show()