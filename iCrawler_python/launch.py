# -*- coding: utf-8 -*-
import sys
from scrapy import cmdline

spider_name = sys.argv[1]
cmdline.execute(("scrapy crawl %s" % spider_name).split())
