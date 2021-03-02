from bs4 import BeautifulSoup
import scrapy


class HnSpider(scrapy.Spider):
    name = "hacker-news"
    allowed_domains = ["news.ycombinator.com"]
    start_urls = [f'https://news.ycombinator.com/news?p={i}' for i in range(1,16)]

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.findAll('tr', class_='athing')

        for link in links:
        	yield {
        		'id': link['id'],
        		'title': link.find_all('td')[2].a.text,
        		"url": link.find_all('td')[2].a['href'],
        		"rank": int(link.td.span.text.replace('.', ''))
        	}