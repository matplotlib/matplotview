Create Inset Axes Without Plotting Twice
========================================

:meth:`matplotview.inset_zoom_axes` can be utilized to create inset axes where we
don't have to plot the parent axes data twice.

.. plot::

    from matplotlib import cbook
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotview import inset_zoom_axes

    def get_demo_image():
        z = cbook.get_sample_data("axes_grid/bivariate_normal.npy", np_load=True)
        # z is a numpy array of 15x15
        return z, (-3, 4, -4, 3)

    fig, ax = plt.subplots()

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

    # Remove the tick labels from the inset axes
    axins.set_xticklabels([])
    axins.set_yticklabels([])

    # Draw the indicator or zoom lines.
    ax.indicate_inset_zoom(axins, edgecolor="black")

    fig.show()


