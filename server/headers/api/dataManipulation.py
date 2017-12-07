#!/usr/bin/python
# -*- coding: utf-8 -*-


# ALTIMETRIK CONFIDENTIAL
# __________________
#
# Copyright (c) 2016 - 2017 Altimetrik India Pvt. Ltd.
# All Rights Reserved.
#
# NOTICE:  All information contained herein is, and remains
# the property of Altimetrik India Pvt. Ltd.
# The intellectual and technical concepts contained herein are proprietary to Altimetrik India Pvt. Ltd. and may be covered by U.S. and Foreign Patents,
# patents in process, and are protected by trade secret or copyright law.
# Dissemination of this information or reproduction of this material
# is strictly forbidden unless prior written permission is obtained
# from Altimetrik India Pvt. Ltd.


"""
====================
  Data Manipulation
====================

"""

# Import libraries
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import pandas as pd
import numpy as np
# import pymysql
from sqlalchemy import create_engine
from pywebhdfs.webhdfs import PyWebHdfsClient
import re

print(__doc__)

# --------- Changing the format of messages in log file -----------

# logging.basicConfig(filename='log.log' , format='%(levelname)s:%(asctime)s- %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p' , level=logging.DEBUG)
# logger = logging.getLogger()


class InputData(object):
    """Class for all the operations related to input the data"""

    def __init__(self):
        self.df = pd.DataFrame()

    def CSV(self, filePath, header):
        # print ('I am getting called')
        flag = 'fine'

        try:
            if header == 'n':
                self.df = pd.read_csv(filePath, header=None)
                no_of_cols = len(self.df.columns)
                array = np.arange(1, no_of_cols + 1)
                self.df.columns = array
            else:
                self.df = pd.read_csv(filePath)
        except Exception as exception:
            flag = 'Unable to process your data. Might be in the wrong format.'
        finally:
            return (flag)

    def excel(self, filePath, header):
        flag = 'fine'
        try:
            if header == 'n':
                self.df = pd.read_excel(filePath, header=None)
                no_of_cols = len(self.df.columns)
                array = np.arange(1, no_of_cols + 1)
                self.df.columns = array
            else:
                self.df = pd.read_excel(filePath)
        except Exception as exception:
            flag = 'Unable to process your data. Might be in the wrong format.'
        finally:
            return (flag)

    def mysql(self, host, user, password, db, tableName, port=3306):
        flag = 'fine'
        try:
            engine = create_engine(
                'mysql+mysqlconnector://root:root@localhost:3306/altisolve')
            conn = engine.raw_connection()

            # connection = pymysql.connect(host= 'localhost', user = 'root', password = 'root',
            #                              db = 'altisolve', port = 3306)
            # print (connection)
            # self.df = pd.read_sql("SELECT * FROM alti_data" ,connection)
            # print (self.df)
        except Exception as exception:
            flag = exception
        finally:
            return (flag)

    def hdfsConnect(self, host, port, dir):
        flag = 'fine'
        try:
			# hdfs =  PyWebHdfsClient(host='vsl080hachon02.altimetrik.com',port='50070')
            hdfs = PyWebHdfsClient(host=host, port=port)
            path = dir
            
            dir_files = hdfs.list_dir(path)
            file_name = dir_files["FileStatuses"]
            dataArray = []

            df1 = pd.DataFrame()
            df2 = pd.DataFrame()

            for item in file_name["FileStatus"]:
                a= (item["pathSuffix"])
                if re.search(r"json", a):
                    # data = hdfs.read_file(path + a)
                    data = hdfs.read_file(path + 'newdata.json')
                    dataArray.append(data)
                    
            try:
                for i in dataArray:
                    df1 = pd.concat([df1,df2])
                    my_json = i.decode('utf8').replace("'", '"')
                    df2 = pd.read_json(my_json)

                df1 = pd.concat([df1,df2])
                self.df = df1

            except Exception as exception:
                flag = 'All json files have different forms of data. Unable to process.'
                return (flag)

        except Exception as exception:
            flag = exception
        finally:
            return (flag)

class ManipulateData(object):
    """Class for all the manupulation task to the data"""

    def fetchColumns(self, df):
        col = df.columns
        header = col.tolist()
        return (header)

    def dataPreprocessing(self, identifier, features, target, df):
        updated_df = pd.DataFrame()
        # Set the identifier
        if identifier == 'no identifier':
            no_of_rows = (df.shape[0])
            array = np.arange(1, no_of_rows + 1)
            updated_df['Identifier'] = array
        else:
            updated_df[identifier] = df[identifier]

        # Set all the features
        for i in features:
            updated_df[features] = df[features]

        # Set all the target
        for i in target:
            updated_df[target] = df[target]

        return (updated_df)

    def DataCleaning(self, df, target):
        no_of_targets = len(target)
        dg = pd.DataFrame()
        dx = pd.DataFrame()
        dy = pd.DataFrame()
        dz = pd.DataFrame()
        dx[df.columns.values[0]] = df[df.columns.values[0]]
        # Intial feature list
        feature_list = df.columns.values.tolist()
        # Removing Identifier
        del(feature_list[0])
        # Removing Targets
        for i in range(0, no_of_targets):
            del(feature_list[df.columns.values.size - no_of_targets - 1])
        # Removing Numeric Columns
        numeric_columns = df._get_numeric_data().columns
        feature_list.remove(numeric_columns)
        dw = df[numeric_columns]
        # dy =pd.get_dummies(df[feature_list],columns =feature_list, drop_first=True)
        dy = pd.get_dummies(df[feature_list], columns=feature_list)
        for i in range(0, no_of_targets):
            # Target columns are placed at the end of dataframe
            column_index = df.columns.values.size - i - 1
            D = {df.columns.values[column_index]
                : df[df.columns.values.tolist()[column_index]]}
            df_target = pd.DataFrame.from_dict(D)
            # print(df_target)

        # target variable encoding using label encoding
        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        for col in df_target.columns.values:
            # Encoding only categorical variables
            if df_target[col].dtypes == 'object':
                # Using whole data to form an exhaustive list of levels
                data = df_target[col]
                le.fit(data.values)
                df_target[col] = le.transform(df_target[col])
            # df_full_target[df.columns.values[column_index]] =df_target
                dz[col] = df_target
        dg = pd.concat([dx, dw, dy, dz], axis=1)
        return(dg)

    def arrangeDf(self, modelName, identifier, features, target):
        path = 'InputDataFrame//' + modelName + '.pkl'
        df = pd.read_pickle(path)
        modified_df = pd.DataFrame()
        for i in features:
            modified_df[i] = df[i]
        
        if (target != "no target"):
            modified_df[target] = df[target]

        modified_df.to_pickle(path)
