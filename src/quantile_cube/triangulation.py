"""
triangulation.py
----------------
Utilities for building the triangular grid used by the quantile cube heatmap.
"""

import numpy as np
from matplotlib.tri import Triangulation


def reorder_in_chunks(lst, chunk_size: int = 5) -> list:
    """
    Reorder a list by reversing the order of fixed-size chunks.

    This is used to rearrange quantile data so that it maps correctly
    onto the triangular heatmap grid (bottom-to-top row ordering).

    Parameters
    ----------
    lst : array-like
        The input list or array to reorder.
    chunk_size : int, optional
        Number of elements per chunk. Default is 5.

    Returns
    -------
    list
        The reordered list.
    """
    lst = list(lst)

    # List to hold the new order
    new_order = []

    # Iterate over the list in reverse chunks of size `chunk_size`
    for i in range(len(lst), 0, -chunk_size):
        # Get the current chunk of size `chunk_size`
        chunk = lst[max(0, i - chunk_size):i]

        # Prepend the chunk to the new order
        new_order.extend(chunk)
    return new_order


def triangulation_for_triheatmap(M: int, N: int) -> list:
    """
    Generate the four Triangulation objects (N, E, S, W) for an M x N heatmap
    where each cell is divided into four triangles.

    Parameters
    ----------
    M : int
        Number of columns in the grid.
    N : int
        Number of rows in the grid.

    Returns
    -------
    list of matplotlib.tri.Triangulation
        Four triangulations corresponding to the North, East, South, and West
        triangles of each cell.
    """
    # Vertex grid (cell corners) - Generates coordinate grids for the vertices 
    # of the squares that will be filled in the heatmap
    xv, yv = np.meshgrid(np.arange(-0.5, M), np.arange(-0.5, N))

    # Center grid (cell centers) - Generates coordinate grids for the centers 
    # of the squares that will be filled in the heatmap
    xc, yc = np.meshgrid(np.arange(0, M), np.arange(0, N))

    # Combines the x and y coordinates of the vertices and centers into single array
    x = np.concatenate([xv.ravel(), xc.ravel()])
    y = np.concatenate([yv.ravel(), yc.ravel()])

    cstart = (M + 1) * (N + 1)  # index where center points begin

    trianglesN = [
        (i + j * (M + 1), i + 1 + j * (M + 1), cstart + i + j * M)
        for j in range(N) for i in range(M)
    ]
    trianglesE = [
        (i + 1 + j * (M + 1), i + 1 + (j + 1) * (M + 1), cstart + i + j * M)
        for j in range(N) for i in range(M)
    ]
    trianglesS = [
        (i + 1 + (j + 1) * (M + 1), i + (j + 1) * (M + 1), cstart + i + j * M)
        for j in range(N) for i in range(M)
    ]
    trianglesW = [
        (i + (j + 1) * (M + 1), i + j * (M + 1), cstart + i + j * M)
        for j in range(N) for i in range(M)
    ]

    return [
        Triangulation(x, y, triangles)
        for triangles in [trianglesN, trianglesE, trianglesS, trianglesW]
    ]