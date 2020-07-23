"""
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd


class DataProcessor:
    """
    """
    VALID_EXTENSIONS = ("csv", "txt", "xls", "xlsx", "xlsm", "xlsb", "odf", )

    filepath = ''
    filename = ''
    extension = ''
    base_dir = ''

    dataframe = None
    columns = []

    def __init__(self, path):
        filepath = path.split('/')
        self.filepath = path
        self.filename = filepath[-1].split('.')[0]
        self.extension = filepath[-1].split('.')[-1]

        if self.extension not in self.VALID_EXTENSIONS:
            raise ValueError(f"filetype '.{self.extension}' not supported")

        if len(path) > 1:
            self.base_dir = '/'.join(filepath[:-1]) + '/'
        else:
            self.base_dir = "./"

        self.dataframe = self.__get_dataframe(self.filepath)
        self.columns.extend(self.dataframe.columns)

    def __getitem__(self, key):
        if type(key) == int:
            return self.dataframe[self.columns[key]]
        elif type(key) == str:
            return self.dataframe[key]
        else:
            raise TypeError("key must be int or str")

    def __get_dataframe(self, path):
        if self.extension == "csv":
            return pd.read_csv(self.filepath)
        if self.extension == "txt":
            return pd.read_table(self.filepath)
        if self.extension in ("xls", "xlsx", "xlsm", "xlsb", "odf"):
            return pd.read_excel(self.filepath)
