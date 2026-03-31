"""
labels.py
---------
Functions for adding text annotations to quantile cube plots.
"""

import numpy as np


def add_value_labels(ax, triangulation, values, fmt: str = ".4f", fontsize: int = 8, color: str = "black"):
    """
    Add numeric value labels at the centroid of each triangle.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axes to annotate.
    triangulation : matplotlib.tri.Triangulation
        The triangulation object whose triangles will be labeled.
    values : array-like
        Values to display, one per triangle.
    fmt : str, optional
        Format string for the numeric values. Default is ".4f".
    fontsize : int, optional
        Font size for the labels. Default is 8.
    color : str, optional
        Text color. Default is "black".
    """
    # Loop over the triangles and add labels at the triangle centers
    for tri, val in zip(triangulation.triangles, np.ravel(values)):
        # Calculate the center of each triangle
        x = triangulation.x[tri].mean()
        y = triangulation.y[tri].mean()
        # Add the text label
        ax.text(x, y, f"{val:{fmt}}", ha="center", va="center", fontsize=fontsize, color=color)


def add_quantile_labels(ax, triangulation, label: str, fontsize: int = 14, color: str = "black"):
    """
    Add a single repeated text label at the centroid of each triangle.

    Useful for annotating each triangular region with its quantile name
    (e.g. "Q1", "Q2") rather than a numeric value.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axes to annotate.
    triangulation : matplotlib.tri.Triangulation
        The triangulation whose triangles will be labeled.
    label : str
        The text label to place at each triangle centroid.
    fontsize : int, optional
        Font size. Default is 14.
    color : str, optional
        Text color. Default is "black".
    """
    # Compute the centroid of each triangle for positioning the labels
    centroids = np.column_stack((
        triangulation.x[triangulation.triangles].mean(axis=1),
        triangulation.y[triangulation.triangles].mean(axis=1),
    ))
    # Add the label at each centroid
    for (x, y) in centroids:
        ax.text(x, y, label, ha="center", va="center", fontsize=fontsize, color=color)