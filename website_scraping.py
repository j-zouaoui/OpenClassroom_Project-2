# import labraries
import requests
from bs4 import BeautifulSoup
import urllib.parse
import csv
import os
import shutil  


#specify the url of the web site
url = "http://books.toscrape.com/"

#query the web site and extract html
page = requests.get(url)

#parse the html line
soup = BeautifulSoup(page.content,'html.parser')
a_tags = soup.find_all("a", href=lambda href: href and "catalogue/category/books/" in href)

# extract the category  data
# For loop that iterates over all the <a> tags
urls = []
for a_tag in a_tags:

    try:
        # looking for href inside anchor tag
        if 'href' in a_tag.attrs:
            # storing the value of href in a separate
            # variable
            url_ext = a_tag.get('href')
            category_href = urllib.parse.urljoin(url, url_ext)
            # appending the url to the output list
            print(category_href)
            urls.append(category_href)

    # if the list does not has a anchor tag or an anchor
    # tag does not has a href params we pass
    except:
        pass
# getting current directory
cwd = os.getcwd()

# for loop that iterates over all the category to extract books information
for url_category in urls:

    #specify the catalogue web page url
    url_catalogue_page = url_category

    #query the web site to get the html
    try:
        page = requests.get(url_catalogue_page)
    except:
        print("Not possible to connect to the web page")

    #parse the html using BeautifulSoup
    soup = BeautifulSoup(page.content, 'html.parser')

    #extract Books section
    list = soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

    #extract links
    books_href_links = []
    for element in list:
        a_href = element.find('a')
        href_ext= a_href.get('href')
        book_href = urllib.parse.urljoin(url_catalogue_page,href_ext)
        books_href_links.append(book_href)

    #creating a csv data list with the column
    csv_row_list = [["product_page_url","Universal product code (upc)", "Title", "Price including tax", "Price excluding_tax",
                    "Number available", "Product description", "Category", "Review rating", "Image url"]]

    #creating a specific folder to save pictures of all the category books
    path = "Downloads_pictures/"
    dir_path = os.path.join(cwd, path)
    
    # Create folders if not exist
    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    except OSError:
        print("Error")

    #for loop that iterates over all the books of the specific category
    for booklink in books_href_links:

        #specify the book url
        url_book_page =booklink

        # query the website and return the html to the variable web page
        try:
            page = requests.get(url_book_page)
        except:
            print("not possible to connect to the requested webpage")

        #parse the html using the Beautiful soup and store in variable soup
        soup = BeautifulSoup(page.content, 'html.parser')

        #find the book title and product description
        title = soup.find("div", class_="col-sm-6 product_main").find("h1").text

        # rating 
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
        image_url = urllib.parse.urljoin(url_book_page, image_url_ext)
        
        #save image in download picture folder
        os.chdir(dir_path)
        filename = image_url.split("/")[-1]

        # Open the url image, set stream to True, this will return the stream content.
        r = requests.get(image_url, stream=True)

        # Check if the image was retrieved successfully
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True

            # Open a local file with wb ( write binary ) permission.
            with open(filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

            print('Image sucessfully Downloaded: ', filename)
        else:
            print('Image Couldn\'t be retreived')

        # find the production description
        article = soup.find("article", class_="product_page")
        paragraphes = article.find_all("p", recursive=False)
        try:
            product_description = paragraphes[0].text
        except:
            production_description = "not possible to get description"
            pass
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

    # added book information to the csv data list
        csv_row_list.append([url_book_page, universal_product_code, title, price_including_tax, price_excluding_tax,
                    number_available, product_description, category, review_rating, image_url])

    
    os.chdir('../')
    # create a csv file and write rows to output file
    with open("%s_data_book.csv" % category, 'w+', newline='', encoding="utf-8") as csv_file:
        datawiter = csv.writer(csv_file,)
        datawiter.writerows(csv_row_list)
    print("%s_data_book.txt has been crated" % category)









