#coding: utf-8
import json

class CSettings:
    def __init__(self, jsonFile):
        self.__json = {}
        self.Import(jsonFile)

    def Json(self):
        return self.__json

    def Import(self, jsonFile):
        with open(jsonFile, 'r') as f:
            self.__json = json.load(f)
