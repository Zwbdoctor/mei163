import scrapy


class Mei163Spider(scrapy.Spider):
    name = 'get_imgs'
    allow_domain = ['mei.163.com']

    def start_requests(self):
        item = ImageItem()
        with open('product_v2.csv') as file:
            while True:
                data = file.readline()
                if not data:
                    break
                data = data.split(',')
                urls = data[1].split(',')
                for url in urls:
                    yield scrapy.Request(url, callback=self.parse_img, meta={'id': data[0]})

    def parse_img(self, response):
        id = response.meta['id']
        pass

