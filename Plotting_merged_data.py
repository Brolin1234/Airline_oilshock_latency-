# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Loading
# path = "/Users/brolinoconnell/Desktop/Johns Hopkins/Airlines_project/Fares_data/Merged_Fares .csv"
# df = pd.read_csv(path, low_memory=False)

# # === Clean and Convert Fare Column Safely ===
# fare_col = "Average Fare ($)"

# # Making strings float issue happened here 
# df[fare_col] = (
#     df[fare_col]
#     .astype(str)
#     .str.replace(r"[^\d\.\-]", "", regex=True)  # keep digits, periods, negatives
#     .replace("", pd.NA)
# )

# df[fare_col] = pd.to_numeric(df[fare_col], errors="coerce")
# df = df.dropna(subset=[fare_col, "Year", "Quarter"])

# # Continuous time axis (like R’s mutate(Time = Year + (Quarter - 1)/4))
# df["Time"] = df["Year"] + (df["Quarter"] - 1) / 4

# # scatter 
# plt.figure(figsize=(10, 6))
# sns.scatterplot(
#     data=df,
#     x="Year",
#     y=fare_col,
#     hue="Quarter",
#     palette="coolwarm",
#     alpha=0.5,
#     s=20,
# )
# plt.title("Average Fare by Quarter (1993–2025)", fontsize=16)
# plt.xlabel("Year")
# plt.ylabel("Average Fare ($)")
# plt.legend(title="Quarter")
# plt.tight_layout()
# plt.show()

# # quarterly mean time series without a lag 
# df_line = df.groupby(["Year", "Quarter"], as_index=False)[fare_col].mean()
# df_line["Time"] = df_line["Year"] + (df_line["Quarter"] - 1) / 4

# plt.figure(figsize=(10, 6))
# sns.lineplot(
#     data=df_line,
#     x="Time",
#     y=fare_col,
#     hue="Quarter",
#     linewidth=1.8,
#     marker="o",
#     palette="coolwarm",
# )
# plt.title("Average Fare by Quarter (1993–2025)", fontsize=16)
# plt.xlabel("Year")
# plt.ylabel("Average Fare ($)")
# plt.legend(title="Quarter")
# plt.tight_layout()
# plt.show()




# # Shocks PLot 
# import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib.ticker as mtick
# import seaborn as sns

# # Read data
# df = pd.read_csv("/Users/brolinoconnell/Desktop/Johns Hopkins/Airlines_project/Fares_data/Merged_Fares .csv", low_memory=False)

# # --- Robust cleaning ---
# def safe_to_float(x):
#     if isinstance(x, str):
#         x = x.replace("$", "").replace(",", "").replace("(", "").replace(")", "").strip()
#         try:
#             return float(x)
#         except ValueError:
#             return None
#     return x

# df["Fare"] = df["Average Fare ($)"].apply(safe_to_float)
# df["Passengers"] = df["2024 Passengers (10% sample)"].apply(safe_to_float)
# df["Time"] = df["Year"] + (df["Quarter"] - 1) / 4

# # Drop bad rows
# df = df.dropna(subset=["Fare", "Passengers", "Time"])

# # Summarize and smooth
# df_summary = (
#     df.groupby(["Year", "Quarter"], as_index=False)
#       .agg(Avg_Fare=("Fare", "mean"), Avg_Passengers=("Passengers", "mean"))
# )
# df_summary["Time"] = df_summary["Year"] + (df_summary["Quarter"] - 1) / 4
# df_summary["Fare_Smoothed"] = df_summary["Avg_Fare"].rolling(4).mean()
# df_summary["Pax_Smoothed"] = df_summary["Avg_Passengers"].rolling(4).mean()

# # --- Shocks ---
# shocks = [
#     {"xmin": 2008, "xmax": 2009, "label": "Financial Crisis (2008–09)", "color": "#ffcc99"},
#     {"xmin": 2020, "xmax": 2021, "label": "COVID-19 (2020–21)", "color": "#99ccff"},
#     {"xmin": 2022, "xmax": 2023, "label": "Ukraine Invasion (2022–23)", "color": "#d9b3ff"},
# ]

# # --- Plot ---
# sns.set_theme(style="whitegrid", font_scale=1.3)
# fig, ax1 = plt.subplots(figsize=(12, 7))

# # Shaded shock zones
# for shock in shocks:
#     ax1.axvspan(shock["xmin"], shock["xmax"], color=shock["color"], alpha=0.25, label=shock["label"])

# # Airfare (black line)
# ax1.plot(df_summary["Time"], df_summary["Fare_Smoothed"], color="black", linewidth=2, label="Average Fare ($)")
# ax1.scatter(df_summary["Time"], df_summary["Avg_Fare"], color="black", alpha=0.4, s=15)

# # Axis for passengers
# ax2 = ax1.twinx()
# ax2.plot(df_summary["Time"], df_summary["Pax_Smoothed"], color="steelblue", linestyle="--",
#          linewidth=2, label="Passenger Volume (10% sample)")

# # Labels and axes
# ax1.set_xlabel("Year", fontsize=13)
# ax1.set_ylabel("Average Fare ($)", color="firebrick")
# ax2.set_ylabel("Passenger Volume (10% sample)", color="steelblue")
# ax1.set_xlim(1993, 2025)
# ax1.xaxis.set_major_locator(mtick.MultipleLocator(4))
# ax2.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{int(x):,}"))

