import time

from runner import runner

def main():
    try:
        while True:
            crawler = runner.SpiderRunner()
            crawler.start()
            crawler.join()


            try:
                scan_time = crawler.spider.crawler.settings['SCAN_TIME']
            except Exception:
                scan_time = 5

            if scan_time is not None:
                time.sleep(scan_time)
            else:
                time.sleep(5)
    except KeyboardInterrupt:
        return

if __name__ == '__main__':
    main()
