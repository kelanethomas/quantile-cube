# quantile-cube

A Python package for visualizing the distribution of 3D movement data — velocity, acceleration, and angle — collapsed into a 2D heatmap.

Movement observations are binned into quantiles along three dimensions: velocity (x-axis), acceleration (y-axis), and angle of movement (the four triangles within each cell). Each triangle's color represents the density of observations — the proportion of total time spent in that specific combination of velocity, acceleration, and angle quantile. This makes it possible to see at a glance where movement is concentrated across all three dimensions simultaneously.

## Installation

```bash
pip install quantile-cube
```

## Quick Start

### Option 1 — Raw arrays (recommended)

```python
from quantile_cube import plot_cube
import numpy as np

q1 = np.random.rand(25)
q2 = np.random.rand(25)
q3 = np.random.rand(25)
q4 = np.random.rand(25)

plot_cube(
    values=[q1, q2, q3, q4],
    M=5,
    N=5,
    title="My Quantile Cube",
    colorbar_label="Value",
    cmap="viridis",
)
```

### Option 2 — DataFrame

If your data is in a DataFrame with columns named like `Q1_vel_Q1_acc_Q1_angle`:

```python
from quantile_cube import plot_cube

plot_cube(
    cube_data=df,
    M=5,
    N=5,
    title="Angle Quantile Cube",
)
```

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `values` | list of 4 arrays | `None` | One array per quantile, each of length M×N |
| `cube_data` | DataFrame | `None` | Single-row DataFrame with columns `Q{vel}_vel_Q{acc}_acc_Q{angle}_angle` |
| `M` | int | `5` | Number of columns |
| `N` | int | `5` | Number of rows |
| `minimum` | float | `0` | Colormap lower bound |
| `maximum` | float | data max rounded up to nearest 0.01 | Colormap upper bound |
| `cmap` | str or Colormap | `"Reds"` | Matplotlib colormap |
| `title` | str | `"Quantile Cube"` | Plot title and default save filename |
| `colorbar_label` | str | `""` | Colorbar label |
| `xlabel` | str | `"Velocity"` | X-axis label |
| `ylabel` | str | `"Acceleration"` | Y-axis label |
| `quantile_labels` | list of 4 str | `["Q1","Q2","Q3","Q4"]` | Triangle labels |
| `show_quantile_labels` | bool | `False` | Show label-only summary view |
| `show_values` | bool | `False` | Print numeric value at center of each triangle |
| `value_fmt` | str | `".4f"` | Format string for numeric labels when `show_values=True` |
| `grey_nonsignificant` | bool | `False` | Render NaN values in grey |
| `save` | bool | `True` | Save figure to file |
| `save_path` | str | `"<title>.png"` | Custom save path |
| `show` | bool | `True` | Call `plt.show()` |
| `figsize` | tuple | `(7, 7)` | Figure size in inches |

## Advanced Usage

### Custom axis labels

```python
plot_cube(
    values=[q1, q2, q3, q4],
    xlabel="Speed Bins",
    ylabel="Acceleration Bins",
)
```

### Custom quantile labels

```python
plot_cube(
    values=[q1, q2, q3, q4],
    quantile_labels=["Low", "Mid-Low", "Mid-High", "High"],
    show_quantile_labels=True,
)
```

### Handling non-significant values

```python
import numpy as np

q1_with_nans = np.where(pvalues > 0.05, np.nan, q1)

plot_cube(
    values=[q1_with_nans, q2, q3, q4],
    grey_nonsignificant=True,
)
```

## License

MIT