import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Loading
path = "/Users/brolinoconnell/Desktop/Johns Hopkins/Airlines_project/Fares_data/Merged_Fares .csv"
df = pd.read_csv(path, low_memory=False)

# === Clean and Convert Fare Column Safely ===
fare_col = "Average Fare ($)"

# Making strings float issue happened here 
df[fare_col] = (
    df[fare_col]
    .astype(str)
    .str.replace(r"[^\d\.\-]", "", regex=True)  # keep digits, periods, negatives
    .replace("", pd.NA)
)

df[fare_col] = pd.to_numeric(df[fare_col], errors="coerce")
df = df.dropna(subset=[fare_col, "Year", "Quarter"])

# Continuous time axis (like R’s mutate(Time = Year + (Quarter - 1)/4))
df["Time"] = df["Year"] + (df["Quarter"] - 1) / 4

# scatter 
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=df,
    x="Year",
    y=fare_col,
    hue="Quarter",
    palette="coolwarm",
    alpha=0.5,
    s=20,
)
plt.title("Average Fare by Quarter (1993–2025)", fontsize=16)
plt.xlabel("Year")
plt.ylabel("Average Fare ($)")
plt.legend(title="Quarter")
plt.tight_layout()
plt.show()

# quarterly mean time series without a lag 
df_line = df.groupby(["Year", "Quarter"], as_index=False)[fare_col].mean()
df_line["Time"] = df_line["Year"] + (df_line["Quarter"] - 1) / 4

plt.figure(figsize=(10, 6))
sns.lineplot(
    data=df_line,
    x="Time",
    y=fare_col,
    hue="Quarter",
    linewidth=1.8,
    marker="o",
    palette="coolwarm",
)
plt.title("Average Fare by Quarter (1993–2025)", fontsize=16)
plt.xlabel("Year")
plt.ylabel("Average Fare ($)")
plt.legend(title="Quarter")
plt.tight_layout()
plt.show()