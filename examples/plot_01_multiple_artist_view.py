"""
A View With Several Plot Elements
=================================

A simple example with an assortment of plot elements.
"""

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