import numpy as np
import pandas as pd
from quantile_cube.plot import plot_cube

M = 5
N = 5

print("Testing Cube Method 1 with Sequential Data - Angle")

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
    value_fmt= "0.0f",
    title="DEBUG TEST",
    cmap="Reds"
)


cols = {}

for acc in range(1, 6):          # Q1 -> Q5 acceleration
    for vel in range(1, 6):      # Q1 -> Q5 velocity

        # Make acceleration dominate value size
        base = acc * 10

        cols[f"Q{vel}_vel_Q{acc}_acc_Q1_angle"] = [base + 1]
        cols[f"Q{vel}_vel_Q{acc}_acc_Q2_angle"] = [base + 2]
        cols[f"Q{vel}_vel_Q{acc}_acc_Q3_angle"] = [base + 3]
        cols[f"Q{vel}_vel_Q{acc}_acc_Q4_angle"] = [base + 4]

df = pd.DataFrame(cols)
print("Testing Cube Method 2 with Sequential Data - Acceleration") 

plot_cube(
    cube_data=df,
    M=5,
    N=5,
    show_values=True,
    value_fmt= "0.2f",
    title="Acceleration Order Test",
    cmap="Reds"
)

cols = {}

for acc in range(1, 6):          # Q1 -> Q5 acceleration
    for vel in range(1, 6):      # Q1 -> Q5 velocity

        # Make velocity dominate value size
        base = vel * 10

        cols[f"Q{vel}_vel_Q{acc}_acc_Q1_angle"] = [base + 1]
        cols[f"Q{vel}_vel_Q{acc}_acc_Q2_angle"] = [base + 2]
        cols[f"Q{vel}_vel_Q{acc}_acc_Q3_angle"] = [base + 3]
        cols[f"Q{vel}_vel_Q{acc}_acc_Q4_angle"] = [base + 4]

df = pd.DataFrame(cols)

print("Testing Cube Method 2 with Sequential Data - Velocity") 

plot_cube(
    cube_data=df,
    M=5,
    N=5,
    show_values=True,
    value_fmt= "0.2f",
    title="Velocity Order Test",
    cmap="Reds"
)

print("Testing Cube Method 2 with Diverging Data") 

diverging_data = pd.read_csv("tests/diverging_data.csv")

plot_cube(
    cube_data=diverging_data,
    M=5,
    N=5,
    title="Diverging Data Test",
    colorbar_ticks = [-0.23, -0.2, -0.1, 0, 0.1, 0.2, 0.23]
)

print("Testing Cube Method 2 with Nonsignificant Grey Cells")

df = diverging_data.copy()

# Pick columns to null out
cols_to_null = [
    col for col in df.columns
    if "Q3_acc" in col or "Q2_acc_Q4_angle" in col
]

df.loc[:, cols_to_null] = np.nan

plot_cube(
    cube_data=df,
    M=5,
    N=5,
    title="Grey Mask Test",
    grey_nonsignificant=True,
    colorbar_ticks=[-0.23, -0.2, -0.1, 0, 0.1, 0.2, 0.23]
)