import scrapy
from scrapy import Item, Field
import re


class ManhuaItem(Item):
    type_ = Field()
    title = Field()
    link = Field()
    books = Field()
    finish = Field()


class A34aSpider(scrapy.Spider):
    name = '34a'
    start_urls = ['https://www.3004aa.vip/']
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 0.25,
        'CONCURRENT_REQUESTS': 10,
        'RETRY_HTTP_CODES': [401, 403, 500, 502, 503, 504],
        'RETYR_TIMES': 5,
        'REFERER_ENABLED': False,
        # 广度优先
        "DEPTH_PRIORITY": 1,
        "SCHEDULER_DISK_QUEUE": 'scrapy.squeues.PickleFifoDiskQueue',
        "SCHEDULER_MEMORY_QUEUE": 'scrapy.squeues.FifoMemoryQueue',
        # 增量爬取
        'SPIDER_MIDDLEWARES': {
            'scrapy_deltafetch.DeltaFetch': 100,
        },
        'DELTAFETCH_ENABLED': True,
    }

    def parse(self, response):
        # 解析主页面，并持续爬取所有的漫画页面
        all_s = response.css('div.pb>div')
        for one in all_s:
            item = ManhuaItem()
            book_url = one.css('header>h2>a::attr(href)').get()
            end = one.css('header>span::text').get()
            item['type_'] = one.css('header>p::text').get()
            item['title'] = one.css('header>h2>a::text').get()
            item['link'] = book_url
            if end:
                item['finish'] = True if end.startswith('完结') or end.startswith('精品') else False
            else:
                item['finish'] = False
            # 请求单本漫画url地址
            if book_url:
                yield scrapy.Request(url=book_url, callback=self.book_parse, cb_kwargs={'item': item})
        # 请求漫画书页面，通过回调方法持续获取页面中所有书籍的简略信息
        next_page = response.css('li.next-page>a::attr(href)').get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def book_parse(self, response, item):
        # pass
        # 解析单本漫画的所有章节
        item = item
        datas = list()
        datas.append({str(1): f"{response.url.split('.html')[0]}/page-1.html"})
        chapters = response.xpath('//article[@class="article-content"]/div[@class="article-paging"][1]//a')
        for chapter in chapters:
            link = chapter.xpath('./@href').get()
            is_num = re.compile(r'.*\d+$')
            if not is_num.findall(link):
                data = {
                    chapter.xpath('./span/text()').get(): link
                }
                datas.append(data)

        item['books'] = datas
        yield item
