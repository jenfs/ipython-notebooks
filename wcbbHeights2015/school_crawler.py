from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from bs4 import BeautifulSoup
import os

class NcaaSchoolSpider(CrawlSpider):
    name = 'schoolspider'
    start_urls = ['http://www.ncaa.com/schools/']
    allowed_domains = ['ncaa.com']
    
    rules = (
        Rule(SgmlLinkExtractor(allow=(r'/schools/[a-z]$',), allow_domains=('ncaa.com'))),
        Rule(SgmlLinkExtractor(allow=(r'/schools/[a-z]',), allow_domains=('ncaa.com')), callback='parse_item'),
    )
    
    def __init__(self):
        CrawlSpider.__init__(self)
        try:
            os.remove('ncaa_d1_schools.txt')
        except OSError:
            pass
    
    def parse_item(self, response):
        page_soup = BeautifulSoup(response.body)
        try:
            if page_soup.find('div', {'class':'school-meta'}).find('h2').text == 'Div I':
                with open('ncaa_d1_schools.txt', 'a') as f:
                    f.write(response.url + '\n')
        except AttributeError:
            pass
            