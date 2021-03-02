# import urllib3
# http = urllib3.PoolManager()
# r = http.request("GET", "https://www.google.com")

# from lxml import html

# data_string = r.data.decode('utf-8', errors = 'ignore')
# tree = html.fromstring(data_string)

# links = tree.xpath("//a")
# for link in links:
#     print(link.get('href'))

import requests
from bs4 import BeautifulSoup 

r = requests.get("https://news.ycombinator.com")
soup = BeautifulSoup(r.text, 'html.parser')
links = soup.findAll('tr', class_='athing')

formatted_links = []

for link in links:
    data = {
        'id': link['id'],
        'title': link.find_all('td')[2].a.text,
		"url": link.find_all('td')[2].a['href'],
		"rank": int(links[0].td.span.text.replace('.', ''))
    }
    formatted_links.append(data)

print(formatted_links[0])    