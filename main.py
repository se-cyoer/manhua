from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

crawler = CrawlerProcess(settings=get_project_settings())
crawler.crawl('34a')
crawler.crawl('downloadimages')
crawler.start()
crawler.start()
