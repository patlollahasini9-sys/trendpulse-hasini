import pandas as pd
import matplotlib.pyplot as plt
import os


# Load the analysed data created in Task 3
df = pd.read_csv("data/trends_analysed.csv")

# Create the outputs folder if it does not exist
os.makedirs("outputs", exist_ok=True)


# ============================================================
# CHART 1: TOP 10 STORIES BY SCORE
# ============================================================

# Select the 10 stories with the highest scores
top_stories = df.nlargest(10, "score").copy()

# Shorten titles longer than 50 characters
top_stories["short_title"] = top_stories["title"].apply(
    lambda title: title[:50] + "..." if len(title) > 50 else title
)

plt.figure(figsize=(10, 6))

plt.barh(
    top_stories["short_title"],
    top_stories["score"]
)

# Put the highest scoring story at the top
plt.gca().invert_yaxis()

plt.title("Top 10 Stories by Score")
plt.xlabel("Score")
plt.ylabel("Story Title")

plt.tight_layout()

# Save before showing the chart
plt.savefig("outputs/chart1_top_stories.png")

plt.show()
plt.close()


# ============================================================
# CHART 2: STORIES PER CATEGORY
# ============================================================

category_counts = df["category"].value_counts()

plt.figure(figsize=(8, 5))

# Use a different colour for each bar
plt.bar(
    category_counts.index,
    category_counts.values,
    color=[
        "steelblue",
        "orange",
        "green",
        "red",
        "purple"
    ]
)

plt.title("Stories per Category")
plt.xlabel("Category")
plt.ylabel("Number of Stories")

plt.xticks(rotation=20)

plt.tight_layout()

# Save before showing
plt.savefig("outputs/chart2_categories.png")

plt.show()
plt.close()


# ============================================================
# CHART 3: SCORE VS COMMENTS
# ============================================================

plt.figure(figsize=(8, 6))

# Separate popular and non-popular stories
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]


# Plot non-popular stories
plt.scatter(
    not_popular["score"],
    not_popular["num_comments"],
    label="Not Popular"
)


# Plot popular stories
plt.scatter(
    popular["score"],
    popular["num_comments"],
    label="Popular"
)

plt.title("Score vs Comments")
plt.xlabel("Score")
plt.ylabel("Number of Comments")

plt.legend()

plt.tight_layout()

# Save before showing
plt.savefig("outputs/chart3_scatter.png")

plt.show()
plt.close()


# ============================================================
# BONUS: COMBINED DASHBOARD
# ============================================================

fig, axes = plt.subplots(2, 2, figsize=(16, 10))

fig.suptitle("TrendPulse Dashboard", fontsize=18)


# Dashboard Chart 1
axes[0, 0].barh(
    top_stories["short_title"],
    top_stories["score"]
)

axes[0, 0].invert_yaxis()

axes[0, 0].set_title("Top 10 Stories by Score")
axes[0, 0].set_xlabel("Score")
axes[0, 0].set_ylabel("Story Title")


# Dashboard Chart 2
axes[0, 1].bar(
    category_counts.index,
    category_counts.values,
    color=[
        "steelblue",
        "orange",
        "green",
        "red",
        "purple"
    ]
)

axes[0, 1].set_title("Stories per Category")
axes[0, 1].set_xlabel("Category")
axes[0, 1].set_ylabel("Number of Stories")


# Dashboard Chart 3
axes[1, 0].scatter(
    not_popular["score"],
    not_popular["num_comments"],
    label="Not Popular"
)

axes[1, 0].scatter(
    popular["score"],
    popular["num_comments"],
    label="Popular"
)

axes[1, 0].set_title("Score vs Comments")
axes[1, 0].set_xlabel("Score")
axes[1, 0].set_ylabel("Number of Comments")
axes[1, 0].legend()


# Leave the fourth dashboard section empty
axes[1, 1].axis("off")


plt.tight_layout()

# Save the complete dashboard
plt.savefig("outputs/dashboard.png")

plt.show()
plt.close()


print("\nAll charts created successfully!")

print("Saved:")
print("  outputs/chart1_top_stories.png")
print("  outputs/chart2_categories.png")
print("  outputs/chart3_scatter.png")
print("  outputs/dashboard.png")