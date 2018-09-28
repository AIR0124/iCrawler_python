# -*- coding: utf-8 -*-


class commonFormat():
    """通用html格式化类"""

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

    def beautifulHtml(self, html):
        """
        格式化html
        :param html: 需格式化的html
        :return: 转化后的html
        """
        html = html.strip()
        if not '<html>' in html and not '<body>' in html:
            html = '<html><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"></head><body>{0}</body></html>'.format(html)
        return html
