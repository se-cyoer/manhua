# import scrapy
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
#
#
# class SaveImage(scrapy.Spider):
#     name = 'test'
#     start_urls = ['https://www.3004aa.vip/648501.html']
#     custom_settings = {
#         'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122"
#                       " UBrowser/4.0.3214.0 Safari/537.36"
#     }
#
#     def parse(self, response, **kwargs):
#         print(response.text)
#         images = response.css('article.article-content p:nth-child(1) img')
#         for image in images:
#             yield {
#                 image.css('::atr(alt)').get(): image.css('::attr(src)').get()
#
#             }
#
#
# process = CrawlerProcess()
# process.crawl(SaveImage)
# process.start()
