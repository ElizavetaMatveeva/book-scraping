import sqlite3
import requests
from bs4 import BeautifulSoup


# Scraping books from the website
def scrape_books(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article")
    all_books = []
    for book in books:
        book_data = (get_title(book), get_price(book), get_rating(book))
        all_books.append(book_data)
    save_books(all_books)


# Saving books to a database
def save_books(all_books):
    connection = sqlite3.connect("books.db")
    c = connection.cursor()
    c.execute('''CREATE TABLE books 
        (title TEXT, price REAL, rating INTEGER)''')
    c.executemany("INSERT INTO books VALUES(?,?,?)", all_books)
    connection.commit()
    connection.close()


# Extracting books title
def get_title(book):
    return book.find("h3").find("a")["title"]


# Extracting book price
def get_price(book):
    price = book.find(class_="price_color").get_text()
    return float(price.replace("£", "").replace("Â", ""))


# Extracting book rating and converting it to a number
def get_rating(book):
    word_rating = book.find(class_="star-rating").get_attribute_list("class")[-1]
    ratings = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    return ratings[word_rating]


scrape_books("http://books.toscrape.com/catalogue/category/books/history_32/index.html")
