import time
import scrapy
from chocolate.items import ChocolateItem
from chocolate.itemloader import ChocolateItemLoader

class ChocolatespiderSpider(scrapy.Spider):
    start_time = time.time()
    name = "chocolatespider"
    allowed_domains = ["chocolate.co.uk"]
    start_urls = [
        "https://www.chocolate.co.uk/collections/all-products"
    ]

    def parse(self, response):
        products = response.css("product-item")
        productItem = ChocolateItem()
        for product in products:
            chocolate = ChocolateItemLoader(item= ChocolateItem(), selector=product)
            chocolate.add_css('name', 'a.product-item-meta__title::text'),
            chocolate.add_css('price', 'span.price', re='<span class="price">\n              <span class="visually-hidden">Sale price</span>(.*)</span>'),
            chocolate.add_css('url', 'div.product-item-meta a::attr(href)')
            yield chocolate.load_item()
        nextPage = response.css('a[rel="next"] ::attr(href)').get()
        if nextPage is not None:
            nextPageURL = "https://www.chocolate.co.uk" + nextPage
            yield response.follow(nextPageURL, callback=self.parse)
        print("--- %s seconds ---" % round(time.time() - self.start_time, 3))