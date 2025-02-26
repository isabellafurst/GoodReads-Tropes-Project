from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import random

# aided from:
# https://www.codecademy.com/article/web-scrape-with-selenium-and-beautiful-soup
# https://www.youtube.com/watch?v=pPBUWJfquzs

def scrape_goodreads(base_url, n_pages=5): #adjust n_pages if you want to increase the # of books in the output CSV file
    """
    Scrapes Goodreads for books. Romance books for now. Might change later.
    n_pages defaults to 5 (total of 250 titles). change if you need more, but note: each page contains 50 book titles
    """

    options = webdriver.ChromeOptions() 
    # REF: https://www.selenium.dev/documentation/webdriver/browsers/chrome/, https://peter.sh/experiments/chromium-command-line-switches/
    options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
    
    # spin up the browser
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    books = []
    
    for i in range(n_pages):
        page = i + 1
        url = f"{base_url}?page={page}"
        print(f"Loading up {page}: {url}")
        driver.get(url)
    
        try:
            WebDriverWait(driver, 8).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "bookTitle"))
            )
        except Exception as e:
            print(f"Errror with page {page}: {e}")
            continue
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        num_books = soup.find_all("a", class_="bookTitle")
        if not num_books:  
            print(f"no books found on page {page} :(")  
        else:  
            print(f"Successfully found {len(num_books)} books on page {page}")

        
        for book in num_books:  
            title = book.text.strip()  
            link = "https://www.goodreads.com" + book.get("href", "") if book.get("href") else "no link found"  
            author_tag = book.find_next("span", itemprop="name")  
            author = author_tag.text.strip() if author_tag else "author is unknown/was not found"  
            books.append((title, author, link))
        
        sleep = random.uniform(2, 7) # more stuff to prevent being flagged as bot
        print(f"taking a quick break: {sleep} seconds")
        time.sleep(sleep)
    
    driver.quit()
    return books

# run the scraper
romance_shelf = "https://www.goodreads.com/shelf/show/romance" # this could be adjusted to run similar analyses for non-romance genres to see popular subgenres
books = scrape_goodreads(romance_shelf, n_pages=5)

# save the outputs
with open("goodreads_bookList.txt", "w") as file:
    for title, author, link in books:
        file.write(f"{title} by {author} - {link}\n")

print(f"all done!!! final output: goodreads_bookList.txt")
