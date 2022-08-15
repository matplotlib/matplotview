The Simplest View
=================

The simplest example: We make a view of a line! Views can be created quickly
using :meth:`matplotview.view` .

.. plot::

    from matplotview import view
    import matplotlib.pyplot as plt
    import numpy as np

    fig, (ax1, ax2) = plt.subplots(1, 2)

    # Plot a line in the first axes.
    ax1.plot([i for i in range(10)], "-o")

    # Create a view! Turn axes 2 into a view of axes 1.
    view(ax2, ax1)
    # Modify the second axes data limits so we get a slightly zoomed out view
    ax2.set_xlim(-5, 15)
    ax2.set_ylim(-5, 15)

    fig.show()

