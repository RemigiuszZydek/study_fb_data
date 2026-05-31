import pandas as pd
import matplotlib.pyplot as plt

# =====================
# Wczytanie danych
# =====================

df = pd.read_csv("matches.csv")

df["match_date"] = pd.to_datetime(df["match_date"])

# =====================
# Tylko Como 1907
# =====================

como_df = df[
    (df["home_team"] == "Como 1907") |
    (df["away_team"] == "Como 1907")
].copy()

# gole zdobyte

como_df["goals_scored"] = como_df.apply(
    lambda row:
    row["home_score"]
    if row["home_team"] == "Como 1907"
    else row["away_score"],
    axis=1
)

# gole stracone

como_df["goals_conceded"] = como_df.apply(
    lambda row:
    row["away_score"]
    if row["home_team"] == "Como 1907"
    else row["home_score"],
    axis=1
)

# strzały celne

como_df["shots_on_target"] = como_df.apply(
    lambda row:
    row["home_shots_on_target"]
    if row["home_team"] == "Como 1907"
    else row["away_shots_on_target"],
    axis=1
)

# posiadanie

como_df["possession"] = como_df.apply(
    lambda row:
    row["home_possession"]
    if row["home_team"] == "Como 1907"
    else row["away_possession"],
    axis=1
)

# przeciwnik

como_df["opponent"] = como_df.apply(
    lambda row:
    row["away_team"]
    if row["home_team"] == "Como 1907"
    else row["home_team"],
    axis=1
)

# punkty

def calculate_points(row):

    if row["goals_scored"] > row["goals_conceded"]:
        return 3

    if row["goals_scored"] == row["goals_conceded"]:
        return 1

    return 0


como_df["points"] = como_df.apply(
    calculate_points,
    axis=1
)

# =====================
# WYKRES 1
# Gole przeciwko rywalom
# =====================

def plot_goals():

    goals = (
        como_df
        .groupby("opponent")["goals_scored"]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(12, 6))

    goals.plot(kind="bar")

    plt.title("Gole zdobyte przez Como przeciwko rywalom")
    plt.ylabel("Liczba goli")

    plt.tight_layout()
    plt.show()


# =====================
# WYKRES 2
# Punkty przeciwko rywalom
# =====================

def plot_points():

    points = (
        como_df
        .groupby("opponent")["points"]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(12, 6))

    points.plot(kind="bar")

    plt.title("Punkty zdobyte przez Como")
    plt.ylabel("Punkty")

    plt.tight_layout()
    plt.show()


# =====================
# WYKRES 3
# Średnie posiadanie
# =====================

def plot_possession():

    possession = (
        como_df
        .groupby("opponent")["possession"]
        .mean()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(12, 6))

    possession.plot(kind="bar")

    plt.axhline(
        y=50,
        linestyle="--"
    )

    plt.title("Średnie posiadanie piłki Como")
    plt.ylabel("%")

    plt.tight_layout()
    plt.show()


# =====================
# WYKRES 4
# Skuteczność
# =====================

def plot_efficiency():

    stats = (
        como_df
        .groupby("opponent")
        .agg({
            "shots_on_target": "mean",
            "goals_scored": "mean"
        })
    )

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

    plt.xlabel("Średnie strzały celne")
    plt.ylabel("Średnie gole")

    plt.title("Skuteczność Como przeciwko rywalom")

    plt.tight_layout()
    plt.show()


# =====================
# WYKRES 5
# Bilans bramkowy
# =====================

def plot_goal_difference():

    temp = como_df.copy()

    temp["goal_difference"] = (
        temp["goals_scored"]
        - temp["goals_conceded"]
    )

    diff = (
        temp
        .groupby("opponent")["goal_difference"]
        .sum()
        .sort_values()
    )

    plt.figure(figsize=(12, 6))

    diff.plot(kind="barh")

    plt.title("Bilans bramkowy Como przeciwko rywalom")
    plt.xlabel("Bilans bramkowy")

    plt.tight_layout()
    plt.show()


# =====================
# URUCHOMIENIE
# =====================

plot_goals()
plot_points()
plot_possession()
plot_efficiency()
plot_goal_difference()