import scrapy
from scrapy_splash import SplashRequest
from pymongo import MongoClient
from scrapy.crawler import CrawlerProcess


class ImageItem(scrapy.Item):
    type_ = scrapy.Field()  # 漫画类型
    title = scrapy.Field()  # 漫画名称
    image_urls = scrapy.Field()
    page = scrapy.Field()  # 漫画页数


class DownloadimagesSpider(scrapy.Spider):
    name = 'downloadimages'
    custom_settings = {
        # "ROBOTSTXT_OBEY": False,
        "IMAGES_STORE": '/home/clay/Pictures/images_',
        "IMAGES_EXPIRES": 30,
        'RETRY_HTTP_CODES': [401, 403, 500, 502, 503, 504],
        'RETYR_TIMES': 5,
        'DELTAFETCH_ENABLED': True,
        'SPLASH_URL': 'http://127.0.0.1:8050',
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
        'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage',
        'SPIDER_MIDDLEWARES': {
            'scrapy_deltafetch.DeltaFetch': 100,
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 101,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        },
        'ITEM_PIPELINES': {
            'manhua.pipelines.SaveImagesPipeline': 300,
        }
    }

    host = 'localhost'
    port = 27017
    db = "mh"
    client = MongoClient(host=host, port=port)
    databases = client[db]
    collections = databases['cm']

    def start_requests(self):
        item = ImageItem()
        for data in self.collections.find():
            item["type_"] = data.get('type_')
            item["title"] = data.get('title').replace('/', '_')
            books = data.get('books')
            for book in books:
                for k, link in book.items():
                    item['page'] = k
                    yield SplashRequest(url=link, callback=self.image_parse,
                                        args={'wait': 1.5, 'proxy': 'http://172.17.0.2:7890'}, endpoint='render.html',
                                        meta=dict(item=item))

    def image_parse(self, response):
        # pass
        item = response.meta.get('item')
        images = response.xpath('//article[@class="article-content"]/p//img/@src').getall()
        item['image_urls'] = images
        yield item

