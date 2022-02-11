import scrapy
from twisted.internet import reactor

import smtplib

from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import sqlite3

class BbSpider(scrapy.Spider):
    products = {}

    def __init__(self):
        super().__init__()

        self.crawler = None
        
        # Connect to SQLite3.
        self.db = sqlite3.connect('products.db')
        self.cursor = self.db.cursor()
        
        # Make sure table exists and if not, create it.
        self.cursor.execute("SELECT count(name) FROM sqlite_master where `type` = 'table' and name = 'products';")

        if self.cursor.fetchone()[0] != 1:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS `products` (`id` TEXT UNIQUE, `soldout` INTEGER);")
            self.db.commit()
        else:
            # Populate products.
            self.cursor.execute("SELECT `id`, `soldout` FROM `products`")
            prods = self.cursor.fetchall()

            for prod in prods:
                self.products[str(prod[0])] = prod[1]
        
    name = "bb"
    start_urls = [
        'https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&browsedCategory=abcat0507002&iht=n&ks=960&list=y&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203080%20Ti&sc=Global&st=categoryid%24abcat0507002&type=page&usc=All%20Categories'
    ]

    products = {}

    def start(self):
        self.crawler = Crawler(BbSpider, get_project_settings())
        self.crawler.crawl()
        reactor.run()

    def send_mail(self, name, price, link, id):
        # Setup SMTP on localhost.
        smtp = smtplib.SMTP()
        smtp.connect('localhost')

        # Loop through all to emails and send mail.
        for email in self.settings['MAIL_TO']:
            # Create MIME Multipart.
            msgRoot = MIMEMultipart("alternative")

            # Set subject (header).
            msgRoot['Subject'] = Header(self.settings['MAIL_SUBJECT'], 'utf-8')

            # Set from.
            msgRoot['From'] = self.settings['MAIN_FROM']

            # Set to.
            msgRoot['To'] = email

            # Parse and attach body.
            body = str(self.settings['MAIL_BODY']).replace('{name}', name).replace('{price}', price).replace('{link}', link)
            body = MIMEText(body, 'html')
            msgRoot.attach(body)

            # Send email.
            smtp.sendmail(msgRoot['From'], msgRoot['To'], msgRoot.as_string())

            if self.settings['PRINT_WHEN_NOT_SOLDOUT']:
                print(f'Sent email to {email}!')

    def parse(self, response):
        # Go through all items.
        for item in response.css('.sku-item'):
            # Retrieve general information.
            id = item.attrib['data-sku-id']
            info = item.css('.information .sku-header a')
            name = info.css('a::text').get()

            # If ID doesn't exist in database, insert it.
            if id not in self.products:
                self.cursor.execute("INSERT INTO `products` (`id`, `soldout`) VALUES ('" + id + "', 1);")
                self.db.commit()
                self.products[id] = 1

            # Button disable could mean sold out, etc.
            if len(item.css('.price-block .c-button-disabled')) < 1:
                # Make sure this item is marked as sold out in database.
                if self.products[id] == 0:
                    self.products[id] = 0

                    self.cursor.execute("UPDATE `products` SET `soldout` = 1 WHERE `id` = '" + id + "';")
                    self.db.commit()

                continue

            # If we're already set to not sold out, ignore.
            if self.products[id] == 0:
                continue

            link = info.attrib['href']

            # Receive price.
            price_str = item.css('.price-block .priceView-customer-price span::text').get().strip('$').replace(',', '')
            price = float(price_str)

            # Make sure we aren't exceeding max price.
            if price > self.settings['MAX_PRICE']:
                continue

            # Print out.
            if self.settings['PRINT_WHEN_NOT_SOLDOUT']:
                print(f'Item {name} at {price_str} not soldout!')
            
            # Email client.
            self.send_mail(name, price_str, link, id)

            # Set product ID to False indicating not sold out.
            self.products[id] = 0

            self.cursor.execute("UPDATE `products` SET `soldout` = 0 WHERE `id` = '" + id + "';")
            self.db.commit()

        self.db.close()
        reactor.stop()