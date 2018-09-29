# -*- coding: utf-8 -*-
import re


def extract_advertising(keyword, document):
    """
    提取知乎号里的广告
    :param keyword:
    :param document:
    :return:
    """
    if keyword == 'zhu-yin-lun':
        extract_zhu_yin_lun(document)

def extract_zhu_yin_lun(document):
    """
    朱寅仑号提取
    :param document:
    :return:
    """
    if '关联阅读' or 'Good things | 往期旅行好物推荐' in document.text:
        glyds = document.find_all(name='a', attrs={'class': ' wrap external'})
        if glyds:
            for glyd in glyds:
                href = glyd['href']
                if 'https://link.zhihu.com/?target=' in href:
                    glyd.extract()
        if '关联阅读' in document.text:
            glydTs = document.find_all(name="p", text=re.compile(r'^\s*关联阅读:\s*$'))
            for glydT in glydTs:
                glydT.extract()
        if 'Good things | 往期旅行好物推荐' in document.text:
            gts = document.find_all(name="p", text=re.compile(r'^\s*Good things | 往期旅行好物推荐\s*$'))
            for gt in gts:
                gt.extract()
