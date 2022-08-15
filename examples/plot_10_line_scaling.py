"""
Disabling Line Scaling
======================

By default, matplotview scales the line thickness settings for lines and markers to match the zoom level.
This can be disabled via the `scale_lines` parameter of :meth:`matplotview.view`.
"""
import matplotlib.pyplot as plt
from matplotview import view

fig, (ax1, ax2, ax3) = plt.subplots(3, 1)

# Plot a line, and circle patch in axes 1
ax1.set_title("Original Plot")
ax1.plot([(i / 10) for i in range(10)], [(i / 10) for i in range(10)], "r-")
ax1.add_patch(plt.Circle((0.5, 0.5), 0.1, ec="black", fc="blue"))

ax2.set_title("Zoom View With Line Scaling")
view(ax2, ax1, scale_lines=True)  # Default, line scaling is ON
ax2.set_xlim(0.33, 0.66)
ax2.set_ylim(0.33, 0.66)

ax3.set_title("Zoom View Without Line Scaling")
view(ax3, ax1, scale_lines=False)  # Line scaling is OFF
ax3.set_xlim(0.33, 0.66)
ax3.set_ylim(0.33, 0.66)

fig.tight_layout()
fig.show()