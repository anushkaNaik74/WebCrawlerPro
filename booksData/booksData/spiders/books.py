import scrapy
from pathlib import Path
from pymongo import MongoClient
client = MongoClient("mongodb+srv://anushkanaik47:Anushka2525@newproject.ztjulpt.mongodb.net/")
import datetime

def insertToDb(page, title, image, rating, price, instock):
    db = client.scrapy
    collection = db[page]
    doc = {
    "title": title,
    "image": image,
    "rating": rating,
    "price": price,
    "instock": instock,
    "date": datetime.datetime.now(tz=datetime.timezone.utc),
    }
    inserted = collection.insert_one(doc)
    return inserted.inserted_id

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["toscrape.com"]
    start_urls = ["https://toscrape.com"]

    def start_requests(self):
        urls = [
            "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
            "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"books-{page}.html"

        bookdetails = {}
        # For saving the content as file
        # Path(filename).write_bytes(response.body)


        self.log(f"Saved file {filename}")
        cards = response.css(".product_pod")
        for card in cards:
            title = card.css("h3>a::text").get()
            image = card.css(".image_container img")
            image = image.attrib["src"].replace("../../../../media", "https://books.toscrape.com/media")
            rating = card.css(".star-rating").attrib["class"].split(" ")[-1]
            price = card.css(".price_color::text").get()
            stock = card.css(".availability")
            # print(image.attrib["src"])
            # print(title)
            # print(rating)
            # print(price)
            if(len(stock.css(".icon-ok")) > 0):
                instock = True
            else:
                instock = False
            insertToDb(page, title, image, rating, price, instock)
