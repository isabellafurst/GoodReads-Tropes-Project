Romance Book Tropes Scraper

Overview:
This is a personal project that scrapes romance book data from Goodreads, extracts genre/trope information, and analyzes the most common tropes used in romance books. 
It consists of three main scripts:
1. url_scraper.py : scrapes book titles, authors, and links from Goodreads
2. genres_scraper.py : extracts the genre/trope information from the book URL pages
3. analysis.py : use basic ML to analyze and visalize the most common tropes that appear

Dependencies:
For this to run, you need to have the following installed on your machine/environment:
- Python 3.x
- selenium
- webdriver_manager
- beautifulsoup4
- pandas
- matplotlib

They're all in requirements.txt, and can be installed by running:
pip install -r requirements.txt

How It Works:
1. Scraping Book Data
Run url_scraper.py to scrape book titles, authors, and Goodreads links from the romance shelf
    Output: goodreads_romance_books.txt

2. Extracting Genres/Tropes
Run genres_scraper.py to visit each book page and extract genre/trope data.
    Output: books_with_genres.csv

3. Analyzing Tropes
Run analysis.py to generate insights from the extracted data.
    Outputs:trope_analysis.csv` (CSV file with trope counts), bar chart of the top 15 most common tropes, pie chart of the top 10 tropes

Some comments about the implementation:
- Uses Selenium to handle JavaScript-rendered Goodreads pages.
- Implements randomized delays and rotating user agents to reduce the chance of getting blocked.
- Saves extracted data for debugging (`debug/debug_selenium.html`).
- Filters out the "romance" tag since all books belong to this genre by default.
- This script was written such that url_scraper.py makes it easy to switch the genre if you want to look at the subgenres for a non-romance category (or "shelf")
