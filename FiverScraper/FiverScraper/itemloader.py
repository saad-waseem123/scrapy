from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst

class GigItemLoader(ItemLoader): 
    defualt_output_processor =  TakeFirst()
    # price_in = MapCompose(lambda x: x.split("$")[-1]) 
    url_in = MapCompose(lambda x: "https://www.fiverr.com" + x.split('?', 1)[0]) 