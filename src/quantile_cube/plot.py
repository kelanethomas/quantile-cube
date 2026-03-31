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
    save: bool = True,
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
        ["Q1", "Q2", "Q3", "Q4"].
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
        If True, save the figure to a file. Default is True.
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
    if cmap is None:
        cmap = plt.get_cmap("Reds")
    elif isinstance(cmap, str):
        cmap = plt.get_cmap(cmap)

    if quantile_labels is None:
        quantile_labels = ["Q1", "Q2", "Q3", "Q4"]
    if len(quantile_labels) != 4:
        raise ValueError("`quantile_labels` must contain exactly 4 strings.")

    # ------------------------------------------------------------------ #
    # Resolve data input
    # ------------------------------------------------------------------ #
    if values is not None:
        if len(values) != 4:
            raise ValueError("`values` must be a list of exactly 4 arrays (one per quantile).")
        q1, q2, q3, q4 = [np.asarray(v, dtype=float) for v in values]

    elif cube_data is not None:
        # Columns are named: Q{v}_vel_Q{a}_acc_Q{angle}_angle
        # e.g. Q1_vel_Q1_acc_Q1_angle
        # We build 4 flat arrays (one per angle quantile), ordered row by row:
        # for acc Q1..QN, for vel Q1..QM  → matches the grid left-to-right, top-to-bottom
        def _extract_angle_q(angle_q: int) -> np.ndarray:
            vals = []
            for a in range(1, N + 1):
                for v in range(1, M + 1):
                    col = f"Q{v}_vel_Q{a}_acc_Q{angle_q}_angle"
                    if col not in cube_data.columns:
                        raise ValueError(
                            f"Expected column '{col}' not found in DataFrame. "
                            f"Check that M={M} and N={N} match your data."
                        )
                    vals.append(cube_data[col].iloc[0])
            return np.asarray(vals, dtype=float)

        q1 = _extract_angle_q(1)
        q2 = _extract_angle_q(2)
        q3 = _extract_angle_q(3)
        q4 = _extract_angle_q(4)

    else:
        raise ValueError("Provide either `values` (list of 4 arrays) or `cube_data` (DataFrame).")

    # ------------------------------------------------------------------ #
    # Summary / label view vs full grid view
    # ------------------------------------------------------------------ #
    if show_quantile_labels:
        plot_values = [q1[-M], q2[-M], q3[-M], q4[-M]]
        plot_m, plot_n = 1, 1
    else:
        plot_values = [q1, q2, q3, q4]
        plot_m, plot_n = M, N

    # ------------------------------------------------------------------ #
    # Normalization
    # ------------------------------------------------------------------ #
    all_vals = np.concatenate([np.ravel(v) for v in plot_values])
    vmin = minimum if minimum is not None else 0.0
    raw_max = np.nanmax(all_vals)
    vmax = maximum if maximum is not None else np.ceil(raw_max * 100) / 100
    norm = plt.Normalize(vmin, vmax)

    # ------------------------------------------------------------------ #
    # Build triangulation and plot
    # ------------------------------------------------------------------ #
    triangul = triangulation_for_triheatmap(plot_m, plot_n)

    fig, ax = plt.subplots(figsize=figsize)

    if grey_nonsignificant:
        import copy
        grey_cmap = copy.copy(cmap)
        grey_cmap.set_bad(color="gray")
        masked_values = [np.ma.masked_invalid(np.ravel(v)) for v in plot_values]
        imgs = [
            ax.tripcolor(t, mv, cmap=grey_cmap, norm=norm, ec="white")
            for t, mv in zip(triangul, masked_values)
        ]
        nan_patch = mpatches.Patch(color="gray", label="Non-significant Coefficient")
        ax.legend(handles=[nan_patch], loc="upper left", bbox_to_anchor=(0.2, -0.16))
    else:
        imgs = [
            ax.tripcolor(t, np.ravel(val), cmap=cmap, norm=norm, ec="white")
            for t, val in zip(triangul, plot_values)
        ]

    # Value labels
    if show_values:
        for t, val in zip(triangul, plot_values):
            add_value_labels(ax, t, val, fmt=value_fmt)

    # Colorbar
    cbar = plt.colorbar(imgs[0], ax=ax)
    cbar.set_label(colorbar_label)

    # Axis ticks
    ax.set_xticks(range(plot_m))
    ax.set_yticks(range(plot_n))
    ax.set_xlabel(xlabel, fontsize=18)
    ax.set_ylabel(ylabel, fontsize=18)

    if show_quantile_labels:
        ax.set_xticklabels(["Q1"], fontsize=14)
        ax.set_yticklabels(["Q1"], fontsize=14)
        for t, lbl in zip(triangul, quantile_labels):
            add_quantile_labels(ax, t, lbl)
    else:
        x_tick_labels = [f"Q{i+1}" for i in range(M)]
        y_tick_labels = [f"Q{N-i}" for i in range(N)]
        ax.set_xticklabels(x_tick_labels, fontsize=14)
        ax.set_yticklabels(y_tick_labels, fontsize=14)

    plt.title(title, fontsize=20)
    ax.invert_yaxis()
    ax.margins(x=0, y=0)
    ax.set_aspect("equal", "box")
    plt.tight_layout()

    if save:
        out_path = save_path if save_path else f"{title}.png"
        plt.savefig(out_path)

    if show:
        plt.show()

    return fig