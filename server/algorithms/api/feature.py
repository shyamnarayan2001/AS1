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
==========================
        Features
==========================

"""

# Import libraries
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pandas as pd
import numpy as np
import math
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import SelectPercentile, f_regression
print(__doc__)

class FeatureElemination(object):
        
        def chi2test(dataframe):
        p_val = 0.06
        num_col = len(dataframe.columns)
        # Convert Dataframe into array format
        array = dataframe.values
        # Devide data by feature and target data
        X = array[:,0:num_col-1]
        y = array[:,num_col-1]
        # Apply Chi2 test
        test = SelectKBest(score_func=chi2, k=4)
        fit = test.fit(X, y)
        # Get P value
        p_value = fit.pvalues_
        # Select columns whose p value is less than 0.06
        l = []
        for i in range(len(p_value)):
                if p_value[i]<p_val:
                        l.extend([i])
                        # print(l)
                else:
                        print(i,'th Column dropped')
                        
                # print('Columns Selected : ' % l)
                l.extend([num_col-1])
                df = dataframe[dataframe.columns[l]]
        return(df)


        def cor_cov(self, dataframe):
                co_val = .20
        # Apply Correlation and make dataframe
                cor_df = dataframe.corr()
        # Find Row and column number of correlation dataframe
                num_row = len(cor_df.index)
                num_col = len(cor_df.columns)
        # Drop last row of correlation dataframe
                d = cor_df.drop(cor_df.index[[num_row-1]])
        # Select last that means target column
                n = d[d.columns[num_col-1]]
        # from target correlation column find and select feature whose correlation value is      greater 	than 0.20
                l = []
                for i in range(0,len(d.index)):
                        if n[i] > co_val:
                                l.extend([i])

        #num_col = len(d.columns)
                l.extend([num_col-1])
        # Make dataframe according to that(based on correlation value)
                final_df = dataframe[dataframe.columns[l]]

                return(final_df)


                        
        ## F-test based on percentile
        def f_test_by_percentile(self, dataframe):
                p = 30

                num_col = len(dataframe.columns)

                X = dataframe[dataframe.columns[range(0,num_col-2)]]
                y = dataframe[dataframe.columns[num_col-1]]
                selectF_regression = SelectPercentile(f_regression, percentile=p).fit(X, y)
                f_regression_selected = selectF_regression.get_support()
                f_regression_selected_features = [ f for i,f in enumerate(X.columns) if f_regression_selected[i]]
                X_sel = X[f_regression_selected_features]
                df = X_sel.join(y)

                return(df)


        ## Select Value based on p value from F-test
        def f_test_by_p_value(self, dataframe):
                p = 30
                p_val = .06

                num_col = len(dataframe.columns)

                X = dataframe[dataframe.columns[range(0,num_col-2)]]
                y = dataframe[dataframe.columns[num_col-1]]
                selectF_regression = SelectPercentile(f_regression, percentile=p).fit(X, y)
                arr = selectF_regression.pvalues_ 
                l = []
                for i in range(0,len(arr)):
                        if arr[i] < p_val:
                                l.extend([i])

                l.extend([num_col-1])
                final_df = dataframe[dataframe.columns[l]]

                return(final_df)


