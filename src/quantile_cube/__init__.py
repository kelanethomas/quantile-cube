"""
quantile_cube
-------------
A Python package for visualizing quantile distributions as triangular heatmaps.

Each cell in the grid is divided into four triangles (N, E, S, W), one per
quantile, allowing comparison of four distributions across a 2D parameter space.

Basic usage
-----------
Using raw arrays::

    from quantile_cube import plot_cube
    import numpy as np

    q1 = np.random.rand(25)
    q2 = np.random.rand(25)
    q3 = np.random.rand(25)
    q4 = np.random.rand(25)

    plot_cube(values=[q1, q2, q3, q4], M=5, N=5, title="My Quantile Cube")

Using a DataFrame (legacy format)::

    from quantile_cube import plot_cube

    plot_cube(cube_data=df, value_prefix="angle", M=5, N=5)

Public API
----------
"""

from .plot import plot_cube
from .triangulation import triangulation_for_triheatmap, reorder_in_chunks
from .labels import add_value_labels, add_quantile_labels

__all__ = [
    "plot_cube",
    "triangulation_for_triheatmap",
    "reorder_in_chunks",
    "add_value_labels",
    "add_quantile_labels",
]

__version__ = "0.1.3"