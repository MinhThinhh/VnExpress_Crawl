import scrapy

class VnexpressItem(scrapy.Item):
    url = scrapy.Field()  
    title = scrapy.Field() 
    time = scrapy.Field() 
    author = scrapy.Field() 
    category = scrapy.Field() 
    content = scrapy.Field() 
    tags = scrapy.Field() 
    comments = scrapy.Field() 
    image_url = scrapy.Field() 
