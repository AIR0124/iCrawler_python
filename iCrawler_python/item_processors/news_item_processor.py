# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

from iCrawler_python.formatTools import zhihuhaoCustomFormat
from iCrawler_python.formatTools.commonFormat import commonFormat
from iCrawler_python.settings import logger


def process_news_item(item):
    """
    处理文章类的item
    :param item: 
    :return: 
    """
    try:
        keyword = item.get('zhihuhao')
        html_text = item.get('html')
        pure_text = item.get('pure_text')

        document = BeautifulSoup(html_text, u'lxml')
        if keyword in ['zhu-yin-lun', 'ravenblockchain', 'qiong-you-jin-nang']:
            zhihuhaoCustomFormat.extract_advertising(keyword, document)
            commonFormat.remove_empty_P(keyword, document)
            html_text = str(document)
            pure_text = document.text.strip()

        if not pure_text:
            pure_text = item.get('title')

        item['html'] = html_text
        item['pure_text'] = _clean_text(pure_text)

        # id = item['url'].split('/')[4]
        # fp = open('D:\source_code\spider_html\\' + id + '.html', 'wb')
        # fp.write(bytes(item['html'], encoding='utf8'))
        # fp.close()

    except Exception as e:
        logger.exception("News Item pipeline error " + str(item))


def _clean_text(text):
    """
    格式化纯文本
    :param text: 
    :return: 
    """
    result = text
    result = result.replace("&nbsp;", "")
    new_str = ""
    for line in result.split('\n'):
        line = line.strip()
        if line:
            new_str = '%s\n%s' % (new_str, line)
    return new_str.strip()

