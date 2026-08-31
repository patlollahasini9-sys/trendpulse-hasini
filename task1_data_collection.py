import requests
import json
import os
import time
from datetime import datetime


# Header added to every API request
headers = {
    "User-Agent": "TrendPulse/1.0"
}


# Keywords used to classify Hacker News stories
categories = {
    "technology": [
        "ai", "software", "tech", "code", "computer",
        "data", "cloud", "api", "gpu", "llm"
    ],

    "worldnews": [
        "war", "government", "country", "president",
        "election", "climate", "attack", "global"
    ],

    "sports": [
        "nfl", "nba", "fifa", "sport", "game",
        "team", "player", "league", "championship"
    ],

    "science": [
        "research", "study", "space", "physics",
        "biology", "discovery", "nasa", "genome"
    ],

    "entertainment": [
        "movie", "film", "music", "netflix",
        "game", "book", "show", "award", "streaming"
    ]
}


# This function checks which category matches the story title
def get_category(title):
    title = title.lower()

    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in title:
                return category

    return None


# URL for getting the top story IDs
top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"


try:
    response = requests.get(
        top_stories_url,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    # Get only the first 500 story IDs
    story_ids = response.json()[:500]

except requests.RequestException as error:
    print("Failed to fetch top stories:", error)
    story_ids = []


# Dictionary to store how many stories are collected per category
category_count = {
    "technology": 0,
    "worldnews": 0,
    "sports": 0,
    "science": 0,
    "entertainment": 0
}


# List to store the final collected stories
all_stories = []


# Loop through the categories
for category in categories:

    print(f"\nCollecting {category} stories...")

    # Wait 2 seconds between category loops
    time.sleep(2)

    # Check all available story IDs
    for story_id in story_ids:

        # Stop when 25 stories are collected for this category
        if category_count[category] >= 25:
            break

        # URL for one specific Hacker News story
        item_url = (
            f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        )

        try:
            response = requests.get(
                item_url,
                headers=headers,
                timeout=30
            )

            response.raise_for_status()

            story = response.json()

        except requests.RequestException as error:
            print(f"Failed to fetch story {story_id}: {error}")
            continue


        # Skip if the story data is empty
        if not story:
            continue


        # Get the title safely
        title = story.get("title", "")


        # Check whether the title belongs to the current category
        detected_category = get_category(title)

        if detected_category != category:
            continue


        # Create a dictionary with the 7 required fields
        story_data = {
            "post_id": story.get("id"),
            "title": title,
            "category": category,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by", "unknown"),
            "collected_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }


        # Add the story to the final list
        all_stories.append(story_data)

        # Increase the category count
        category_count[category] += 1


# Create the data folder if it does not already exist
os.makedirs("data", exist_ok=True)


# Create a file name using today's date
date_today = datetime.now().strftime("%Y%m%d")

file_name = f"data/trends_{date_today}.json"


# Save all collected stories into the JSON file
with open(file_name, "w", encoding="utf-8") as file:
    json.dump(
        all_stories,
        file,
        indent=4,
        ensure_ascii=False
    )


# Print the final result
print("\nCollection completed!")

print(f"Collected {len(all_stories)} stories.")
print(f"Saved to {file_name}")

print("\nStories collected per category:")

for category, count in category_count.items():
    print(f"{category}: {count}")