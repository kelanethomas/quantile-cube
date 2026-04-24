import numpy as np
import pandas as pd
from quantile_cube.plot import plot_cube

M = 5
N = 5

print("Testing Cube Method 1")

# Build obvious values
q1 = np.arange(101, 126)   # 101..125
q2 = np.arange(201, 226)
q3 = np.arange(301, 326)
q4 = np.arange(401, 426)

plot_cube(
    values=[q1, q2, q3, q4],
    M=M,
    N=N,
    show_values=True,
    title="DEBUG TEST",
    cmap="Reds"
)


cols = {}

for acc in range(1, 6):          # Q1 -> Q5 acceleration
    for vel in range(1, 6):      # Q1 -> Q5 velocity

        # Make acceleration dominate value size
        base = acc * 100

        cols[f"Q{vel}_vel_Q{acc}_acc_Q1_angle"] = [base + 1]
        cols[f"Q{vel}_vel_Q{acc}_acc_Q2_angle"] = [base + 2]
        cols[f"Q{vel}_vel_Q{acc}_acc_Q3_angle"] = [base + 3]
        cols[f"Q{vel}_vel_Q{acc}_acc_Q4_angle"] = [base + 4]

df = pd.DataFrame(cols)

plot_cube(
    cube_data=df,
    M=5,
    N=5,
    show_values=True,
    title="Acceleration Order Test",
    cmap="Reds"
)