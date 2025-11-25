BOT_NAME = "scraper"

SPIDER_MODULES = ["scraper.spiders"]
NEWSPIDER_MODULE = "scraper.spiders"

ROBOTSTXT_OBEY = True
DOWNLOAD_DELAY = 1

DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; RailScraper/1.0)'
}

ITEM_PIPELINES = {
   'scraper.pipelines.JsonWriterPipeline': 300,
}
