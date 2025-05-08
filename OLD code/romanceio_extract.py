from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time

# note: this is OLD code -- originally using romance.io. only works for 1 instance
def get_book_details(book_url):
    """Extracts book details (title, author, tropes, description) from the individual book page."""
    
    # Setup Selenium WebDriver
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Navigate to the page
    driver.get(book_url)
    
    # Explicit wait for the page to load the book title
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "book-info"))
        )
    except Exception as e:
        print(f"Error loading page: {e}")
        driver.quit()
        return None, None, None, None

    # Allow additional time if needed
    time.sleep(5)

    # Extract page source after JavaScript content loads
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Extract title and author
    title = soup.find("div", class_="book-info").find("h1").text.strip() if soup.find("div", class_="book-info") else "Unknown"
    author_tag = soup.find("h2", class_="author")
    author = author_tag.text.strip() if author_tag else "Unknown"

    # Extract description
    description_tag = soup.find("div", id="book-description")
    description = description_tag.text.strip() if description_tag else "No description available"

    # Clean up description
    description = description.replace("\n", " ").strip()

    # Extract tropes from the list
    tropes = []
    topics_list = soup.find("ul", id="valid-topics-list", class_="list-unstyled topic-tags topic-tags-vote is-clearfix")
    if topics_list:
        for topic in topics_list.find_all("li", class_="tagged-topic"):
            trope = topic.get("data-link", "Unknown Tropes")
            tropes.append(trope)
    tropes = ", ".join(tropes) if tropes else "No tropes found"

    # Close the browser after scraping
    driver.quit()

    return title, author, tropes, description

# Example book URL (adjust with the actual book URL)
book_url = "https://www.romance.io/books/5484ecd47a5936fb0405756c/pride-and-prejudice-jane-austen"
title, author, tropes, description = get_book_details(book_url)

print(f"Title: {title}")
print(f"Author: {author}")
print(f"Tropes: {tropes}")
print(f"Description: {description}")
