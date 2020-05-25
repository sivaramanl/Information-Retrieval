# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 20:01:19 2020

@author: Sivaraman Lakshmipathy
"""

from bs4 import BeautifulSoup

#Class to parse the crawled HTML files and extract the contents and outgoing links
class html_parser:
    ignore_tags = ['style', 'script', 'link', 'header', 'svg', 'nav', 'form', 'input', 'img', 'footer', 'meta', 'path']

    def __init__(self, source, parser="html.parser"):
        self.soup_obj = None
        self.valid = False
        self.titles = []
        self.initialize(source, parser)

    def initialize(self, source, parser):
        self.soup_obj = BeautifulSoup(source, parser)
        self.populate_titles()
        self.clean_soup()
        if len(self.titles) > 0:
            self.valid = True
        self.isValid()

    def isValid(self):
        return self.valid

    def clean_soup(self):
        for tag in self.soup_obj(self.ignore_tags):
            tag.decompose()

    def get_text(self):
        #Extract the content
        return self.soup_obj.get_text().strip()

    def get_title(self):
        return self.titles[0]

    def get_titles(self):
        return self.titles

    def populate_titles(self):
        title_texts = self.soup_obj.find_all('title')
        for title_text in title_texts:
            self.titles.append(title_text.get_text().strip())

    def get_links(self):
        #Extract the outgoing links
        outgoing_links = []
        for link in self.soup_obj.find_all('a'):
            if link not in outgoing_links:
                outgoing_links.append(link.get('href'))
        return outgoing_links