# # Legend
# lines, labels = ax1.get_legend_handles_labels()
# lines2, labels2 = ax2.get_legend_handles_labels()
# shock_labels = [plt.Line2D([0], [0], color=s["color"], lw=10, alpha=0.3) for s in shocks]
# shock_texts = [s["label"] for s in shocks]
# ax1.legend(lines + lines2 + shock_labels, labels + labels2 + shock_texts,
#             loc="upper left", frameon=False, fontsize=10)

# # Titles
# plt.title("Airfare vs Passenger Volume (1993–2025)", fontsize=17, weight="bold", pad=20)
# plt.suptitle("Solid black = Airfare trend  |  Dashed blue = Passenger trend  |  Shaded = Shock periods",
#              fontsize=12, y=0.91)

# # Save and show
# plt.tight_layout()
# plt.savefig("Airfare_vs_Passengers_Python.png", dpi=300, bbox_inches="tight")
# plt.show()



# Clean dual-axis shocks plot — minimal changes as requested
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.lines import Line2D
import seaborn as sns

# Read data (use your exact path)
df = pd.read_csv("/Users/brolinoconnell/Desktop/Johns Hopkins/Airlines_project/Fares_data/Merged_Fares .csv",
                 low_memory=False)

def safe_to_float(x):
    if isinstance(x, str):
        x = x.replace("$", "").replace(",", "").replace("(", "").replace(")", "").strip()
        try:
            return float(x)
        except ValueError:
            return None
    return x

df["Fare"] = df["Average Fare ($)"].apply(safe_to_float)
df["Passengers"] = df["2024 Passengers (10% sample)"].apply(safe_to_float)
df = df.dropna(subset=["Fare", "Passengers", "Year", "Quarter"])
df["Time"] = df["Year"] + (df["Quarter"] - 1) / 4

# QThis is the code amking the scatter points: NOte here 
# that these points are an average of hte airfare that will 
# end up overlaying the average line and then they are 
# differetiated by shape so that way we do not have 60kplus points on the chart 
df_summary = (df.groupby(["Year", "Quarter"], as_index=False)
                .agg(Avg_Fare=("Fare", "mean"),
                     Avg_Passengers=("Passengers", "mean")))
df_summary["Time"] = df_summary["Year"] + (df_summary["Quarter"] - 1) / 4
df_summary["Fare_Smoothed"] = df_summary["Avg_Fare"].rolling(4).mean()
df_summary["Pax_Smoothed"]  = df_summary["Avg_Passengers"].rolling(4).mean()

# Shock periods
shocks = [
    {"xmin": 2008, "xmax": 2009, "name": "Financial Crisis (2008–09)", "color": "#ffcc99"},
    {"xmin": 2020, "xmax": 2021, "name": "COVID-19 (2020–21)",        "color": "#99ccff"},
    {"xmin": 2022, "xmax": 2023, "name": "Ukraine Invasion (2022–23)", "color": "#d9b3ff"},
]

sns.set_theme(style="whitegrid", font_scale=1.25)
fig, ax1 = plt.subplots(figsize=(12, 7))

# Shocks (no labels here—legend handled manually)
for s in shocks:
    ax1.axvspan(s["xmin"], s["xmax"], color=s["color"], alpha=0.25)

# Average fare line (same as before)
ax1.plot(df_summary["Time"], df_summary["Fare_Smoothed"],
         color="black", linewidth=2)

# Small quarterly dots (at AVERAGE LEVEL), shaped by quarter
markers = {1: "o", 2: "s", 3: "^", 4: "D"}
for q, mk in markers.items():
    d = df_summary[df_summary["Quarter"] == q]
    ax1.scatter(d["Time"], d["Avg_Fare"], color="black", alpha=0.45, s=18, marker=mk)

# Passenger dashed line (right axis)
ax2 = ax1.twinx()
ax2.plot(df_summary["Time"], df_summary["Pax_Smoothed"],
         color="steelblue", linestyle="--", linewidth=2)

# Axes/labels
ax1.set_xlabel("Year", fontsize=13)
ax1.set_ylabel("Average Fare ($)", color="firebrick")
ax2.set_ylabel("Passenger Volume (10% sample)", color="steelblue")
ax1.set_xlim(1993, 2025)
ax1.xaxis.set_major_locator(mtick.MultipleLocator(4))
ax2.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{int(x):,}"))

# Title (single, no overlap)
ax1.set_title(
    "Airfare vs Passenger Volume (1993–2025)\n"
)

# One legend outside
fare_handle = Line2D([0], [0], color="black", lw=2, label="Average Fare ($)")
pax_handle  = Line2D([0], [0], color="steelblue", lw=2, ls="--", label="Passenger Volume (10% sample)")
quarter_handles = [Line2D([0], [0], marker=mk, color='w', markerfacecolor='black',
                          markersize=7, label=f"Quarter {q}") for q, mk in markers.items()]
shock_handles   = [Line2D([0], [0], color=s["color"], lw=10, alpha=0.3, label=s["name"]) for s in shocks]

legend_items  = [fare_handle, pax_handle] + quarter_handles + shock_handles
legend_labels = [h.get_label() for h in legend_items]

fig.subplots_adjust(bottom=0.24, top=0.90)
ax1.legend(legend_items, legend_labels, loc="upper center",
           bbox_to_anchor=(0.5, -0.18), ncol=2, frameon=False, fontsize=10)

plt.tight_layout()
plt.savefig("Airfare_vs_Passengers_Clean_FINAL.png", dpi=300, bbox_inches="tight")
plt.show()