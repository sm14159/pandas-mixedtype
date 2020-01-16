##### Call with the following in the cli
# scrapy crawl random_addresses -o addresses.json
import scrapy

URL = 'https://ca.postcodebase.com/randomaddress#random_anchor'

class AddressSpider(scrapy.Spider):
    name = "random_addresses"
    allowed_domains = [URL]
    start_urls = [URL]
    max_number_requests = 100
    request_number = 1
    download_delay = 0.5

    def start_requests(self):
        yield scrapy.Request(url=URL, 
                            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'},
                            callback=self.parse,
                            dont_filter=True)

    def parse(self, response):
        for address in response.selector.css("div.radom_show_list div.box"):
            addr_lines = address.css("span::text").getall()
            zip_code = address.css("a::text").get()
            yield {
                'address_line': " ".join(addr_lines[:-3]),
                'city': addr_lines[-2],
                'state': addr_lines[-1],
                'zip_code': zip_code
            }
        self.request_number += 1
        if self.request_number < self.max_number_requests:
            print("Calling another request")
            yield next(self.start_requests())
