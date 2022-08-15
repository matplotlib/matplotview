"""
Filtering Artists in a View
===========================

:meth:`matplotview.view` supports filtering out artist instances and types using the `filter_set` parameter,
which accepts an iterable of artists types and instances.
"""
import matplotlib.pyplot as plt
from matplotview import view

fig, (ax1, ax2, ax3) = plt.subplots(3, 1)

# Plot a line, circle patch, and some text in axes 1
ax1.set_title("Original Plot")
ax1.plot([(i / 10) for i in range(10)], [(i / 10) for i in range(10)], "r")
ax1.add_patch(plt.Circle((0.5, 0.5), 0.25, ec="black", fc="blue"))
text = ax1.text(0.2, 0.2, "Hello World!", size=12)

# Axes 2 is viewing axes 1, but filtering circles...
ax2.set_title("View Filtering Out Circles")
view(ax2, ax1, filter_set=[plt.Circle])  # We can pass artist types
ax2.set_xlim(ax1.get_xlim())
ax2.set_ylim(ax1.get_ylim())

# Axes 3 is viewing axes 1, but filtering the text artist
ax3.set_title("View Filtering Out Just the Text Artist.")
view(ax3, ax1, filter_set=[text])  # We can also pass artist instances...
ax3.set_xlim(ax1.get_xlim())
ax3.set_ylim(ax1.get_ylim())

fig.tight_layout()
fig.show()