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

# #PLOTTING


# # Read CSV
# df = pd.read_csv(
#     "Asylum applicants by type - annual aggregated data_cleaned.csv"
# )
#
# # Keep only TOTAL applicants
# df_total = df[df["applicant"] == "TOTAL"].copy()
#
# # Identify the year columns
# year_cols = [col for col in df.columns if str(col).strip().isdigit()]
#
# # Convert from wide to long format
# plot_df = df_total.melt(
#     id_vars=["geo"],
#     value_vars=year_cols,
#     var_name="year",
#     value_name="applicants"
# )
#
# # Convert to numeric
# plot_df["year"] = pd.to_numeric(plot_df["year"])
# plot_df["applicants"] = pd.to_numeric(
#     plot_df["applicants"],
#     errors="coerce"
# )
#
# # Plot
# plt.figure(figsize=(14, 8))
#
# sns.lineplot(
#     data=plot_df,
#     x="year",
#     y="applicants",
#     hue="geo"
# )
#
# plt.title("Total Asylum Applicants by Country")
# plt.xlabel("Year")
# plt.ylabel("Number of Applicants")
#
# plt.show()