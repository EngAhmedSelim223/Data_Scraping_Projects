
from setup import setup
setup()


from scrapy.crawler import CrawlerProcess
import json,re,datetime,scrapy
from scrapy.selector import Selector
from output import outlist
from datetime import datetime as dt

class Bassettfurniture(scrapy.Spider):
    def __init__(self):
        self.results = {}
        self.records = 0
        self.st = dt.now()
    base_url = "https://www.bassettfurniture.com"
    products = 'https://www.bassettfurniture.com/p-sitemap.xml'

    name  = "Bassettfurniture_makdi"
    
    filename = 'Bassettfurniture_All_records' + '_' + datetime.datetime.now().strftime('%d-%m-%Y_%I-%M-%S-%p')
    
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.344' }
    
    custom_settings = {
    'CONCURRENT_REQUESTS_PER_DOMAIN': 6,
    'CONCURRENT_REQUESTS': 6,
    # 'DOWNLOAD_DELAY': 1,
    'REQUEST_FINGERPRINTER_IMPLEMENTATION':'2.7',
    }
    
    
    def start_requests(self):
        yield scrapy.Request(url = self.products,callback=self.parse_products,headers = self.headers)
    def parse_products(self,res):
        res = Selector(text=res.text)
        urls = res.css("urlset > url > loc")

        for url in urls:
            uri = url.css("::text").get()
            yield scrapy.Request(url=uri,headers=self.headers,callback=self.details)
    def details(self,res):

        levels = res.css('span.ancestor > a::text').getall()
        if len(levels) == 2:
            cat = levels[1]
        else:
            cat = "N/A"
        if cat not in self.results.keys():
            self.results[cat] = {'count':0,'data':[]}

        script = res.xpath('//script[contains(text(),"$.pdp.global.product =")]/text()').get()

        data = json.loads(re.search(r'pdp\.global\.product = ([^\n]+)',script).group(1).strip()[:-1])

        name = data.get("name")
        price = data.get('price')
        desc = ','.join(data.get('description') or [])
        sku = data.get("sku")
        specs = data.get("Specifications") or []
        height = length = width = depth = color = matt ='N/A'
        image = data.get('ctaImage')
        for spec in specs:
            header = spec.get('header')
            attrs = spec.get('attributes')

            if header and header == 'Essentials':
                for attr in attrs:
                    attrName = attr.get('attribute').lower()
                    attrVal = attr.get('value')
                    if 'height' in attrName:
                        height = attrVal
                    if 'width' in attrName:
                        width = attrVal
                    if 'length' in attrName:
                        length = attrVal

            if header and header =='Materials + Construction':
                for attr in attrs:
                    attrName = attr.get('attribute').lower()
                    attrVal = attr.get('value')

                    if 'material' in attrName:
                        matt = attrVal
                    if matt =='N/A':
                        if 'construction' in attrName:
                            matt = attrVal

        numsOnly = lambda val: re.sub(r'[^.0-9]','',val)
        height = numsOnly(height)
        length = numsOnly(length)
        width = numsOnly(width)
        depth = numsOnly(depth)


        basicOpt = data.get("basicOptions")
        if basicOpt:
            basicOpt = basicOpt[0]
            selectedVal = basicOpt.get('selectedValue')
            if selectedVal:
                color = selectedVal.get("Color")

        info_dict = {
            "Name": name or "N/A",
            "Sku": sku or "N/A",
            "Category": cat or "N/A",
            "Price": price or "N/A",
            "Material": matt or "N/A",
            "Height": height or "N/A",
            "Length": length or 'N/A',
            "Width": width or "N/A",
            "Depth": depth or "N/A",
            "Color": color or "N/A",
            "Description": desc or "N/A",
            "Image": image or "N/A",
            "Product Url": res.url

        }
        self.results[cat]['count']+=1
        self.records+=1
        print(f"\n {cat} : {self.results.get(cat).get('count')}")
        print(f'\nRecords : {self.records}')
        self.results[cat]['data'].append(info_dict)
        print(info_dict)
    def close(self, spider, reason):
        print("\n----------------------Completing----------------------\n")
        for key,v in self.results.items():
            data = v['data']
            if data:
                outlist(self.filename,data,xl=True,json=True)
        print(f"Time Taken :- {(dt.now() - self.st).seconds // 60} Mins")
        print("\n----------------------Completed------------------------\n")

if __name__ == '__main__':
    task = CrawlerProcess()
    task.crawl(Bassettfurniture)
    task.start()
