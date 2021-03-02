import scrapy
from ..items import AmazonbooksItem

class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon_spider'
    page_number = 2
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/Books-Last-30-days/s?rh=n%3A283155%2Cp_n_publication_date%3A1250226011']

    def parse(self, response):
        items = AmazonbooksItem()

        # you will get all in one line so, use for loop and xpath for better maybe
        book_name = response.css(".a-color-base.a-text-normal::text").extract()
        book_author = response.css(".sg-col-12-of-28 .a-size-base+ .a-size-base , .a-color-secondary .a-size-base.a-link-normal").css("::text").extract()
        book_price = response.css(".a-spacing-top-small .a-price-fraction , .a-spacing-top-small .a-price-whole").css("::text").extract()
        book_image_link = response.css(".s-image::attr(src)").extract()

        items["book_name"] = book_name
        items['book_author'] = book_author
        items['book_price'] = book_price
        items["book_image_link"] = book_image_link

        yield items

        next_page = "https://www.amazon.com/Books-Last-30-days/s?i=stripbooks&rh=n%3A283155%2Cp_n_publication_date%3A1250226011&page="+ str(AmazonSpiderSpider.page_number) + "&qid=1599800733&ref=sr_pg_2"
            
        if AmazonSpiderSpider.page_number <= 4:
            AmazonSpiderSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)



















        # all_books = response.css(".a-color-base.a-text-normal , .a-color-secondary .a-size-base.a-link-normal , .s-image , .a-spacing-top-small .a-price-fraction , .a-spacing-top-small .a-price-whole")
        
        # for book in all_books:
        #     book_name = book.css(".a-color-base.a-text-normal::text").extract()
        #     book_author = book.css(".a-color-secondary .a-size-base.a-link-normal").css("::text").extract()
        #     book_price = book.css(".a-spacing-top-small .a-price-fraction , .a-spacing-top-small .a-price-whole").css("::text").extract()
        #     book_image_link = book.css(".s-image::attr(src)").extract()

        #     items["book_name"] = book_name
        #     items['book_author'] = book_author
        #     items['book_price'] = book_price
        #     items["book_image_link"] = book_image_link
            
        #     yield items
        
