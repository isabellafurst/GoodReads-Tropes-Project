from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv

# Function to scrape book URLs from the category page
def get_book_links(page_url):
    """Scrape book URLs from the category page."""
    
    # Setup Selenium WebDriver
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Navigate to the page
    driver.get(page_url)
    
    # Wait for the page to load
    try:
        WebDriverWait(driver, 20).until(  # Increased wait time to 20 seconds
            EC.presence_of_all_elements_located((By.CLASS_NAME, "result"))
        )
    except Exception as e:
        print(f"Error loading page with books: {e}")
        driver.quit()
        return []

    # Sleep a bit to ensure that JavaScript has fully rendered the page
    time.sleep(3)  # Adjust the time if needed
    
    # Extract page source after the page has loaded
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Find all book links on the page
    book_links = []
    for book in soup.find_all("a", class_="img-holder"):
        book_url = "https://www.romance.io" + book.get("href", "")
        book_links.append(book_url)
    
    # Close the browser after scraping
    driver.quit()
    
    return book_links

# Function to extract book details (title, author, tropes, description) from the book page
def get_book_details(book_url):
    """Extracts book details from the individual book page."""
    
    # Setup Selenium WebDriver
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Navigate to the page
    driver.get(book_url)
    
    # Wait for the page to load the book title
    try:
        WebDriverWait(driver, 20).until(  # Increased wait time to 20 seconds
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

# Write data to CSV file
with open("romance_books.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Author", "Tropes", "Description"])  # Write the header row

    # Loop through the book URLs and extract details
    all_book_urls = []
    for page_number in range(1, 6):  # Scrape first 5 pages
        page_url = f"https://www.romance.io/topics/bestof-2025/all/{page_number}"
        print(f"Scraping page {page_number}...")
        
        # Get book URLs from the current page
        book_links = get_book_links(page_url)
        all_book_urls.extend(book_links)
        
    # Loop through all book URLs and scrape details
    for book_url in all_book_urls:
        print(f"Scraping {book_url}...")
        title, author, tropes, description = get_book_details(book_url)
        
        if title and author:
            writer.writerow([title, author, tropes, description])

        # Human-like delay between each book scraping
        time.sleep(2)  # Adjust the delay as needed

print("Data saved to 'romance_books.csv'.")
