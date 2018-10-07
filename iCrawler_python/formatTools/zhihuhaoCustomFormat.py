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
    if keyword == 'ravenblockchain':
        extract_ravenblockchain(document)

def extract_zhu_yin_lun(document):
    """
    朱寅仑号提取
    :param document:
    :return:
    """
    if '关联阅读' in document.text:
        glyds = document.find_all(name='a', attrs={'class': ' wrap external'})
        if glyds:
            for glyd in glyds:
                href = glyd['href']
                if 'https://link.zhihu.com/?target=' in href:
                    glyd.extract()
        if '关联阅读' in document.text:
            glydTs = document.find_all('p')
            for glydT in glydTs:
                if '关联阅读' in glydT.text:
                    glydT.extract()


def extract_ravenblockchain(document):
    """
    ravenblockchain
    :param document:
    :return:
    """
    ps = document.find_all(name='p', text=re.compile(r'^\s*零识仅为翻译中文供大家学习使用，本文版权归英文原作者所有。\s*$'))
    for p in ps:
        p.extract()
