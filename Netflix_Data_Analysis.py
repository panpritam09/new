# ============================================================
# NETFLIX MOVIES & TV SHOWS DATA ANALYSIS - ADVANCED EDITION
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Added new line
# ............................
# 1. IMPORT LIBRARIES
#.............................

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from matplotlib.ticker import MaxNLocator
import warnings

warnings.filterwarnings("ignore")

# -----------------------------
# 2. GLOBAL STYLE SETTINGS
# -----------------------------

# Beautiful modern style
sns.set_theme(style="whitegrid", context="talk")
plt.rcParams.update({
    "figure.facecolor": "#0e1117",
    "axes.facecolor": "#0e1117",
    "axes.edgecolor": "#444",
    "axes.labelcolor": "#ffffff",
    "xtick.color": "#dddddd",
    "ytick.color": "#dddddd",
    "text.color": "#ffffff",
    "grid.color": "#2a2f3a",
    "grid.alpha": 0.5,
    "font.family": "DejaVu Sans",
    "font.size": 12,
    "axes.titlesize": 16,
    "axes.titleweight": "bold",
})

# Custom vibrant color palettes (no plain blue)
PALETTE_MULTI = [
    "#FF6B6B", "#FFD93D", "#6BCB77", "#4D96FF",
    "#C780FA", "#FF8C42", "#00C2A8", "#F72585",
    "#B5E48C", "#F4A261", "#9D4EDD", "#06D6A0",
    "#EF476F", "#118AB2", "#FFB703"
]

# Gradient helper for horizontal bars
def gradient_colors(n, cmap_name="plasma"):
    cmap = plt.get_cmap(cmap_name)
    return [cmap(i / max(n - 1, 1)) for i in range(n)]

# -----------------------------
# 3. LOAD DATASET
# -----------------------------

df = pd.read_csv("netflix_titles_1000.csv")

print("\n" + "=" * 60)
print("NETFLIX DATASET - ADVANCED ANALYSIS")
print("=" * 60)

print(df.head())

# -----------------------------
# 4. BASIC INFORMATION
# -----------------------------

print("\n" + "=" * 60)
print("DATASET SHAPE")
print("=" * 60)
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\n" + "=" * 60)
print("COLUMN NAMES")
print("=" * 60)
print(df.columns.tolist())

print("\n" + "=" * 60)
print("DATA TYPES")
print("=" * 60)
print(df.dtypes)

print("\n" + "=" * 60)
print("DATASET INFORMATION")
print("=" * 60)
df.info()

# -----------------------------
# 5. STATISTICAL INFORMATION
# -----------------------------

print("\n" + "=" * 60)
print("STATISTICAL SUMMARY")
print("=" * 60)
print(df.describe(include="all"))

# -----------------------------
# 6. HANDLE MISSING VALUES
# -----------------------------

print("\n" + "=" * 60)
print("MISSING VALUES (BEFORE CLEANING)")
print("=" * 60)
print(df.isnull().sum())

for col in ["director", "cast", "country", "rating"]:
    df[col] = df[col].fillna("Unknown")

df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")

print("\n" + "=" * 60)
print("MISSING VALUES (AFTER CLEANING)")
print("=" * 60)
print(df.isnull().sum())

# ============================================================
# ANALYSIS SECTION
# ============================================================

# -----------------------------
# 7. MOVIES VS TV SHOWS (PIE - Vibrant Colors)
# -----------------------------

print("\n" + "=" * 60)
print("MOVIES VS TV SHOWS")
print("=" * 60)

type_count = df["type"].value_counts()
print(type_count)

fig, ax = plt.subplots(figsize=(8, 8))
colors_pie = ["#FF6B6B", "#4D96FF"]
explode = (0.04, 0.04)

wedges, texts, autotexts = ax.pie(
    type_count,
    labels=type_count.index,
    autopct="%1.1f%%",
    startangle=120,
    colors=colors_pie,
    explode=explode,
    shadow=True,
    wedgeprops={"edgecolor": "#0e1117", "linewidth": 3},
    textprops={"color": "#ffffff", "fontsize": 13, "fontweight": "bold"},
)

for at in autotexts:
    at.set_color("#0e1117")
    at.set_fontweight("bold")

ax.set_title("Movies vs TV Shows Distribution", pad=20, color="#FFD93D")
plt.tight_layout()
plt.savefig("movies_vs_tv.png", dpi=300, bbox_inches="tight", facecolor="#0e1117")
plt.show()

# -----------------------------
# 8. TOP 10 GENRES (Horizontal - Unique Colors)
# -----------------------------

print("\n" + "=" * 60)
print("TOP 10 GENRES")
print("=" * 60)

genres = df["listed_in"].dropna().str.split(", ")
genre_count = genres.explode().value_counts()
print(genre_count.head(10))

