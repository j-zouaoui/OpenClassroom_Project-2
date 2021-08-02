# import labraries
import requests
from bs4 import BeautifulSoup
import urllib.parse
import csv

#specify the url
urlpage ="http://books.toscrape.com/catalogue/you-are-what-you-love-the-spiritual-power-of-habit_872/index.html"

# query the website and return the html to the variable web page

try:
    page = requests.get(urlpage)
except:
    print("not possible to connect to the requested webpage")

#parse the html using the Beautiful soup and store in variable soup
soup = BeautifulSoup(page.content, 'html.parser')

#find the book title and product description
title = soup.find("div", class_="col-sm-6 product_main").find("h1").text

# rating (try to find another way to reduce the code line / the select should be tested)
section = soup.find("div", class_="col-sm-6 product_main")
rating_1 = section.find("p", class_="star-rating One")
rating_2 = section.find("p", class_="star-rating Two")
rating_3 = section.find("p", class_="star-rating Three")
rating_4 = section.find("p", class_="star-rating Four")
rating_5 = section.find("p", class_="star-rating Five")
review_rating = 0
if rating_1 != None:
    review_rating = 1
elif rating_2 !=None:
    review_rating = 2
elif rating_3 !=None:
    review_rating = 3
elif rating_4 !=None:
    review_rating = 4
elif rating_5 !=None:
    review_rating = 5



#find results within the table
table = soup.find("table", class_="table table-striped")
results = table.find_all("tr")
table_data = []
for result in results:
    data = result.find("td")
    table_data.append(data)

universal_product_code = table_data[0].getText()
price_excluding_tax = table_data[2].getText()
price_including_tax = table_data[3].getText()
number_available = table_data[5].getText()
number_of_reviews = table_data[6].getText()

#find the image url's
image_section = soup.find("div", class_="col-sm-6")
image = image_section.find("img")

# use the .attrs method to pull out the URL found in src=
image_url_ext = image.attrs['src']
image_url = urllib.parse.urljoin(urlpage, image_url_ext)

# find the production description
article = soup.find("article", class_="product_page")
paragraphes = article.find_all("p", recursive=False)
product_description = paragraphes[0].text
#find the book category
list_ul = soup.find("ul", class_="breadcrumb")

# Create top_items as empty list
all_links = []

links = list_ul.select('a')
for ahref in links:
    text = ahref.text
    text = text.strip() if text is not None else ''
    all_links.append(text)

category = all_links[-1]

# create a csv file and write rows to output file

csv_row_list = [["product_page_url","Universal product code (upc)", "Title", "Price including tax", "Price excluding_tax",
            "Number available", "Product description", "Category", "Review rating", "Image url"],
                [urlpage, universal_product_code, title, price_including_tax, price_excluding_tax,
            number_available, product_description, category, review_rating, image_url]]
with open("Data_book.txt", 'w+', newline='') as csv_file:
    datawiter = csv.writer(csv_file,)
    datawiter.writerows(csv_row_list)

#test
"""print("Book title: ", title)
print("Universal product code: ", universal_product_code)
print("Review rating: ", review_rating)
print("Price excluding tax:", price_excluding_tax)
print("Price including tax: ", price_including_tax)
print("Number available: ", number_available)
print("Number of reviews: ", number_of_reviews)
print("The url of the image: ", image_url)
print(paragraphes[0].text)"""




