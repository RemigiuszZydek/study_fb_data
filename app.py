from flask import Flask, render_template
import pandas as pd
import matplotlib
import os

matplotlib.use("Agg")
import matplotlib.pyplot as plt

app = Flask(__name__)

# =====================
# DANE
# =====================

df = pd.read_csv("matches.csv")
df["match_date"] = pd.to_datetime(df["match_date"])

como_df = df[
    (df["home_team"] == "Como 1907") |
    (df["away_team"] == "Como 1907")
].copy()

# =====================
# FEATURE ENGINEERING
# =====================

como_df["goals_scored"] = como_df.apply(
    lambda row: row["home_score"] if row["home_team"] == "Como 1907" else row["away_score"],
    axis=1
)

como_df["goals_conceded"] = como_df.apply(
    lambda row: row["away_score"] if row["home_team"] == "Como 1907" else row["home_score"],
    axis=1
)

como_df["shots_on_target"] = como_df.apply(
    lambda row: row["home_shots_on_target"] if row["home_team"] == "Como 1907" else row["away_shots_on_target"],
    axis=1
)

como_df["possession"] = como_df.apply(
    lambda row: row["home_possession"] if row["home_team"] == "Como 1907" else row["away_possession"],
    axis=1
)

como_df["opponent"] = como_df.apply(
    lambda row: row["away_team"] if row["home_team"] == "Como 1907" else row["home_team"],
    axis=1
)

def calculate_points(row):
    if row["goals_scored"] > row["goals_conceded"]:
        return 3
    if row["goals_scored"] == row["goals_conceded"]:
        return 1
    return 0

como_df["points"] = como_df.apply(calculate_points, axis=1)

# =====================
# FOLDER NA WYKRESY
# =====================

CHART_DIR = "static/charts"
os.makedirs(CHART_DIR, exist_ok=True)

# =====================
# POMOCNICZA FUNKCJA
# =====================

def save_chart(filename):
    path = os.path.join(CHART_DIR, filename)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path

# =====================
# WYKRESY
# =====================

def generate_goals_chart():
    goals = como_df.groupby("opponent")["goals_scored"].sum().sort_values(ascending=False)

    plt.figure(figsize=(12, 6))
    goals.plot(kind="bar")

    plt.title("Gole Como vs rywale")
    plt.ylabel("Gole")

    save_chart("goals.png")


def generate_points_chart():
    points = como_df.groupby("opponent")["points"].sum().sort_values(ascending=False)

    plt.figure(figsize=(12, 6))
    points.plot(kind="bar")

    plt.title("Punkty Como vs rywale")
    plt.ylabel("Punkty")

    save_chart("points.png")


def generate_possession_chart():
    possession = como_df.groupby("opponent")["possession"].mean().sort_values(ascending=False)

    plt.figure(figsize=(12, 6))
    possession.plot(kind="bar")

    plt.axhline(y=50, linestyle="--")

    plt.title("Posiadanie piłki Como")
    plt.ylabel("%")

    save_chart("possession.png")


def generate_efficiency_chart():
    stats = como_df.groupby("opponent").agg({
        "shots_on_target": "mean",
        "goals_scored": "mean"
    })

    plt.figure(figsize=(10, 8))

    plt.scatter(
        stats["shots_on_target"],
        stats["goals_scored"],
        s=120
    )

    for opponent in stats.index:
        plt.annotate(
            opponent,
            (
                stats.loc[opponent, "shots_on_target"],
                stats.loc[opponent, "goals_scored"]
            )
        )

    plt.xlabel("Strzały celne")
    plt.ylabel("Gole")
    plt.title("Skuteczność Como")

    save_chart("efficiency.png")


def generate_goal_diff_chart():
    temp = como_df.copy()
    temp["goal_diff"] = temp["goals_scored"] - temp["goals_conceded"]

    diff = temp.groupby("opponent")["goal_diff"].sum().sort_values()

    plt.figure(figsize=(12, 6))
    diff.plot(kind="barh")

    plt.title("Bilans bramkowy Como")
    plt.xlabel("Bilans")

    save_chart("goal_diff.png")

# =====================
# ROUTES
# =====================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/goals")
def goals():
    generate_goals_chart()
    return render_template("chart.html", image="charts/goals.png", title="Gole")


@app.route("/points")
def points():
    generate_points_chart()
    return render_template("chart.html", image="charts/points.png", title="Punkty")


@app.route("/possession")
def possession():
    generate_possession_chart()
    return render_template("chart.html", image="charts/possession.png", title="Posiadanie")


@app.route("/efficiency")
def efficiency():
    generate_efficiency_chart()
    return render_template("chart.html", image="charts/efficiency.png", title="Skuteczność")


@app.route("/goal-diff")
def goal_diff():
    generate_goal_diff_chart()
    return render_template("chart.html", image="charts/goal_diff.png", title="Bilans")


# =====================
# START
# =====================

if __name__ == "__main__":
    app.run(debug=True)