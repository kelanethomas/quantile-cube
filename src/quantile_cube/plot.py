"""
plot.py
-------
Main plotting function for the quantile cube heatmap.
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from .triangulation import triangulation_for_triheatmap
from .labels import add_value_labels, add_quantile_labels

def reorder_in_chunks(lst, chunk_size=5):
    # List to hold the new order
    new_order = []
    
    # Iterate over the list in reverse chunks of size `chunk_size`
    for i in range(len(lst), 0, -chunk_size):
        # Get the current chunk of size `chunk_size`
        chunk = lst[max(0, i - chunk_size):i]
        
        # Prepend the chunk to the new order
        new_order.extend(chunk)
    
    return new_order 

def plot_cube(
    # --- Data input: provide EITHER `values` OR `cube_data` ---
    values: list | None = None,
    cube_data=None,
    # --- Grid dimensions ---
    M: int = 5,
    N: int = 5,
    # --- Color scaling ---
    minimum: float | None = None,
    maximum: float | None = None,
    cmap=None,
    # --- Labels and titles ---
    title: str = "Quantile Cube",
    colorbar_label: str = "",
    xlabel: str = "Velocity",
    ylabel: str = "Acceleration",
    quantile_labels: list[str] | None = None,
    show_quantile_labels: bool = False,
    show_values: bool = False,
    value_fmt: str = ".4f",
    # --- Display options ---
    grey_nonsignificant: bool = False,
    save: bool = False,
    save_path: str | None = None,
    show: bool = True,
    figsize: tuple = (7, 7),
) -> plt.Figure:
    """
    Plot a quantile cube: an M x N heatmap where each cell is divided into
    four triangles representing four quantile values.

    Data Input
    ----------
    Provide data using **one** of the two options below:

    Option 1 — raw arrays (recommended for general use):
        Pass a list of exactly 4 array-like objects, one per quantile (Q1–Q4).
        Each array should have M * N values.

        Example::

            plot_cube(values=[q1_arr, q2_arr, q3_arr, q4_arr], M=5, N=5)

    Option 2 — DataFrame:
        Pass a single-row DataFrame whose columns are named:
        ``Q{vel}_vel_Q{acc}_acc_Q{angle}_angle``

        For example: ``Q1_vel_Q1_acc_Q1_angle``, ``Q2_vel_Q1_acc_Q3_angle``, etc.
        The vel and acc quantile indices determine the grid cell; the angle
        quantile index (1–4) determines which triangle within that cell.

        Example::

            plot_cube(cube_data=df, M=5, N=5)

    Parameters
    ----------
    values : list of array-like, optional
        List of 4 arrays [Q1, Q2, Q3, Q4], each of length M * N.
    cube_data : pandas.DataFrame, optional
        Single-row DataFrame with columns named ``<value_prefix>_Q1_*``, etc.
    value_prefix : str, optional
        Column prefix used when reading from ``cube_data``. Default is "angle".
    M : int
        Number of columns (x-axis quantile bins). Default is 5.
    N : int
        Number of rows (y-axis quantile bins). Default is 5.
    minimum : float, optional
        Minimum value for colormap normalization. Defaults to 0.
    maximum : float, optional
        Maximum value for colormap normalization. Defaults to the data max
        rounded up to the nearest 0.01 (e.g. 0.087 → 0.09).
    cmap : str or matplotlib Colormap, optional
        Colormap to use. Defaults to "viridis".
    title : str, optional
        Plot title and default save filename. Default is "Quantile Cube".
    colorbar_label : str, optional
        Label for the colorbar. Default is "".
    xlabel : str, optional
        X-axis label. Default is "Velocity".
    ylabel : str, optional
        Y-axis label. Default is "Acceleration".
    quantile_labels : list of str, optional
        Four labels for the triangles [N, E, S, W]. Defaults to
        ["Angle Q1", "Angle Q2", "Angle Q3", "Angle Q4"]
    show_quantile_labels : bool, optional
        If True, display a single-cell summary view with quantile labels
        instead of the full grid. Default is False.
    show_values : bool, optional
        If True, print the numeric value at the center of each triangle.
        Default is False.
    value_fmt : str, optional
        Format string for numeric labels when ``show_values=True``.
        Default is ".4f".
    grey_nonsignificant : bool, optional
        If True, NaN values are rendered in grey with a legend entry labeled
        "Non-significant Coefficient". Default is False.
    save : bool, optional
        If True, save the figure to a file. Default is False.
    save_path : str, optional
        File path for saving. Defaults to ``"<title>.png"`` in the
        current directory.
    show : bool, optional
        If True, call ``plt.show()``. Default is True.
    figsize : tuple, optional
        Figure size as (width, height) in inches. Default is (7, 7).

    Returns
    -------
    matplotlib.figure.Figure
        The generated figure.

    Raises
    ------
    ValueError
        If neither ``values`` nor ``cube_data`` is provided, or if ``values``
        does not contain exactly 4 arrays.
    """
    # Colormap Handling 
    if cmap is None:
        cmap = plt.get_cmap("Reds")
    elif isinstance(cmap, str):
        cmap = plt.get_cmap(cmap)

    # Default Labels for Angle Quantiles 
    if quantile_labels is None:
        quantile_labels = ["Angle Q1", "Angle Q2", "Angle Q3", "Angle Q4"]
    if len(quantile_labels) != 4:
        raise ValueError("quantile_labels must contain exactly 4 strings.")

    # Resolve data input
    if values is not None:
        if len(values) != 4:
            raise ValueError("values must be a list of exactly 4 arrays (one per quantile).")
        q1, q2, q3, q4 = [np.asarray(v, dtype=float) for v in values]

    elif cube_data is not None:
        q1 = np.asarray(reorder_in_chunks(cube_data.filter(like="Q1_angle").iloc[0].values, M),
                        dtype=float)
        q2 = np.asarray(reorder_in_chunks(cube_data.filter(like="Q2_angle").iloc[0].values, M),
                        dtype=float)
        q3 = np.asarray(reorder_in_chunks(cube_data.filter(like="Q3_angle").iloc[0].values, M),
                        dtype=float)
        q4 = np.asarray(reorder_in_chunks(cube_data.filter(like="Q4_angle").iloc[0].values, M),
                        dtype=float)

    else:
        raise ValueError(
            "Provide either values=[q1,q2,q3,q4] "
            "or cube_data=DataFrame."
        )

    # Summary Mode: Show one cell with four labeled triangles
    if show_quantile_labels:
        plot_values = [
            q1[-M],
            q2[-M],
            q3[-M],
            q4[-M],
        ]
        plot_M, plot_N = 1, 1

    else:
        # Full grid mode
        plot_values = [q1, q2, q3, q4]
        plot_M, plot_N = M, N

    # Color Normalization
    if minimum is None:
        minimum = 0.0

    if maximum is None:

        # Use data max rounded upward to nearest hundredth
        all_vals = np.concatenate(
            [np.ravel(v) for v in plot_values]
        )

        raw_max = np.nanmax(all_vals)
        maximum = np.ceil(raw_max * 100) / 100
    
    norm = plt.Normalize(minimum, maximum)

    # Build triangulations for N/E/S/W triangles in each square
    triangul = triangulation_for_triheatmap( plot_M, plot_N)

    fig, ax = plt.subplots(figsize=figsize)

    if grey_nonsignificant:
        import copy
        grey_cmap = copy.copy(cmap)

        # NaN values appear gray
        grey_cmap.set_bad(color="gray")

        # Mask NaN values
        masked_values = [np.ma.masked_invalid(np.ravel(v)) for v in plot_values]

        # Draw each quantile layer
        imgs = [
            ax.tripcolor(t, mv, cmap=grey_cmap, norm=norm, ec="white")
            for t, mv in zip(triangul, masked_values)
        ]

        # Add legend for gray cells
        nan_patch = mpatches.Patch(color="gray", label="Non-significant Coefficient")

        ax.legend(handles=[nan_patch], loc="upper left", bbox_to_anchor=(0.2, -0.16))

    else:
        # Standard rendering
        imgs = [
            ax.tripcolor(t, np.ravel(val), cmap=cmap, norm=norm, ec="white")
            for t, val in zip(triangul, plot_values)
        ]

    # Add numeric labels to triangle centers
    if show_values:
        for t, val in zip(triangul, plot_values):
            add_value_labels(ax, t, val, fmt=value_fmt)

    # Colorbar
    cbar = plt.colorbar(imgs[0], ax=ax)
    cbar.set_label(colorbar_label)

    # Axis ticks
    ax.set_xticks(range(plot_M))
    ax.set_yticks(range(plot_N))
    ax.set_xlabel(xlabel, fontsize=18)
    ax.set_ylabel(ylabel, fontsize=18)

    if show_quantile_labels:
        ax.set_xticklabels(["Q1"], fontsize=14)
        ax.set_yticklabels(["Q1"], fontsize=14)
        for t, lbl in zip(triangul, quantile_labels):
            add_quantile_labels(ax, t, lbl)
    else:
        # X labels increase left -> right
        x_tick_labels = [f"Q{i+1}" for i in range(M)]

        # Y labels decrease top -> bottom
        y_tick_labels = [f"Q{N-i}" for i in range(N)]
        ax.set_xticklabels(x_tick_labels, fontsize=14)
        ax.set_yticklabels(y_tick_labels, fontsize=14)

    plt.title(title, fontsize=20)

    # Highest quantile row at top
    ax.invert_yaxis()
    
    # Remove outer margins
    ax.margins(x=0, y=0)
    ax.set_aspect("equal", "box")

    # Make square cells
    plt.tight_layout()

    if save:
        out_path = save_path if save_path else f"{title}.png"
        plt.savefig(out_path)

    if show:
        plt.show()

    return fig