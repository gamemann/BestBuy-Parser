from twisted.internet import reactor
from spiders import bb_spider

from multiprocessing import Process

class SpiderRunner(Process):
    def __init__(self):
        self.spider = None
        Process.__init__(self)

    def run(self):
        self.spider = bb_spider.BbSpider()

        self.spider.start()
        