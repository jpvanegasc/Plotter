"""
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd


class DataProcessor:
    """
    """
    VALID_EXTENSIONS = ("csv", "txt", "xls", "xlsx", "xlsm", "xlsb", "odf", )

    filepath = ''
    filename = ''
    extension = ''
    base_dir = ''

    df = None
    columns = []

    def __init__(self, path):
        self.__process_filepath(path)
        self.df = self.__get_dataframe(self.filepath)
        self.columns.extend(self.df.columns)

    def __getitem__(self, key):
        if type(key) == int:
            return self.df[self.columns[key]]
        elif type(key) == str:
            return self.df[key]
        else:
            raise TypeError("key must be int or str")

    def __process_filepath(self, path_to_file):
        self.filepath = path_to_file

        filepath = path_to_file.split('/')
        self.filename = filepath[-1].split('.')[0]
        self.extension = filepath[-1].split('.')[-1]

        if self.extension not in self.VALID_EXTENSIONS:
            raise ValueError(f"filetype '.{self.extension}' not supported")

        if len(filepath) > 1:
            self.base_dir = '/'.join(filepath[:-1]) + '/'
        else:
            self.base_dir = "./"

    def __get_dataframe(self, path):
        if self.extension == "csv":
            return pd.read_csv(self.filepath)
        if self.extension == "txt":
            return pd.read_table(self.filepath)
        if self.extension in ("xls", "xlsx", "xlsm", "xlsb", "odf"):
            return pd.read_excel(self.filepath)

    def column_to_log(self, index, base=10, base_e=False):
        """
        """
        key = self.columns[index]

        if base_e == True:
            log_key = f"ln_{key}"
            self.df[log_key] = np.log(self.df[key])
            self.columns.append(log_key)
        elif base == 10:
            log_key = f"log10_{key}"
            self.df[log_key] = np.log10(self.df[key])
            self.columns.append(log_key)
        elif base == 2:
            log_key = f"log2_{key}"
            self.df[log_key] = np.log2(self.df[key])
            self.columns.append(log_key)
        else:
            log_key = f"log{base}_{key}"
            self.df[log_key] = np.log(self.df[key])/np.log(base)
            self.columns.append(log_key)
