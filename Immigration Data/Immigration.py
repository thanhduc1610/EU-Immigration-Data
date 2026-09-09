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

def read_eurostat_tsv(file_path):
    # Read TSV file
    df = pd.read_csv(file_path, sep="\t")

    # Get the first column name
    first_col = df.columns[0]

    # Get dimension names
    dimension_names = first_col.replace("\\TIME_PERIOD", "").split(",")

    # Split first column
    dimensions = df.iloc[:, 0].str.split(",", expand=True)
    dimensions.columns = dimension_names

    # Combine dimensions with remaining columns
    df = pd.concat(
        [dimensions, df.iloc[:, 1:]],
        axis=1
    )

    # Create output filename based on input filename
    input_path = Path(file_path)
    output_path = input_path.with_name(
        input_path.stem + "_cleaned.csv"
    )

    # Export
    df.to_csv(output_path, index=False)

    return df

df = read_eurostat_tsv(
    "People living in households with very low work intensity by group of citizenship (population aged 18 to 64 years).tsv"
)

# Identify the year columns
year_cols = [col for col in df.columns if str(col).strip().isdigit()]

# Reshape from wide to long format
df_long = df.melt(
    id_vars=[col for col in df.columns if col not in year_cols],
    value_vars=year_cols,
    var_name="year",
    value_name="value"
)

# Convert year to integer
df_long["year"] = df_long["year"].astype(int)

# Clean Eurostat values and convert to numeric
df_long["value"] = (
    df_long["value"]
    .astype(str)
    .str.extract(r"(\d+(?:\.\d+)?)")[0]
)

df_long["value"] = pd.to_numeric(df_long["value"], errors="coerce")

plt.figure(figsize=(14, 8))

sns.lineplot(
    data=df_long,
    x="year",
    y="value",
    hue="geo"
)

plt.xlabel("Year")
plt.ylabel("Number of asylum applicants")
plt.title("Asylum Applicants by Country Over Time")

plt.legend(
    title="Country",
    bbox_to_anchor=(1.05, 1),
    loc="upper left"
)

plt.tight_layout()
plt.show()
