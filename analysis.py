import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv("books_with_genres.csv")

# Extract and process tropes
all_tropes = []
for tropes in df["Tropes"]:  
    tropes_list = tropes.split(", ")  # Split tropes by comma
    filtered_tropes = [t for t in tropes_list if t.lower() != "romance"]  # Remove "romance"
    all_tropes.extend(filtered_tropes)

# Count trope occurrences
trope_counts = Counter(all_tropes)

# Convert to DataFrame for easy manipulation
trope_df = pd.DataFrame(trope_counts.items(), columns=["Trope", "Count"])
trope_df = trope_df.sort_values(by="Count", ascending=False)

# Display the top 10 most common tropes
print("Top 10 Most Common Tropes:")
print(trope_df.head(10))

# Horizontal Bar Chart (Improved Readability)
plt.figure(figsize=(12, 6))
plt.barh(trope_df["Trope"][:15], trope_df["Count"][:15], color="royalblue")
plt.xlabel("Count", fontsize=12)
plt.ylabel("Trope", fontsize=12)
plt.title("Top 15 Most Common Tropes in Romance Books", fontsize=14, fontweight="bold")
plt.gca().invert_yaxis()  # Invert axis for better readability
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.show()

# 2️Pie Chart for Top 10 Tropes
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

print("Analysis complete! Tropes data saved to 'trope_analysis.csv'")
