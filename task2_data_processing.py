import pandas as pd
import glob


# Find the JSON file created by Task 1
json_files = glob.glob("data/trends_*.json")

if not json_files:
    print("No JSON file found in the data folder.")
    exit()

json_file = json_files[0]


# Load the JSON data into a Pandas DataFrame
df = pd.read_json(json_file)

print(f"Loaded {len(df)} stories from {json_file}")


# Remove duplicate stories using post_id
df = df.drop_duplicates(subset="post_id")

print(f"After removing duplicates: {len(df)}")


# Remove rows where post_id, title, or score is missing
df = df.dropna(subset=["post_id", "title", "score"])

print(f"After removing nulls: {len(df)}")


# Convert score and num_comments into integers
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce")

# Remove rows that could not be converted to numbers
df = df.dropna(subset=["score", "num_comments"])

df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)


# Remove stories with score less than 5
df = df[df["score"] >= 5]

print(f"After removing low scores: {len(df)}")


# Remove extra spaces from story titles
df["title"] = df["title"].str.strip()


# Save the cleaned data as CSV
output_file = "data/trends_clean.csv"

df.to_csv(output_file, index=False)

print(f"\nSaved {len(df)} rows to {output_file}")


# Print number of stories in each category
print("\nStories per category:")

category_counts = df["category"].value_counts()

for category, count in category_counts.items():
    print(f"  {category:<15} {count}")