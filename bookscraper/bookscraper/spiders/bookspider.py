import scrapy
from bookscraper.items import BookscraperItem

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        # books = response.css("article.product_pod")
        books = response.xpath('//article[@class="product_pod"]')
        # bookItem = BookscraperItem()

        for book in books:
            relative_url = book.xpath('//h3/a/@href').get()

            if 'catalogue/' in relative_url:
                book_url = "https://books.toscrape.com/" + relative_url
            else:
                book_url = "https://books.toscrape.com/catalogue/" + relative_url

            yield response.follow(book_url, callback = self.parse_book_page)

        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = "https://books.toscrape.com/" + next_page
            else:
                next_page_url = "https://books.toscrape.com/catalogue/" + next_page

            yield response.follow(next_page_url, callback = self.parse)

    def parse_book_page(self, response):
        url = response.url
        title = response.xpath('//h1/text()').get()
        category = response.xpath('//ul[@class="breadcrumb"]/li[@class="active"]/preceding-sibling::li[1]/a/text()').get()
        description = response.xpath('//div[@id="product_description"]/following-sibling::p/text()').get()
        price = response.xpath('//p[@class="price_color"]/text()').get()

        table_rows = response.css('table tr')
        product_type = table_rows[1].css('td ::text').get()
        price_excl_tax = table_rows[2].css('td ::text').get()
        price_incl_tax = table_rows[3].css('td ::text').get()
        tax = table_rows[4].css('td ::text').get()
        availability = table_rows[5].css('td ::text').get()
        num_reviews = table_rows[6].css('td ::text').get()
        stars = table_rows[0].xpath('//p[contains(@class, "star-rating")]/@class').get()

        yield {
            "url": url,
            "title": title,
            "rating": stars,
            "category": category,
            "description": description,
            "product_type": product_type,
            "price": price,
            "price_incl_tax": price_incl_tax,
            "price_excl_tax": price_excl_tax,
            "tax": tax,
            "availability": availability,
            "num_reviews": num_reviews,
        }