# BestBuy Parser
## Description
My first project using Python's Scrapy [framework](https://scrapy.org/).

I'm using this project personally for a couple friends of mine and I. Basically, it scrapes a products listing [page](https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&browsedCategory=abcat0507002&iht=n&ks=960&list=y&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203080%20Ti&sc=Global&st=categoryid%24abcat0507002&type=page&usc=All%20Categories) from BestBuy that lists RTX 3080 TIs. It scans each product and if the `c-button-disable` class doesn't exist within each entry (indicating it is not sold out and available), it will email a list of users from the `settings.py` file. It keeps each ID tracked in SQLite to make sure users don't get emailed more than once.

## Requirements
The Scrapy framework is required and may be installed with the following.

```bash
python3 -m pip install scrapy
```

## Settings
Settings are configured in the `src/bestbuy_parser/bestbuy_parser/settings.py` file. The following are defaults.

```python
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
```

## Running The Program
You must change the working directory to `src/bestbuy_parser/bestbuy_parser` via `cd`. Afterwards, you may run the following.

```bash
python3 parse.py
```

This will run the program until a keyboard interrupt.

## Systemd Service
A `systemd` service is included in the `systemd/` directory. It is assuming you cloned the repository into `/usr/src` (you will need to change the systemd file if this is not correct).

You may install the `systemd` service via the following command as root (or ran with `sudo`).

```bash
sudo make install
```

## Credits
* [Christian Deacon](https://github.com/gamemann)