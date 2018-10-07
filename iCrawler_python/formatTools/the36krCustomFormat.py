# -*- coding: utf-8 -*-

def extract_advertising(document):
    """
    36氪广告提取
    :param document:
    :return:
    """
    if '编者按：本文来自' in document.text:
        wxgzhs = document.find_all('p')
        if wxgzhs:
            for wxgzh in wxgzhs:
                if '编者按：本文来自' in wxgzh.text:
                    wxgzh.extract()