top_genres = genre_count.head(10).sort_values()
colors_g = gradient_colors(len(top_genres), "plasma")

fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.barh(top_genres.index, top_genres.values, color=colors_g,
               edgecolor="#0e1117", linewidth=1.5)

# Value labels
for bar in bars:
    w = bar.get_width()
    ax.text(w + max(top_genres.values) * 0.01, bar.get_y() + bar.get_height() / 2,
            f"{int(w)}", va="center", color="#ffffff", fontsize=11, fontweight="bold")

ax.set_xlabel("Number of Titles", color="#ffffff")
ax.set_ylabel("Genre", color="#ffffff")
ax.set_title("Top 10 Netflix Genres", color="#FFD93D", pad=15)
ax.set_xlim(0, max(top_genres.values) * 1.12)
ax.grid(axis="x", color="#2a2f3a", linestyle="--", alpha=0.6)
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig("top_genres.png", dpi=300, bbox_inches="tight", facecolor="#0e1117")
plt.show()

# -----------------------------
# 9. TOP 10 COUNTRIES (Horizontal - Unique Colors)
# -----------------------------

print("\n" + "=" * 60)
print("TOP 10 COUNTRIES")
print("=" * 60)

countries = df["country"].dropna().str.split(", ")
country_count = countries.explode().value_counts()
print(country_count.head(10))

top_countries = country_count.head(10).sort_values()
colors_c = gradient_colors(len(top_countries), "viridis")

fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.barh(top_countries.index, top_countries.values, color=colors_c,
               edgecolor="#0e1117", linewidth=1.5)

for bar in bars:
    w = bar.get_width()
    ax.text(w + max(top_countries.values) * 0.01, bar.get_y() + bar.get_height() / 2,
            f"{int(w)}", va="center", color="#ffffff", fontsize=11, fontweight="bold")

ax.set_xlabel("Number of Titles", color="#ffffff")
ax.set_ylabel("Country", color="#ffffff")
ax.set_title("Top 10 Countries Producing Netflix Content", color="#FFD93D", pad=15)
ax.set_xlim(0, max(top_countries.values) * 1.12)
ax.grid(axis="x", color="#2a2f3a", linestyle="--", alpha=0.6)
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig("top_countries.png", dpi=300, bbox_inches="tight", facecolor="#0e1117")
plt.show()

# -----------------------------
# 10. NETFLIX RATINGS (Horizontal - Unique Colors)
# -----------------------------

print("\n" + "=" * 60)
print("NETFLIX RATINGS")
print("=" * 60)

rating_count = df["rating"].value_counts()
print(rating_count)

top_ratings = rating_count.head(10).sort_values()
colors_r = gradient_colors(len(top_ratings), "cool")

fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.barh(top_ratings.index, top_ratings.values, color=colors_r,
               edgecolor="#0e1117", linewidth=1.5)

for bar in bars:
    w = bar.get_width()
    ax.text(w + max(top_ratings.values) * 0.01, bar.get_y() + bar.get_height() / 2,
            f"{int(w)}", va="center", color="#ffffff", fontsize=11, fontweight="bold")

ax.set_xlabel("Number of Titles", color="#ffffff")
ax.set_ylabel("Rating", color="#ffffff")
ax.set_title("Netflix Content by Rating", color="#FFD93D", pad=15)
ax.set_xlim(0, max(top_ratings.values) * 1.12)
ax.grid(axis="x", color="#2a2f3a", linestyle="--", alpha=0.6)
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig("ratings.png", dpi=300, bbox_inches="tight", facecolor="#0e1117")
plt.show()

# -----------------------------
# 11. TOP 10 DIRECTORS (Horizontal - Unique Colors)
# -----------------------------

print("\n" + "=" * 60)
print("TOP DIRECTORS")
print("=" * 60)

director_count = df[df["director"] != "Unknown"]["director"].value_counts()
print(director_count.head(10))

top_directors = director_count.head(10).sort_values()
colors_d = gradient_colors(len(top_directors), "magma")

fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.barh(top_directors.index, top_directors.values, color=colors_d,
               edgecolor="#0e1117", linewidth=1.5)

for bar in bars:
    w = bar.get_width()
    ax.text(w + max(top_directors.values) * 0.01, bar.get_y() + bar.get_height() / 2,
            f"{int(w)}", va="center", color="#ffffff", fontsize=11, fontweight="bold")

ax.set_xlabel("Number of Titles", color="#ffffff")
ax.set_ylabel("Director", color="#ffffff")
ax.set_title("Top 10 Directors", color="#FFD93D", pad=15)
ax.set_xlim(0, max(top_directors.values) * 1.12)
ax.grid(axis="x", color="#2a2f3a", linestyle="--", alpha=0.6)
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig("top_directors.png", dpi=300, bbox_inches="tight", facecolor="#0e1117")
plt.show()

