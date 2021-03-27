# coding=utf-8

import json


class Config:
    def __init__(self):
        self.data = {}

    def load_file(self, filename):
        with open(filename) as a_file:
            self.data = json.load(a_file)

    def get_key(self, key_path):
        array_path = key_path.split('.')
        base = self.data

        for key in array_path:
            if not isinstance(base, dict) or not key in base:
                return None

            base = base[key]

        return base
