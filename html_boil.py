# $Id: html_boil.py 154 2017-11-01 18:01:50Z jmcfarren $

import re
from html.parser import HTMLParser

class HtmlBoil(HTMLParser):


    def __init__(self, settings):
        super().__init__()
        self.reset()
        self.debug = False
        self.settings = settings
        self.strict = False
        self.parent = []
        self.links = []
        self.convert_charrefs = True
        self.fed = []


    def handle_starttag(self, tag, attrs):
        self.parent.append(tag)
        if self.debug == True:
            self.fed.append("\n" + str(self.parent) + "\n")
        if tag == 'a':
            self.links.append(self.getAttr('href', attrs))
        if tag == 'div':
            self.fed.append(self.settings.get('div_before'))


    def handle_endtag(self, tag):
        if self.debug == True:
            self.fed.append("\n" + str(self.parent) + "\n")
        self.parent.pop()
        if tag == 'a':
            link = self.links.pop()
            if link != None:
                self.fed.append(self.settings.get('link_before'))
                self.fed.append(link.strip())
                self.fed.append(self.settings.get('link_after'))
        if tag == 'div':
            self.fed.append(self.settings.get('div_after'))


    def handle_startendtag(self, tag, attrs):
        if tag == 'img':
            self.fed.append(self.settings.get('alt_before'))
            self.fed.append(self.getAttr('alt', attrs))
            self.fed.append(self.settings.get('alt_after'))
        if tag == 'br':
            self.fed.append(self.settings.get('br_after'))


    def handle_data(self, content):
        if self.parent and not self.parent[-1] in self.settings.get('skip_inner'):
            self.fed.append(content)


    def handle_entityref(self, name):
        self.fed.append(self.unescape('&' + name + ';'))


    def get_data(self):
        return ''.join(self.fed)


    def getAttr(self, attr, attrs = []):
        for a in attrs:
            if a[0] == attr:
                return a[1]


    def removeIndent(self, content):
        new_lines = []
        old_lines = content.splitlines()
        for old_line in old_lines:
            if old_line.strip() != '':
                new_lines.append(old_line.strip())
        return "\n\n".join(new_lines)
