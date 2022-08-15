"""
Viewing Multiple Axes From A Single View
========================================

Views can view multiple axes at the same time, by simply calling :meth:`matplotview.view` multiple times.
"""
import matplotlib.pyplot as plt
from matplotview import view

fig, (ax1, ax2, ax3) = plt.subplots(1, 3)

# We'll plot 2 circles in axes 1 and 3.
ax1.add_patch(plt.Circle((1, 1), 1.5, ec="black", fc=(0, 0, 1, 0.5)))
ax3.add_patch(plt.Circle((3, 1), 1.5, ec="black", fc=(1, 0, 0, 0.5)))
for ax in (ax1, ax3):
        ax.set_aspect(1)
        ax.relim()
        ax.autoscale_view()

# Axes 2 is a view of 1 and 3 at the same time (view returns the axes it turns into a view...)
view(view(ax2, ax1), ax3)

# Change data limits, so we can see the entire 'venn diagram'
ax2.set_aspect(1)
ax2.set_xlim(-0.5, 4.5)
ax2.set_ylim(-0.5, 2.5)

fig.show()