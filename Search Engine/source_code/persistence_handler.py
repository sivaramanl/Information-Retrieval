# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 20:01:19 2020

@author: Sivaraman Lakshmipathy
"""

import os
import json
import pickle
import datetime
from logger_handler import *

#Class to persist the crawled content as JSON files
class crawl_data_persistence_handler:
    current_dir = os.getcwd()
    root_dir = os.path.dirname(current_dir)
    data_dir = root_dir + os.path.sep + "data" + os.path.sep + "crawl_data"

    def get_dir(self):
        return self.data_dir

    def clean_slate(self):
        if os.path.exists(self.data_dir):
            try:
                documents_list = os.listdir(self.data_dir)
                for entry in documents_list:
                    try:
                        os.remove(self.data_dir + os.path.sep + entry)
                    except Exception as e:
                        custom_logger().log_message("Exception while removing file:\n" + str(e), logger_handler.log_level_WARNING)
                        pass
            except Exception as e:
                pass
        else:
            try:
                if not os.path.exists(self.root_dir + os.path.sep + "data"):
                    os.mkdir(self.root_dir + os.path.sep + "data")
                os.mkdir(self.data_dir)
                custom_logger().log_message("Data directory created.", logger_handler.log_level_INFO)
            except Exception as e:
                custom_logger().log_message("Error creating data directory.\n" + str(e), logger_handler.log_level_ERROR)

    def read(self, fileName):
        file_full_path = self.data_dir + os.path.sep + fileName
        try:
            if os.path.exists(file_full_path):
                with open(file_full_path, "r", encoding="utf-8") as f:
                    jsonObj = json.load(f)
                return jsonObj
        except Exception as e:
            custom_logger().log_message("Error while reading file:\n" + str(e), logger_handler.log_level_WARNING)
            pass
        return None

    def update(self, fileName, url, title, content, time=None):
        custom_logger().log_message("Updating:" + fileName + " " + url, logger_handler.log_level_INFO)
        file_full_path = self.data_dir + os.path.sep + fileName
        if os.path.exists(file_full_path):
            if time is None:
                time = datetime.datetime.now().timestamp()

            with open(file_full_path) as f:
                jsonObj = json.load(f)
            jsonObj["url"] = url
            jsonObj["title"] = title
            jsonObj["content"] = content
            jsonObj["time"] = time
            with open(file_full_path, "w") as f:
                json.dump(jsonObj, f)

    def add(self, fileName, url, title=None, content=None, time=None):
        file_full_path = self.data_dir + os.path.sep + fileName
        if os.path.exists(file_full_path):
            custom_logger().log_message("File exists:" + file_full_path, logger_handler.log_level_INFO)
            return
        if time is None:
            time = datetime.datetime.now().timestamp()
        jsonObj = {
            "url": url,
            "title": title,
            "content": content,
            "time": time
        }
        with open(file_full_path, "w") as f:
            json.dump(jsonObj, f)

    def delete(self, fileName):
        custom_logger().log_message("Deleting file:" + fileName, logger_handler.log_level_INFO)
        file_full_path = self.data_dir + os.path.sep + fileName
        try:
            if os.path.exists(file_full_path):
                os.remove(file_full_path)
        except Exception as e:
            custom_logger().log_message("Unable to delete file:" + file_full_path + "\n" + str(e), logger_handler.log_level_WARNING)
            pass


#General class to handle pickle operations
class pickle_handler:

    @staticmethod
    def pickle_object(pickle_filename, object):
        try:
            with open(pickle_filename, "wb") as pickle_file_obj:
                pickle.dump(object, pickle_file_obj)
        except Exception as e:
            custom_logger().log_message("Unable to pickle:" + pickle_filename + "\n" + str(e), logger_handler.log_level_ERROR)

    @staticmethod
    def unpickle_object(pickle_filename):
        try:
            if not os.path.exists(pickle_filename):
                custom_logger().log_message("Pickle file " + pickle_filename + " not found!", logger_handler.log_level_INFO)
                return None

            with open(pickle_filename, "rb") as f:
                ret_obj = pickle.load(f)
                return ret_obj
        except Exception as e:
            custom_logger().log_message("Unable to unpickle:" + pickle_filename + "\n" + str(e), logger_handler.log_level_ERROR)
        return None
