import scrapy
import time

class BelspiderSpider(scrapy.Spider):
    name = "belspider"
    allowed_domains = ["belfurniture.com"]
    start_urls = ["https://belfurniture.com/"]

    def parse(self, response):
        # Extract the category links from the navigation bar until kids
        category_links_part_1 = response.css('#header-nav li div summary span.header__active-menu-item a')
        category_links_part_2 = response.css('#header-nav > li > a')
        category_links = category_links_part_1 + category_links_part_2
        for link in category_links:
            try:

                category_name = link.css('span::text').get().strip()
                category_url = f"https://belfurniture.com{link.css('::attr(href)').get()}"
            except:
                category_name = link.css('::text').get().strip()
                category_url = f"https://belfurniture.com{link.css('::attr(href)').get()}".strip()

            if "collections" in category_url:
                yield scrapy.Request(category_url, callback=self.parse_products, meta={'category_name': category_name})
            else:
                yield scrapy.Request(category_url, callback=self.parse_category, meta={'category_name': category_name})


    def parse_category(self, response):
        category_name = response.meta['category_name']

        sub_categories = response.css('div.subbanners a')
        del sub_categories[len(sub_categories)-1:]
        for sub_cat in sub_categories:
            try:
                sub_category_name =sub_cat.css('div.cms-banner-subtitle::text').get().strip()
                sub_category_url = f"https://belfurniture.com{sub_cat.css('::attr(href)').get()}".strip()
                yield scrapy.Request(sub_category_url, callback=self.parse_products, meta={'category_name': sub_category_name})

            except:
                pass


    def parse_products(self,response):

        try:
            sub_category_name = response.meta['category_name']
        except:
            sub_category_name = ""

        products = response.css('li.grid__item.item span.products div.card-img a')
        for product in products:
            product_link = f"https://belfurniture.com/{product.css('::attr(href)').get()}".strip()
            yield scrapy.Request(product_link, callback=self.info_scraper, meta={'category_name': sub_category_name})
        # pagination = response.xpath("//ul[@class='pagination__list list-unstyled']")
        next_page = response.xpath("//nav[@class='pagination']/ul/li/a[@aria-label='Next page']/@href").get()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse_products)


    def info_scraper(self,response):

        # product_main_category = response.meta['category_name']
        product_link = response.url
        product_title = response.xpath("//h1[@class='product__title']/text()").get().strip()
        product_price = response.xpath("(//dd/span[@class='price-item price-item--regular'])[1]/text()").get().strip().replace("$","")
        product_vendor = response.xpath("//div[@class='product__type'][1]/text()[2]").get().strip().replace(":","")
        product_type = response.xpath("//div[@class='product__type'][2]/text()[2]").get().strip().replace(":","")
        product_Sku = response.xpath("//div[@class='product__type'][3]/text()[2]").get().strip().replace(":","")
        try:
            description = response.xpath("//div[@id='tab-1']/p[1]/text()").get().strip()
        except:
            product_description = response.xpath("//div[@id='tab-1']//text()").getall()
            stripped_text_content = [text.strip() for text in product_description]
            description = ' '.join(stripped_text_content).encode(encoding='utf-8')
        try:
            product_dimensions = response.xpath("//div[@id='tab-1']/ul/li/text()[2]").get().strip()
        except:
            try:
                product_dimensions = description[-1:-len(description) - 25].encode(encoding='utf-8')
            except:
                product_dimensions = description[-1:-len(description)-25].decode(encoding='utf-8')
        product_images = []
        try:
            for image in response.css("#zoom1"):
                product_images.append(image.css('::attr(href)').get())
        except:
            pass




        yield {
            "title": product_title,
            "type": product_type,
            "price": product_price,
            "retailer" : "belfurniture.com",
            "retailerURI": product_link,
            "images" : product_images,
            # "product_main_category": product_main_category,
            "brand": product_vendor,
            "sku": product_Sku,
            "dimensions": product_dimensions,
            "description" : description
        }