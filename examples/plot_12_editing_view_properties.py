"""
Editing View Properties
=======================

A view's properties can be edited by simply calling :meth:`matplotview.view` with the same axes arguments.
To stop a viewing, :meth:`matplotview.stop_viewing` can be used.
"""
import matplotlib.pyplot as plt
from matplotview import view, stop_viewing

fig, (ax1, ax2, ax3) = plt.subplots(3, 1)

# Plot a line, and circle patch in axes 1
ax1.set_title("Original Plot")
ax1.plot([(i / 10) for i in range(10)], [(i / 10) for i in range(10)], "r-")
ax1.add_patch(plt.Circle((0.5, 0.5), 0.1, ec="black", fc="blue"))

ax2.set_title("An Edited View")
# Ask ax2 to view ax1.
view(ax2, ax1, filter_set=[plt.Circle])
ax2.set_xlim(0.33, 0.66)
ax2.set_ylim(0.33, 0.66)

# Does not create a new view as ax2 is already viewing ax1.
# Edit ax2's viewing of ax1, remove filtering and disable line scaling.
view(ax2, ax1, filter_set=None, scale_lines=False)

ax3.set_title("A Stopped View")
view(ax3, ax1)  # Ask ax3 to view ax1.
ax3.set_xlim(0.33, 0.66)
ax3.set_ylim(0.33, 0.66)

# This makes ax3 stop viewing ax1.
stop_viewing(ax3, ax1)

fig.tight_layout()
fig.show()