# -----------------------------
# 12. CONTENT BY RELEASE YEAR (Line - Vibrant)
# -----------------------------

print("\n" + "=" * 60)
print("CONTENT BY RELEASE YEAR")
print("=" * 60)

year_count = df["release_year"].value_counts().sort_index()
print(year_count.tail(15))

fig, ax = plt.subplots(figsize=(14, 7))
ax.plot(year_count.index, year_count.values, marker="o", markersize=6,
        color="#00C2A8", linewidth=3, markerfacecolor="#FFD93D",
        markeredgecolor="#0e1117", markeredgewidth=1.2, label="Titles")
ax.fill_between(year_count.index, year_count.values, alpha=0.18, color="#00C2A8")

ax.set_xlabel("Release Year", color="#ffffff")
ax.set_ylabel("Number of Titles", color="#ffffff")
ax.set_title("Netflix Content by Release Year", color="#FFD93D", pad=15)
ax.grid(color="#2a2f3a", linestyle="--", alpha=0.5)
ax.legend(facecolor="#1a1f2b", edgecolor="#444", labelcolor="#ffffff")
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig("content_by_year.png", dpi=300, bbox_inches="tight", facecolor="#0e1117")
plt.show()

# -----------------------------
# 13. MOVIES VS TV SHOWS BY YEAR (Line - Vibrant)
# -----------------------------

print("\n" + "=" * 60)
print("MOVIES VS TV SHOWS BY YEAR")
print("=" * 60)

content_year = df.groupby(["release_year", "type"]).size().unstack(fill_value=0)
print(content_year.tail(10))

fig, ax = plt.subplots(figsize=(14, 7))
ax.plot(content_year.index, content_year["Movie"], label="Movies",
        color="#FF6B6B", linewidth=3, marker="o", markersize=5)
ax.plot(content_year.index, content_year["TV Show"], label="TV Shows",
        color="#4D96FF", linewidth=3, marker="s", markersize=5)

ax.fill_between(content_year.index, content_year["Movie"], alpha=0.12, color="#FF6B6B")
ax.fill_between(content_year.index, content_year["TV Show"], alpha=0.12, color="#4D96FF")

ax.set_xlabel("Release Year", color="#ffffff")
ax.set_ylabel("Number of Titles", color="#ffffff")
ax.set_title("Movies vs TV Shows by Release Year", color="#FFD93D", pad=15)
ax.grid(color="#2a2f3a", linestyle="--", alpha=0.5)
ax.legend(facecolor="#1a1f2b", edgecolor="#444", labelcolor="#ffffff")
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig("movies_vs_tv_by_year.png", dpi=300, bbox_inches="tight", facecolor="#0e1117")
plt.show()

# -----------------------------
# 14. MOVIE DURATION HISTOGRAM (Vibrant)
# -----------------------------

print("\n" + "=" * 60)
print("MOVIE DURATION ANALYSIS")
print("=" * 60)

movies_df = df[df["type"] == "Movie"].copy()
movies_df["duration_minutes"] = movies_df["duration"].str.extract(r"(\d+)").astype(float)
print(movies_df["duration_minutes"].describe())

average_duration = movies_df["duration_minutes"].mean()
print("Average Movie Duration:", round(average_duration, 2), "minutes")

fig, ax = plt.subplots(figsize=(12, 7))
n, bins, patches = ax.hist(
    movies_df["duration_minutes"].dropna(),
    bins=22, edgecolor="#0e1117", linewidth=1.2
)

# Apply gradient to bars
cmap = plt.get_cmap("plasma")
for i, patch in enumerate(patches):
    patch.set_facecolor(cmap(i / len(patches)))

ax.axvline(average_duration, color="#FFD93D", linestyle="--", linewidth=2.5,
           label=f"Mean: {average_duration:.1f} min")

ax.set_xlabel("Duration (minutes)", color="#ffffff")
ax.set_ylabel("Number of Movies", color="#ffffff")
ax.set_title("Distribution of Movie Durations", color="#FFD93D", pad=15)
ax.grid(axis="y", color="#2a2f3a", linestyle="--", alpha=0.5)
ax.legend(facecolor="#1a1f2b", edgecolor="#444", labelcolor="#ffffff")
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig("movie_duration.png", dpi=300, bbox_inches="tight", facecolor="#0e1117")
plt.show()

# -----------------------------
# 15. CONTENT ADDED BY YEAR (Horizontal - Unique Colors)
# -----------------------------

print("\n" + "=" * 60)
print("CONTENT ADDED BY YEAR")
print("=" * 60)

df["date_added_year"] = df["date_added"].dt.year
added_year = df["date_added_year"].value_counts().sort_index()
print(added_year)

