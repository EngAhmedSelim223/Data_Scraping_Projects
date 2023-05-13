# Scrapy settings for ashleynew project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "ashleynew"

SPIDER_MODULES = ["ashleynew.spiders"]
NEWSPIDER_MODULE = "ashleynew.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "ashleynew (+http://www.yourdomain.com)"

ROBOTSTXT_OBEY = False


COOKIES_ENABLED = False
# DOWNLOADER_MIDDLEWARES = {
#     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#     'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,}
HTTPCACHE_ENABLED = False
# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",

}

# SPLASH_URL = 'http://localhost:8050/'
# DOWNLOADER_MIDDLEWARES = {
#     'scrapy_splash.SplashCookiesMiddleware': 723,
#     'scrapy_splash.SplashMiddleware': 725,
#     'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
# }
CONCURRENT_REQUESTS = 15
CONCURRENT_REQUESTS_PER_IP = 15
CONCURRENT_REQUESTS_PER_DOMAIN = 15
DOWNLOAD_DELAY = 0.5
HTTPPROXY_ENABLED = True

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
