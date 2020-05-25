# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 20:01:19 2020

@author: Sivaraman Lakshmipathy
"""

import os
import sys
import hashlib
import datetime
from lda import *
from indexer import *
from pagerank import *
from html_parser import *
from logger_handler import *
from urllib import robotparser
from persistence_handler import *
from urllib.request import urlopen
from ssl import SSLError, CertificateError
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse, urlunparse

#Class to perform the web crawling operations
class crawler:
    url_hash_pickle_filename = os.path.dirname(os.getcwd()) + os.path.sep + "data" + os.path.sep + "url_hash"

    def __init__(self, persist_obj=None, network_graph=None, indexer_param=None, crawler_name="*"):
        custom_logger().log_message("Initializing crawler", logger_handler.log_level_INFO)
        self.root_dir = ""
        self.root_urls = []
        self.max_crawl = 3000
        self.crawler_rules = {}
        self.crawler_name = crawler_name
        if persist_obj is None:
            self.persistObj = crawl_data_persistence_handler()
        else:
            self.persistObj = persist_obj
        self.persistObj.clean_slate()
        if indexer_param is None:
            self.indexer = indexer()
        else:
            self.indexer = indexer_ip
        self.url_hash = {}

        if network_graph is None:
            self.network_graph = graph()
        else:
            self.network_graph = network_graph

        current_dir = os.getcwd()
        self.root_dir = os.path.dirname(current_dir)
        self.load_configuration()

    def load_configuration(self):
        config_file_path = self.root_dir + os.path.sep + "config" + os.path.sep + "root_config.txt"

        if not os.path.exists(config_file_path):
            custom_logger().log_message("Configuration file not found. Exiting crawler.", logger_handler.log_level_CRITICAL)
            print("Configuration file not found. Exiting crawler.")
            return

        try:
            with open(config_file_path) as config_file:
                config_entries = config_file.readlines()

            for entry in config_entries:
                if "root_urls=" in entry:
                    urls = entry.split("root_urls=")[1]
                    self.root_urls = urls.strip().split(",")
                if "max_crawl=" in entry:
                    self.max_crawl = int(entry.split("max_crawl=")[1])
        except Exception as e:
            custom_logger().log_message("Error while configuring crawler. Exiting.", logger_handler.log_level_CRITICAL)
            return

        self.run()

    def can_crawl(self, url):
        url_components = urlparse(url)

        url_root = url_components.netloc

        # Check if URL in UIC domain
        if "uic.edu" not in url_root:
            return False

        # Check robots rules
        if url_root not in self.crawler_rules:
            self.locate_rules(url_components)

        rp = self.crawler_rules[url_root]
        if rp is not None:
            return rp.can_fetch(self.crawler_name, url)
        else:
            return False

    def locate_rules(self, root_url):
        try:
            robots_url = urlunparse((root_url.scheme, root_url.netloc, "robots.txt", "", "", ""))
            robots = robotparser.RobotFileParser()
            robots.set_url(robots_url)
            robots.read()
            self.crawler_rules[root_url.netloc] = robots
        except Exception as e:
            custom_logger().log_message("Exception in robots:\n" + str(e), logger_handler.log_level_ERROR)
            self.crawler_rules[root_url.netloc] = None

    def run(self):
        custom_logger().log_message("Crawler sequence activated.", logger_handler.log_level_INFO)
        url_queue = []
        seen = set()

        # Populate the queue initial URLs
        for url in self.root_urls:
            url = self.get_clean_url(url)
            if url is not None:
                url_queue.append(url)
                url_hash = self.get_hash(self.get_plain_url(url))
                self.url_hash[url] = url_hash

        # BFS to fetch crawled data and construct the network graph
        while len(url_queue) > 0 and len(seen) < self.max_crawl:
            cur_url = url_queue.pop(0)
            cur_plain_url = self.get_plain_url(cur_url)
            if cur_plain_url not in seen and self.can_crawl(cur_url):
                cur_hash = self.url_hash[cur_url]
                parsed_content = self.process_url(cur_url)
                if parsed_content is not None and parsed_content.isValid():
                    seen.add(cur_plain_url)

                    #Persist file contents
                    self.persistObj.add(cur_hash, cur_url, parsed_content.get_title(), parsed_content.get_text())

                    links = [self.get_clean_url(link, cur_url) for link in parsed_content.get_links()]
                    for link in links:
                        if link is not None:
                            if link not in self.url_hash:
                                link_hash = self.get_hash(self.get_plain_url(link))
                                self.url_hash[link] = link_hash
                            else:
                                link_hash = self.url_hash[link]
                            self.network_graph.add_edge(cur_hash, link_hash)
                            if self.get_plain_url(link) not in seen and link not in url_queue:
                                url_queue.append(link)
                else:
                    self.persistObj.delete(cur_hash)
                    self.url_hash.pop(cur_url, None)

        custom_logger().log_message("Crawler sequence completed.", logger_handler.log_level_INFO)

        #Page Rank
        pagerank(self.network_graph)

        #Indexer
        self.indexer.run_indexer()

        #LDA training
        lda().run()

    @staticmethod
    def get_hash(val):
        return hashlib.md5(val.encode()).hexdigest()

    @staticmethod
    def get_plain_url(url):
        url = url.split("://")[1]
        if url.startswith("www."):
            url = url[4:]
        return url

    @staticmethod
    def get_clean_url(url, root_url=""):
        if url == "None" or url is None:
            return None
        try:
            url = url.strip()
            if url.startswith("/"):
                root_url = urlparse(root_url)
                url = urlunparse((root_url.scheme, root_url.netloc, url, "", "", ""))
            parsed_url = urlparse(url)
            if parsed_url.scheme == 'http' or parsed_url.scheme == 'https':
                if "uic.edu" in parsed_url.netloc:
                    if len(parsed_url.fragment) > 0:
                        url = url.rsplit("#", maxsplit=1)[0]
                    if url.endswith("/"):
                        url = url.rstrip("/")
                    return url
            return None
        except Exception as e:
            custom_logger().log_message("Exception URL:\n" + url + "\n" + str(e), logger_handler.log_level_ERROR)
        return None

    @staticmethod
    def process_url(url):
        try:
            url_obj = urlopen(url)
            if url_obj.status == 200 and 'text/html' in url_obj.getheader('Content-Type'):
                custom_logger().log_message("Crawled URL:" + url, logger_handler.log_level_INFO)
                cur_page = url_obj.read().decode('utf-8')
                parsed_content = html_parser(cur_page)
                return parsed_content
        except(HTTPError, TimeoutError, URLError, SSLError, CertificateError, UnicodeDecodeError) as e1:
            custom_logger().log_message("Exception while crawling URL:\n" + str(e1), logger_handler.log_level_ERROR)
        except Exception as e:
            custom_logger().log_message("Exception while crawling URL:\n" + str(e), logger_handler.log_level_ERROR)
        return None
