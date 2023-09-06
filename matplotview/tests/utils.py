import numpy as np
import matplotlib.pyplot as plt


def figure_to_image(figure):
    figure.canvas.draw()
    img = np.frombuffer(figure.canvas.buffer_rgba(), dtype=np.uint8)
    return img.reshape(figure.canvas.get_width_height()[::-1] + (4,))[..., :3]


def matches_post_pickle(figure):
    import pickle
    img_expected = figure_to_image(figure)

    saved_fig = pickle.dumps(figure)
    plt.close("all")

    figure = pickle.loads(saved_fig)
    img_result = figure_to_image(figure)

    return np.all(img_expected == img_result)


def plotting_test(num_figs=1, *args, **kwargs):
    def plotting_decorator(function):
        def test_plotting():
            plt.close("all")
            res = function(
                *(plt.figure(*args, **kwargs) for __ in range(num_figs))
            )
            plt.close("all")
            return res

        return test_plotting

    return plotting_decorator
