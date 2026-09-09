import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import polars as pl
import requests
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from pathlib import Path

# def read_eurostat_tsv(file_path):
#     # Read TSV file
#     df = pd.read_csv(file_path, sep="\t")
#
#     # Get the first column name
#     first_col = df.columns[0]
#
#     # Get dimension names
#     dimension_names = first_col.replace("\\TIME_PERIOD", "").split(",")
#
#     # Split first column
#     dimensions = df.iloc[:, 0].str.split(",", expand=True)
#     dimensions.columns = dimension_names
#
#     # Combine dimensions with remaining columns
#     df = pd.concat(
#         [dimensions, df.iloc[:, 1:]],
#         axis=1
#     )
#
#     # Create output filename based on input filename
#     input_path = Path(file_path)
#     output_path = input_path.with_name(
#         input_path.stem + "_cleaned.csv"
#     )
#
#     # Export
#     df.to_csv(output_path, index=False)
#
#     return df



df = pd.read_csv("At-risk-of poverty rate for children by citizenship of their parents_cleaned.csv")
# Columns that are years
year_cols = [col for col in df.columns if str(col).strip().isdigit()]

# Keep only the numerical part of Eurostat values
for col in year_cols:
    df[col] = pd.to_numeric(df[col].astype(str).str.extract(r"(-?\d+(?:\.\d+)?)", expand=False), errors="coerce")

# Everything except applicant and years identifies the row
id_cols = [col for col in df.columns if col not in year_cols and col != "citizen"]

# Pivot applicant statuses into columns
df_grouped = df.pivot(index=id_cols, columns="citizen", values=year_cols)

# Flatten the multi-level column names
df_grouped.columns = [
    f"{status}_{year}"
    for year, status in df_grouped.columns
]

#print
print(df_grouped.head())

# Turn index columns back into normal columns
df_grouped = df_grouped.reset_index()
df_grouped = df_grouped[~df_grouped["geo"].str.contains(r"\d", na=False)]

# Create a new csv file
df_grouped.to_csv("At-risk-of poverty rate for children grouped.csv", index=False)

##PLOTTING
# Read CSV
df = df_grouped

# Remove spaces from column names
df.columns = df.columns.str.strip()

# Select Netherlands and Spain
countries = df[df["geo"].isin(["NL", "ES"])]

years = range(2003, 2026)

plt.figure(figsize=(12, 6))

# Assign a color to each country
country_colors = {
    "NL": "orange",
    "ES": "blue"
}

for country in ["NL", "ES"]:

    country_df = countries[countries["geo"] == country]

    nat = []
    foreign = []

    for year in years:
        nat.append(
            country_df[f"NAT_{year}"].iloc[0]
        )

        foreign.append(
            country_df[f"FOR_{year}"].iloc[0]
        )

    # National = solid line
    plt.plot(
        years,
        nat,
        color=country_colors[country],
        linestyle="-",
        linewidth=2,
        label=f"{country} - National"
    )

    # Foreign = dashed line
    plt.plot(
        years,
        foreign,
        color=country_colors[country],
        linestyle="--",
        linewidth=2,
        label=f"{country} - Foreign"
    )

plt.xlabel("Year")
plt.ylabel("At-risk-of-poverty rate (%)")
plt.title("At-risk-of-poverty rate for children – Netherlands & Spain")
plt.legend()
plt.grid(alpha=0.3)

plt.show()