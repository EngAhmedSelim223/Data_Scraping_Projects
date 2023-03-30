import scrapy


class MineSpider(scrapy.Spider):
    name = "mine"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["http://www.worldometers.info/world-population/population-by-country/"]

    def parse(self, response):
        countries = response.xpath("//td/a")
        
        for country in countries:
            country_name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()
            
            yield response.follow(url = link, callback = self.parse_country, meta = {"name": country_name})
            
    def parse_country(self, response):
        name = response.request.meta['name']
        rows = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()
            
            yield{
                "country_name": name,
                "Year" : year,
                "population" : population
            }
        
