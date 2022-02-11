# General Scrapy settings.
BOT_NAME = 'bestbuy_parser'

SPIDER_MODULES = ['bestbuy_parser.spiders']
NEWSPIDER_MODULE = 'bestbuy_parser.spiders'

TELNETCONSOLE_ENABLED = False
LOG_LEVEL = 'ERROR'

# The User Agent used to crawl.
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Best Buy Parser-specific settings.

# The email's subject to send.
MAIL_SUBJECT = "RTX 3080 TI In Stock On Best Buy!"

# Where the email is coming from.
MAIN_FROM = "test@domain.com"

# The email body.
MAIL_BODY = '<html><body><ul><li><a href="https://www.bestbuy.com{link}">{name}</a></li><li>{price}</li></ul></body></html>'

# Recipients to send to.
MAIL_TO = [
    'test@domain2.com'
]

# If any items exceed this price and are labeled as available, users will not be notified on this product.
MAX_PRICE = 1500.00

# How often to scan in seconds.
SCAN_TIME = 5.0

# Whether to print to `stdout` when a product isn't sold out/valid and a user is being emailed.
PRINT_WHEN_NOT_SOLDOUT = True