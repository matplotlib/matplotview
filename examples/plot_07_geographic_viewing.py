"""
Viewing Geographic Projections
==============================

Matplotview also works with matplotlib's built in geographic projections.
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotview import view

x = np.linspace(-2.5, 2.5, 20)
y = np.linspace(-1, 1, 20)
circ_gen = lambda: plt.Circle((1.5, 0.25), 0.7, ec="black", fc="blue")

fig_test = plt.figure()

# Plot in 2 seperate geographic projections...
ax_t1 = fig_test.add_subplot(1, 2, 1, projection="hammer")
ax_t2 = fig_test.add_subplot(1, 2, 2, projection="lambert")

ax_t1.grid(True)
ax_t2.grid(True)

ax_t1.plot(x, y)
ax_t1.add_patch(circ_gen())

view(ax_t2, ax_t1)

fig_test.tight_layout()
fig_test.savefig("test7.png")
