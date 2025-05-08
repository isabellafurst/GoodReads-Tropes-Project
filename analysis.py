import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

#NOTE: might also be good to consider excluding "fiction" as a genre -- most common trope but seemingly obvious?

# load csv file w/ book data
df = pd.read_csv("books_with_genres.csv")

# get every trope out of the 'Tropes' column and clean it up a bit.
all_tropes = []
for tropes in df["Tropes"]:  
    tropes_list = tropes.split(", ")  # Split tropes by comma
    filtered_tropes = [t for t in tropes_list if t.lower() != "romance"]  # remove any "romance" tropes because, like, every book is romance, so it's kinda redundant
    all_tropes.extend(filtered_tropes)

# count how many times each trope shows up! -- helps figure out figure out which ones are the most common
trope_counts = Counter(all_tropes)

trope_df = pd.DataFrame(trope_counts.items(), columns=["Trope", "Count"])
trope_df = trope_df.sort_values(by="Count", ascending=False)

print("Top 10 Most Common Tropes:")
print(trope_df.head(10))

# horizontal bar chart to show the top 15 most common tropes
plt.figure(figsize=(12, 6))
plt.barh(trope_df["Trope"][:15], trope_df["Count"][:15], color="royalblue")
plt.xlabel("Count", fontsize=12)
plt.ylabel("Trope", fontsize=12)
plt.title("Top 15 Most Common Tropes in Romance Books", fontsize=14, fontweight="bold")
plt.gca().invert_yaxis()  # want the biggest trope on top so flip the axis
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.show()

# pie chart for the top 10 tropes for funsies
plt.figure(figsize=(8, 8))
plt.pie(
    trope_df["Count"][:10],
    labels=trope_df["Trope"][:10],
    autopct="%1.1f%%",
    colors=plt.cm.Paired.colors,
    wedgeprops={"edgecolor": "black"},
)
plt.title("Top 10 Tropes Distribution", fontsize=14, fontweight="bold")
plt.show()

# Save the analyzed trope data to a new CSV file
trope_df.to_csv("trope_analysis.csv", index=False)

print("finished analyzing!! Tropes data saved to 'trope_analysis.csv'")
