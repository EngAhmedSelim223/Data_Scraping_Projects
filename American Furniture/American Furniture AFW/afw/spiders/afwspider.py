import scrapy
from scraper_api import ScraperAPIClient
client = ScraperAPIClient("e02593ff12f89e9f7f6baf2c638c6362")

class AfwspiderSpider(scrapy.Spider):
    name = "afwspider"
    # allowed_domains = ["https://www.afw.com/"]
    # start_urls = ["http://x/"]

    def start_requests(self):
        url = "https://www.afw.com/furniture"
        yield scrapy.Request(client.scrapyGet(url=url), self.parse)
    def parse(self, response):
        Category_links = response.xpath("//div[contains(@class, 'child-category')]/a")
        for link in Category_links :
            url = f"https://www.afw.com{link.xpath('./@href').get()}".strip()
            yield scrapy.Request(client.scrapyGet(url=url), callback = self.parse_products)

    def parse_products(self, response):
        products = response.xpath("//div[@class='product-title']/a")

        for product in products:
            if product is not None:
                product_link = f"https://www.afw.com{product.xpath('./@href').get()}"
                if product_link is not None:
                    product_link = product_link.strip()
                    yield scrapy.Request(client.scrapyGet(url=product_link), callback=self.info_scrape, meta={"product_link":product_link})
                else:
                    pass
        next_page = response.css("li.next-page a::attr(href)").get()
        if next_page:
            yield scrapy.Request(client.scrapyGet(url=next_page), callback=self.parse_products)


    def info_scrape(self, response):
        product_link = response.meta['product_link']
        product_title = response.xpath("//strong[@class='current-item']/text()").get()

        if product_title is not None:
            product_title = product_title.strip()
        else:
            pass
        product_type = response.xpath("//div[@class='breadcrumb']/ul/li[4]/a/span/text()").get()

        if product_type is not None:
            product_type = product_type.strip()
        else:
            product_type = response.xpath("//div[@class='breadcrumb']/ul/li/a/span/text()").get().strip()

        product_category = response.xpath("//div[@class='breadcrumb']/ul/li[3]/a/span/text()").get()
        if product_category is not None:
            product_category = product_category.strip()
        else:
            pass

        product_price = response.xpath("//div[@class='product-price']/span/text()").get()
        if product_price is not None:
            product_price = product_price.strip().replace("$","")
        else:
            pass

        Item_Attributes = response.xpath("//table/tbody/tr/td[contains(text(), 'Construction')]/../td[2]/text()").get()
        if Item_Attributes is not None:
            Item_Attributes = Item_Attributes.strip()
        else :
            pass

        product_color = response.xpath("//table/tbody/tr/td[contains(text(), 'Color')]/../td[2]/text()").get()
        if product_color is not None:
            product_color = product_color.strip()
        else:
            pass
        product_width = response.xpath("//table/tbody/tr/td[contains(text(), 'Width')]/../td[2]/text()").get()
        if product_width is not None:
            product_width = product_width.strip()
        else:
            pass

        product_height = response.xpath("//table/tbody/tr/td[contains(text(), 'Height')]/../td[2]/text()").get()
        if product_height is not None:
            product_height = product_height.strip()
        else:
            pass

        product_depth = response.xpath("//table/tbody/tr/td[contains(text(), 'Depth')]/../td[2]/text()").get()
        if product_depth is not None:
            product_depth = product_depth.strip()
        else:
            pass
        product_description = response.xpath("//div[@class='product-accordion-description']/ul/li/text()").getall()
        if product_description is not None:
            joined = "".join(product_description)
            product_description = joined.strip()
        else:
            pass

        product_sku = response.xpath("//div[@class='sku']/span[2]/text()").get()
        if product_sku is not None:
            product_sku = product_sku.strip()
        else:
            pass

        product_images = response.xpath("//div[@class='picture-thumbs']/div/img/@src").getall()
        if product_images is not None:
            product_images = product_images
        else:
            pass


        yield{
            "title": product_title,
            "Description" : product_description,
            "Room Categories": product_category,
            "Item Categories": product_type,
            "Item Attributes": Item_Attributes,
            "Price": product_price,
            "Sku": product_sku,
            "URL": product_link,
            "Image URLs": product_images,
            "Brand": "American Furniture Warehouse",
            "Color": product_color,
            "Retailer" : "afw.com",
            "Width": product_width,
            "Height": product_height,
            "Depth": product_depth

        }
