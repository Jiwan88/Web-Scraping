import scrapy
from ..items import UniversityItem


class UniversitySpider(scrapy.Spider):
    name = 'university'
    # allowed_domains = ['example.com']
    start_urls = ['https://study.unimelb.edu.au/find/']

    def parse(self, response):
        items = UniversityItem()
        area = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "interest-item__name", " " ))]/text()').extract()
        area_url =  response.xpath("//div[@data-test='interest-list']/div/div/a[@data-test='image-card-item']/@href").extract()
        for i in range(len(area)):
            items["area"] = area[i]
            items["area_url"] = "https://study.unimelb.edu.au/" + area_url[i]
            yield items
        
        # for base_url in range(area_url):
        #     items['area_url'] = "https://study.unimelb.edu.au/" + area_url[base_url]
        #     yield items


        

        
