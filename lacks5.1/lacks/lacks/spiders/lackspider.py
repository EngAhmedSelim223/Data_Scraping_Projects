import scrapy
from scrapy_playwright.page import PageMethod

def should_abourt_request(request):
    if request.resource_type == "image":
        return True
    else:
        return False

class LackspiderSpider(scrapy.Spider):
    name = "lackspider"
    # allowed_domains = ["www.lacks.com"]
    # start_urls = ["https://www.lacks.com"]

    def start_requests(self):
        url = 'https://www.lacks.com/'
        yield scrapy.Request(url, self.parse, meta={"playwright" : True})


    def parse(self, response):
        #get categories links
        categories = response.xpath("//nav[@id='nav']/ul/li[position() <= 7]/a")
        for category in categories:
            category_link = f"https://www.lacks.com{category.xpath('./@href').get()}"
            yield scrapy.Request(category_link, callback=self.parse_category)

    def parse_category(self, response):
        view_all_links = response.css('.category-landing-content-headline a.btn-outline')
        for viewall in view_all_links:
            category_link = f"https://www.lacks.com{viewall.css('::attr(href)').get()}"
            
               
            yield scrapy.Request(category_link, self.parse_products, meta={
                "playwright": True,
                "playwright_abort_request" : should_abourt_request,
                "playwright_page_methods": [

                    # PageMethod("click", "button[data-role='deny']"),
                    # PageMethod("click", "button[data-role='allow']"),
                    PageMethod("wait_for_selector", "p.product-block-title a")
                ],
            })

    def parse_products(self, response):
        
        products = response.css('p.product-block-title a::attr(href)').getall()
        for product in products:
            product_link = f"https://www.lacks.com{product}"
            yield scrapy.Request(product_link, callback=self.info_scraper, meta={
                "playwright": True,
                "playwright_page_methods": [

                    # PageMethod("click", "button[data-role='deny']"),
                    # PageMethod("click", "button[data-role='allow']"),
                    PageMethod("wait_for_selector", "img.pdp-slider-main-img")
                ],
            })
        page_numbers = [1,2,3,4,5,6,7]
        for page in page_numbers:
            next_page = f"{response.url}?page={page}"
            if next_page is not None:
                yield scrapy.Request(next_page, self.parse_products, meta={"playwright": True})

    def info_scraper(self,response):
        #extracting information from each product

        # product_type = response.meta['product_type']
        product_link = response.url
        product_title = response.css("h2.global-two-col-header-content-headline::text").get()
        product_type = response.xpath("//p[@class='breadcrumbs'] /a[2]/text()").get()
        product_price = response.xpath("//p[@class='sale-total-price-new ng-binding']/text()").get().replace("$","")
        product_stock = response.xpath("//div[@class='pdp-details pdp-details-desktop'] /ul /li[1]/text()").get()
        product_description = response.xpath("//div[@class='rich-text']/p[1]/text()").get().strip()
        try:
            dimensions = response.xpath("//div[@class='pdp-details pdp-details-desktop']/ul/li[position()>1 and position() <5]/text()").getall()
        except:
            dimensions = "Unknown"
        image_src = response.css('img.pdp-slider-main-img::attr(src)').get()
        image = f"https://www.lacks.com{image_src}".strip()
        

        yield{
            "title" : product_title,
            "type" : product_type,
            "price" : product_price,
            "retailer" : "lacks.com",
            "retailerURI" : product_link,
            "images" : image,
            "sku" : product_stock,
            "dimensions" : dimensions,
            "description" : product_description
         }