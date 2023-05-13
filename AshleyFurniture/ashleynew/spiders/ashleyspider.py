import scrapy
import pandas as pd
from scraper_api import ScraperAPIClient

client = ScraperAPIClient("dbcdd9e8dbf3522f15186db7c51461b0")
import json
class AshleyspiderSpider(scrapy.Spider):
    name = "ashleyspider"
    custom_settings = {
        'HTTPERROR_ALLOW_ALL': True,}

    def start_requests(self):
        df = pd.read_excel("data.xlsx")
        categories = df['links']
        for category in categories:
            yield scrapy.Request(
                client.scrapyGet(url=category, country_code="us"),
                callback=self.parse_products

            )
    def parse_products(self, response):
        products = response.xpath("//a[@class='name-link']")
        for product in products:
            product_link = product.xpath("./@href").get()
            yield scrapy.Request(
                client.scrapyGet(url=product_link, country_code="us", autoparse=True),
                callback=self.info_scrapper,
                meta={"product_link" : product_link}
            )
        next_page = response.xpath("//a[contains(@class,'page-switcher page-next')]/@href").get()
        if next_page:
            yield scrapy.Request(
                client.scrapyGet(url=next_page, country_code="us"),
                callback=self.parse_products
            )

    def info_scrapper(self, response):

        target_type = 'Product'
        script_tags = response.xpath('//script[@type="application/ld+json"]/text()').getall()

        json_data = None
        for script_tag in script_tags:
            try:
                data = json.loads(script_tag)
                if data.get('@type') == target_type:
                    json_data = data
                    break
            except json.JSONDecodeError as err:
                self.logger.error(f"JSON decoding error: {err}")
                self.logger.error(f"Failed to decode the following response: {script_tag}")

        if json_data:
            Retailer = "ashleyfurniture.com"
            category = response.xpath("(//a[@class='breadcrumb-element'])[last()]/text()").get()
            if category is not None:
                category = category.strip()
            else:
                pass
            product_color = response.xpath("//span[@class='selected-variant']/text()").get()
            if product_color is not None:
                product_color = product_color.strip()
            else:
                pass

            title = json_data['name']
            url = json_data['url']
            images = json_data['image']
            description = json_data['description']
            brand = json_data['brand']['name']
            if brand is None:
                brand = "Signature Design by Ashley®"
            sku = json_data['sku']
            price = json_data['offers']['price']
            yield {
                "Title" : title,
                "Description": description,
                "Item Category" : category,
                "Price": price,
                "Sku": sku,
                "Url": url,
                "Images" : images,
                "Colors" : product_color,
                "Brand" : brand,
                "Retailer" : Retailer
            }

        else:
            self.logger.warning(f"No JSON data found with @type '{target_type}'.")

