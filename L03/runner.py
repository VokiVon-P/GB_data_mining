from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser import settings

from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.spjob import SpjobSpider




if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    # краулер HeadHunter
    process.crawl(HhruSpider)
    # краулер SuperJob
    process.crawl(SpjobSpider)
    process.start()
