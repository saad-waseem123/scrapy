import time
import scrapy
from FiverScraper.items import GigItem
from FiverScraper.itemloader import GigItemLoader
from urllib.parse import urlencode

API_KEY = 'aa5b300b-df79-4fd7-a4ab-929c6748f8d9'
def get_proxy_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url
    # return url

class GigSpiderSpider(scrapy.Spider):
    start_time = time.time()
    name = "gigspider"
    allowed_domains = ["fiverr.com"]
    baseURL = "https://www.fiverr.com"

    def start_requests(self):
        mymeta = { "page": 3, "keyword": "wordpress%20developer" }
        start_url = f"https://www.fiverr.com/search/gigs?query={mymeta['keyword']}&page={mymeta['page']}"
        yield scrapy.Request(url=get_proxy_url(start_url), callback=self.parse, meta=mymeta)

    def parse(self, response):
        elements = 0
        gigs = response.xpath('//div[@class="layout-row content-row"]/div/div[@class="gig_listings-package listing-container grid-view"]/div')
        for gig in gigs:
            elements += 1
            i = GigItemLoader(item= GigItem(), selector=gig)
            i.add_xpath('title', './/h3/a/text()'),
            i.add_xpath('level', 'normalize-space(.//div[@class="seller-info text-body-2"]/div/div/span)')
            i.add_xpath('rating', 'normalize-space(.//div[@class="rating-wrapper"]/span)')
            i.add_xpath('price', 'normalize-space(.//footer/a/span)')
            i.add_xpath('url', './/h3/a/@href'),
            yield i.load_item()
        
        if elements != 0:
            ## next page
            pageinc = response.meta['page']
            pageinc += 1
            response.meta['page'] = pageinc
            start_url = f"https://www.fiverr.com/search/gigs?query={response.meta['keyword']}&page={pageinc}"
            # print(f'########### {start_url}')
            yield response.follow(url=get_proxy_url(start_url), callback=self.parse, meta=response.meta)
            # yield scrapy.Request(url=get_proxy_url(start_url), callback=self.parse, meta=response.meta) 
        print("--- %s seconds ---" % round(time.time() - self.start_time, 3))