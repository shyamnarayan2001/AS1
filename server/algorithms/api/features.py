# /*
# * ALTIMETRIK CONFIDENTIAL
# * __________________
# *
# * Copyright (c) 2016 - 2017 Altimetrik India Pvt. Ltd.
# * All Rights Reserved.
# *
# * NOTICE:  All information contained herein is, and remains
# * the property of Altimetrik India Pvt. Ltd.
# * The intellectual and technical concepts contained herein are proprietary to Altimetrik India Pvt. Ltd. and may be covered by U.S. and Foreign Patents,
# * patents in process, and are protected by trade secret or copyright law.
# * Dissemination of this information or reproduction of this material
# * is strictly forbidden unless prior written permission is obtained
# * from Altimetrik India Pvt. Ltd.
# */


"""
==================================
  Feature Importance & Selection
==================================

"""

# Import libraries
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from sklearn.feature_selection import f_regression, chi2
import pandas as pd

class FeatureImportance(object):
    
    def __init__(self, df):
        self.df = df
        
    def regressionFeatureImportance(self):
        num_col = len(self.df.columns)
        X = self.df[self.df.columns[range(0,num_col-1)]]
        y = self.df[self.df.columns[num_col-1]]
        F, pval = f_regression(X, y)
        featureDF = pd.DataFrame()
        featureDF['feature'] = self.df.columns[0:-1]
        featureDF['F'] = F
        featureDF['pval'] = pval
        featureDF = featureDF.sort_values(['F'], ascending=[False])
        featureDF = featureDF[0:50]
        return featureDF
    
    def classificationFeatureImportance(self):
        num_col = len(self.df.columns)
        X = self.df[self.df.columns[range(0,num_col-1)]]
        y = self.df[self.df.columns[num_col-1]]
        chi_sq, pval = chi2(X,y)
        featureDF = pd.DataFrame()
        featureDF['feature'] = self.df.columns[0:-1]
        featureDF['F'] = chi_sq
        featureDF['pval'] = pval
        featureDF = featureDF.sort_values(['F'], ascending=[False])
        featureDF = featureDF[0:50]
        return featureDF
