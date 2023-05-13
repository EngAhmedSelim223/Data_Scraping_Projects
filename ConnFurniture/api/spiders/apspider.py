import json
import scrapy
from scraper_api import ScraperAPIClient
client = ScraperAPIClient("dbcdd9e8dbf3522f15186db7c51461b0")
class ApiSpider(scrapy.Spider):
    name = 'apspider'

    def start_requests(self):

        url = 'https://eucs29v2.ksearchnet.com/cs/v2/search'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'klevu-164677714116414855'
        }
        categories = [
            "Furniture;Living Room Furniture",
            "Furniture;Bedroom Furniture",
            "Furniture;Dining Room Furniture",
            "Furniture;Home Office Furniture",
            "Furniture;Kids Bedroom",
            "Furniture;Kids Playroom Furniture",
            "Furniture;Nursery Furniture",
            "Clearance;Clearance Furniture",
            "Furniture;Living Room Furniture;Sofas & Sleepers",
            "Furniture;Living Room Furniture;Loveseats",
            "Furniture;Living Room Furniture;Sectionals",
            "Furniture;Living Room Furniture;Sectionals",
            "Furniture;Living Room Furniture;Recliners",
            "Furniture;Bedroom Furniture;Bedroom Sets",
            "Furniture;Bedroom Furniture;Beds",
            "Furniture;Bedroom Furniture;Dressers and Chests",
            "Furniture;Bedroom Furniture;Nightstands"

        ]
        for category in categories:
            data = {
                "context": {
                    "apiKeys": ["klevu-164677714116414855"]
                },
                "recordQueries": [
                    {
                        "id": "productList",
                        "typeOfRequest": "CATNAV",
                        "filters": {
                            "applyFilters": {
                                "filters": [
                                    {"key": "availability", "values": ["In Stock Only"]},
                                    {"key": "csi", "values": ["340", "341", "027", "071", "316", "070", "266", "301", "129", "026", "017", "024", "025", "018", "112", "247", "078", "105", "076", "102", "021", "077", "029", "073", "248"]}
                                ]
                            },
                            "filtersToReturn": {
                                "enabled": True,
                                "options": {
                                    "limit": "20"
                                },
                                "rangeFilterSettings": [
                                    {"key": "klevu_price", "rangeInterval": "500"}
                                ]
                            }
                        },
                        "settings": {
                            "query": {
                                "term": "*",
                                "categoryPath": category
                            },
                            "fields": [
                                "id", "is_bespoke", "bespoke_skus", "product_variant_options", "product_variant_label", "name", "price", "sku", "PDP_Flags", "free_shipping", "klevu_creation_date", "basePrice", "category", "currency", "image", "salePrice", "url", "weight", "klevu_category"
                            ],
                            "limit": "10000",
                            "priceFieldSuffix": "USD-027",
                            "searchPrefs": ["searchCompoundsAsAndQuery"],
                            "typeOfRecords": ["KLEVU_PRODUCT"]
                        }
                    }
                ]
            }
            yield scrapy.Request(client.scrapyGet(url=url), method='POST', body=json.dumps(data), headers=headers, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.text)

        # Extract the records
        records = data['queryResults'][0]['records']

        # Iterate through the records and print the values
        for record in records:
            title = record["name"].strip()
            price = record["basePrice"].strip()
            sku = record["sku"].strip()
            product_link = record["url"]
            cats = record["klevu_category"].split(";")
            cat = cats[-1].replace("@ku@kuCategory@ku@","").strip()
            image1 = record["image"]
            image2 = record["imageUrl"]
            images = image1 + image2
            meta={
                "title" :title,
                "price" : price,
                "sku" : sku,
                "product_link": product_link,
                "category":cat,
                "images" : images
            }
            yield scrapy.Request(client.scrapyGet(url=product_link, render=True, country_code="us"), callback=self.info_scraper, meta=meta)

    def info_scraper(self,response):
        description = response.xpath("//div[@class='marketing_information']/text()").get()
        if description is not None:
            description = description.strip()
        else:
            pass

        product_width = response.xpath('//table[@class="table table-striped table-responsive"]/tbody/tr[td[contains(., "Width:")]]/td[@class="tb_title_pdp"]/text()').get()
        if product_width is not None:
            product_width = product_width.strip()
        else:
            pass

        product_depth = response.xpath('//table[@class="table table-striped table-responsive"]/tbody/tr[td[contains(., "Depth:")]]/td[@class="tb_title_pdp"]/text()').get()
        if product_depth is not None:
            product_depth = product_depth.strip()
        else:
            pass

        product_weight = response.xpath('//table[@class="table table-striped table-responsive"]/tbody/tr[td[contains(., "Weight:")]]/td[@class="tb_title_pdp"]/text()').get()
        if product_weight is not None:
            product_weight = product_weight.strip()
        else:
            pass
        item_attributes = response.xpath('//table[@class="table table-striped table-responsive"]/tbody/tr[td[contains(., "material:")]]/td[@class="tb_title_pdp"]/text()').get()
        if item_attributes is not None:
            item_attributes = item_attributes.strip()
        else:
            pass

        product_color = response.xpath('//table[@class="table table-striped table-responsive"]/tbody/tr[td[contains(., "color:")]]/td[@class="tb_title_pdp"]/text()').get()
        if product_color is not None:
            product_color = product_color.strip()
        else:
            pass


        Title = response.meta['title']
        Price = response.meta['price']
        Sku = response.meta['sku']
        URL = response.meta['product_link']
        Category = response.meta['category']
        images = response.xpath("//ul[contains(@class,'productView-thumbnails mt-8')]/li/a[@class='productView-thumbnail-link']/@href").getall()
        if len(images) < 2:
            images = response.meta['images']

        brand = "Conn's HomePlus"
        yield {
            "Title" : Title,
            "Description": description,
            "Category": Category,
            "Item Attributes" : item_attributes,
            "Price" : Price,
            "Sku" : Sku,
            "URL" : URL,
            "Images" :images,
            "Brand" : brand,
            "Colors" : product_color,
            "product_width": product_width,
            "product_depth": product_depth,
            "product_weight": product_weight,
        }

