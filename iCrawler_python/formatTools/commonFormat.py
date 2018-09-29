# -*- coding: utf-8 -*-


class commonFormat():


    def remove_empty_P(self, document):
        """
        移除文章中空的标签
        :param document:
        :return:
        """
        ps = document.select('p')
        for p in ps:
            if len(p.text.strip()) > 0 or '<img' in str(p):
                continue
            p.extract()

        divs = document.select('div')
        for div in divs:
            if len(div.text.strip()) > 0 or '<img' in str(div):
                continue
            div.extract()
