
BOT_NAME = "lacks"

SPIDER_MODULES = ["lacks.spiders"]
NEWSPIDER_MODULE = "lacks.spiders"

ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY= 10
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": False,  # Run the browser in headless mode
    # "slowMo": 100,  # Slow down Playwright operations by 100ms
    "args": [
        "--disable-web-security",  # Disable web security to bypass CORS policies
        "--no-sandbox",  # Disable the sandbox for better compatibility with Docker
        "--disable-setuid-sandbox",  # Disable the setuid sandbox for better compatibility with Docker
        "--disable-dev-shm-usage",  # Disable /dev/shm usage to prevent crashes in Docker
    ],  
    # "ignoreHTTPSErrors": True,  # Ignore HTTPS errors
}

# Configure Playwright browser type and launch options
PLAYWRIGHT_BROWSER_TYPE = "chromium"
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,
    "args": [
        "--disable-web-security",
        "--disable-features=IsolateOrigins,site-per-process",
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage",
    ],
}

# Configure maximum number of concurrent Playwright requests
PLAYWRIGHT_CONCURRENT_REQUESTS = 2

# Enable or disable Playwright request retry middleware
PLAYWRIGHT_RETRY_ENABLED = True

# Configure maximum number of retries for failed Playwright requests
PLAYWRIGHT_RETRY_TIMES = 3

# Configure Playwright request retry HTTP status codes
PLAYWRIGHT_RETRY_HTTP_CODES = [500, 502, 503, 504, 408]

# Configure Playwright request retry exceptions

# Enable or disable Playwright screenshot capture middleware
PLAYWRIGHT_SCREENSHOT_ENABLED = False

# Configure Playwright screenshot capture options
PLAYWRIGHT_SCREENSHOT_OPTIONS = {
    "fullPage": True,
    "path": "screenshot.png",
}

# Disable cookies
COOKIES_ENABLED = False

# Disable user agent middleware
USER_AGENT_ENABLED = False

# Disable HTTP compression middleware
HTTPCompressionMiddleware_ENABLED = False

# Set download timeout (in seconds)
DOWNLOAD_TIMEOUT = 50

# Set maximum number of concurrent requests per domain
CONCURRENT_REQUESTS_PER_DOMAIN = 4

# Set maximum number of concurrent requests per IP
CONCURRENT_REQUESTS_PER_IP = 4

# Set user agent string (optional)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
FEED_EXPORT_ENCODING = "utf-8"