added_year_sorted = added_year.sort_values()
colors_a = gradient_colors(len(added_year_sorted), "turbo")

fig, ax = plt.subplots(figsize=(12, max(7, len(added_year_sorted) * 0.5)))
bars = ax.barh(added_year_sorted.index.astype(int).astype(str),
               added_year_sorted.values, color=colors_a,
               edgecolor="#0e1117", linewidth=1.2)

for bar in bars:
    w = bar.get_width()
    ax.text(w + max(added_year_sorted.values) * 0.01, bar.get_y() + bar.get_height() / 2,
            f"{int(w)}", va="center", color="#ffffff", fontsize=10, fontweight="bold")

ax.set_xlabel("Number of Titles Added", color="#ffffff")
ax.set_ylabel("Year", color="#ffffff")
ax.set_title("Netflix Content Added by Year", color="#FFD93D", pad=15)
ax.set_xlim(0, max(added_year_sorted.values) * 1.12)
ax.grid(axis="x", color="#2a2f3a", linestyle="--", alpha=0.5)
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig("content_added_by_year.png", dpi=300, bbox_inches="tight", facecolor="#0e1117")
plt.show()

# -----------------------------
# 16. MOVIES VS TV SHOWS BY YEAR (Horizontal Grouped Bar)
# -----------------------------

print("\n" + "=" * 60)
print("GROUPED HORIZONTAL BAR - MOVIES VS TV SHOWS")
print("=" * 60)

recent_years = content_year.tail(15)
years = recent_years.index.astype(int).astype(str)
y_pos = np.arange(len(years))
bar_height = 0.4

fig, ax = plt.subplots(figsize=(12, max(8, len(years) * 0.6)))
ax.barh(y_pos + bar_height / 2, recent_years["Movie"], bar_height,
        label="Movies", color="#FF6B6B", edgecolor="#0e1117")
ax.barh(y_pos - bar_height / 2, recent_years["TV Show"], bar_height,
        label="TV Shows", color="#4D96FF", edgecolor="#0e1117")

ax.set_yticks(y_pos)
ax.set_yticklabels(years)
ax.set_xlabel("Number of Titles", color="#ffffff")
ax.set_ylabel("Release Year", color="#ffffff")
ax.set_title("Movies vs TV Shows by Release Year (Last 15 Years)",
             color="#FFD93D", pad=15)
ax.legend(facecolor="#1a1f2b", edgecolor="#444", labelcolor="#ffffff")
ax.grid(axis="x", color="#2a2f3a", linestyle="--", alpha=0.5)
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig("movies_vs_tv_by_year_horizontal.png", dpi=300,
            bbox_inches="tight", facecolor="#0e1117")
plt.show()

# -----------------------------
# 17. CORRELATION HEATMAP
# -----------------------------

print("\n" + "=" * 60)
print("CORRELATION ANALYSIS")
print("=" * 60)

numeric_columns = df[["release_year"]]
correlation = numeric_columns.corr()
print(correlation)

fig, ax = plt.subplots(figsize=(6, 5))
sns.heatmap(
    correlation, annot=True, cmap="rocket", ax=ax,
    cbar_kws={"label": "Correlation"},
    linewidths=2, linecolor="#0e1117",
    annot_kws={"color": "#ffffff", "fontsize": 14, "fontweight": "bold"}
)
ax.set_title("Correlation Heatmap", color="#FFD93D", pad=15)
plt.tight_layout()
plt.savefig("correlation_heatmap.png", dpi=300, bbox_inches="tight", facecolor="#0e1117")
plt.show()

# ============================================================
# FINAL SUMMARY
# ============================================================

total = len(df)
movies = len(df[df["type"] == "Movie"])
tv_shows = len(df[df["type"] == "TV Show"])
movie_percentage = (movies / total) * 100
tv_percentage = (tv_shows / total) * 100

most_common_genre = genre_count.idxmax()
most_common_country = country_count.idxmax()
most_common_rating = rating_count.idxmax()
latest_year = df["release_year"].max()
earliest_year = df["release_year"].min()

print("\n" + "=" * 60)
print("           NETFLIX ANALYSIS SUMMARY")
print("=" * 60)

summary = {
    "Total Titles": total,
    "Movies": movies,
    "TV Shows": tv_shows,
    "Movie Percentage": f"{movie_percentage:.2f}%",
    "TV Show Percentage": f"{tv_percentage:.2f}%",
    "Most Common Genre": most_common_genre,
    "Most Common Country": most_common_country,
    "Most Common Rating": most_common_rating,
    "Average Movie Duration": f"{average_duration:.2f} minutes",
    "Earliest Release Year": earliest_year,
    "Latest Release Year": latest_year,
}

for k, v in summary.items():
    print(f"{k:.<35} {v}")

print("=" * 60)
print("          ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 60)