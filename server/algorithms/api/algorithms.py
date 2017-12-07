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
====================================
        Algorithms
====================================

"""

# Import libraries
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import pickle
import pandas as pd
import numpy as np
from sklearn import model_selection
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn import ensemble
import threading
import math
import time
from sklearn.svm import LinearSVR
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression

from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
print(__doc__)

# ------------- Train Regression Model ----------------------------


class RegressionTrainMoldel(object):
    """class for all regression algorithms"""

    def __init__(self, dataframe, modelName, test_size=0.33):
        self.df = dataframe
        self.modelName = modelName
        self.X_train = None
        self.X_test = None
        self.Y_train = None
        self.Y_test = None
        # Split the data into training/testing sets
        # 33% will be in test set and remaining training set
        self.test_size = test_size
        self.score = []
        self.alpha_score = []
        self.C_score = []
        self.Rsquare_value = []
        self.C_value = []
        self.alpha_value = []

    def split_data(self):

        # Convert dataframe into array
        array = self.df.values
        # Devide array by independent and dependent variable
        # Last column should be dependent variable
        col_length = len(self.df.columns) - 1
        X = array[:, 0:col_length]
        Y = array[:, col_length]

        seed = 7
        self.X_train, self.X_test, self.Y_train, self.Y_test = model_selection.train_test_split(
            X, Y, test_size=self.test_size, random_state=seed)

    def linearRegression(self):
        # Fit model
        model = LinearRegression()
        model.fit(self.X_train, self.Y_train)

        # Dump the trained linear regression with Pickle
        linearRegression_filename = 'Model/' + self.modelName + '_lineraRegression.pkl'
        model_pkl = open(linearRegression_filename, 'wb')
        pickle.dump(model, model_pkl)
        model_pkl.close()

        # Accuracy score
        score = model.score(self.X_test, self.Y_test)
        self.score.append(['Linear Regression', score])

    def neuralNetwork(self):
        # Here alpha is Lambda value which is Regularization parameter
        # Need to look for Lambda value 0.01 to 10 by 0.01 difference
        alpha_range = np.arange(.0001, .001, .0001)
        # Total number of alpha value
        num_alpha = len(alpha_range)
        # Fit model and print accuracy score for each alpha value

        for i in range(0, num_alpha):
            model = MLPRegressor(alpha=alpha_range[:][i], hidden_layer_sizes=(
                1000, 3), activation='relu', solver='lbfgs', random_state=9)
            model.fit(self.X_train, self.Y_train)
            score = model.score(self.X_test, self.Y_test)
            self.Rsquare_value.append([alpha_range[:][i], score])

        # alpha_score contains all the accuracy score with respect to alpha value
        self.Rsquare_value = np.array(self.Rsquare_value)

        for i in range(1, num_alpha):
            #     if num_alpha <= len(Rsquare_value):
            if self.Rsquare_value[:, 1][i - 1] > self.Rsquare_value[:, 1][i]:
                break
            else:
                self.alpha_value = self.Rsquare_value[:, 0][i - 1]
                # print(Rsquare_value[:,0][i-1],Rsquare_value[:,1][i-1],2)

        #self.alpha_value = np.array([self.alpha_value])

        if len(self.alpha_value) == 0:
            self.alpha_value = self.Rsquare_value[:, 0][0]
        else:
            self.alpha_value = self.alpha_value

        # Fit final model with most suitable alpha value
        model = MLPRegressor(alpha=self.alpha_value, hidden_layer_sizes=(
            1000, 3), activation='relu', solver='lbfgs', random_state=9)
        model.fit(self.X_train, self.Y_train)

        # Dump the trained Ridge Regression with Pickle
        neuralNetwork_filename = 'Model/' + self.modelName + '_neuralNetwork.pkl'
        model_pkl = open(neuralNetwork_filename, 'wb')
        pickle.dump(model, model_pkl)
        model_pkl.close()

        # Rsquare score -Accuracy score
        score = model.score(self.X_test, self.Y_test)
        self.score.append(['Neural Network', score])

    def ridgeRegression(self):
        # Here alpha is Lambda value which is Regularization parameter
        # Need to look for Lambda value 0.01 to 10 by 0.01 difference
        alpha_range = np.arange(0.01, 10.01, 0.01)
        for i in range(0, len(alpha_range)):
            model = Ridge(alpha=alpha_range[i])
            model.fit(self.X_train, self.Y_train)
            score = model.score(self.X_test, self.Y_test)
            self.alpha_score.append([alpha_range[i], score])

        # alpha_score contains all the accuracy score with respect to alpha value
        self.alpha_score = np.array(self.alpha_score)

        # Finding the most accurate model and the alpha value of it
        max_score = max(self.alpha_score[:, 1])
        index_list = np.where(self.alpha_score[:, 1] == max_score)
        index = int(index_list[0][0])

        alpha = self.alpha_score[index][0]

        # Fit model with most suitable alpha value
        model = Ridge(alpha=alpha)
        model.fit(self.X_train, self.Y_train)

        # Dump the trained Ridge Regression with Pickle
        ridgeRegression_filename = 'Model/' + self.modelName + '_ridgeRegression.pkl'
        model_pkl = open(ridgeRegression_filename, 'wb')
        pickle.dump(model, model_pkl)
        model_pkl.close()

        # Accuracy score
        score = model.score(self.X_test, self.Y_test)
        self.score.append(['Ridge Regression', score])

    def supportVectorMachine(self):
        # Need to look for C value 100 to 1000 by 1000 difference
        C_range = np.arange(100, 1000, 100)
        for i in range(0, len(C_range)):
            model = LinearSVR(C=C_range[i])
            model.fit(self.X_train, self.Y_train)
            score = model.score(self.X_test, self.Y_test)
            self.C_score.append([C_range[i], score])

        # C_score contains all the accuracy score with respect to C value
        self.C_score = np.array(self.C_score)

        # Finding the most accurate model and the alpha value of it
        max_score = max(self.C_score[:, 1])
        index_list = np.where(self.C_score[:, 1] == max_score)
        index = int(index_list[0][0])
        C = self.C_score[index][0]

        # Fit model with most suitable C value
        model = LinearSVR(C=C)
        model.fit(self.X_train, self.Y_train)

        # Dump the trained Ridge Regression with Pickle
        supportVectorMachine_filename = 'Model/' + \
            self.modelName + '_supportVectorMachine.pkl'
        model_pkl = open(supportVectorMachine_filename, 'wb')
        pickle.dump(model, model_pkl)
        model_pkl.close()

        # Accuracy score
        score = model.score(self.X_test, self.Y_test)
        self.score.append(['Support Vector Machine', score])

    def gradientBoosting(self, n_weekLearner=300, decisionTreeDepth=4, loss='ls', seed=9):
        # Fit model
        model = ensemble.GradientBoostingRegressor(n_estimators=n_weekLearner,
                                                   max_depth=decisionTreeDepth,
                                                   loss=loss,
                                                   random_state=seed)
        model.fit(self.X_train, self.Y_train)

        # Dump the trained linear regression with Pickle
        gradientBoosting_filename = 'Model/' + self.modelName + '_gradientBoosting.pkl'
        model_pkl = open(gradientBoosting_filename, 'wb')
        pickle.dump(model, model_pkl)
        model_pkl.close()

        # Accuracy score
        score = model.score(self.X_test, self.Y_test)
        self.score.append(['Gradient Boosting', score])

    def adaBoosting(self, decisionTreeDepth=4, n_weekLearner=300, seed=9):
        # Fit model
        model = AdaBoostRegressor(n_estimators=n_weekLearner,
                                  random_state=seed,
                                  loss='linear')
        model.fit(self.X_train, self.Y_train)

        # Dump the trained linear regression with Pickle
        adaBoosting_filename = 'Model/' + self.modelName + '_adaBoosting.pkl'
        model_pkl = open(adaBoosting_filename, 'wb')
        pickle.dump(model, model_pkl)
        model_pkl.close()

        # Accuracy score
        score = model.score(self.X_test, self.Y_test)
        self.score.append(['Ada Boosting', score])


# ------------- Test Regression Model ----------------------------

class RegressionTestMoldel(object):
    """class for all regression algorithms"""

    def __init__(self, dataframe, modelName):
        self.df = dataframe
        self.modelName = modelName
        self.X_test = None
        self.Y_test = None

        self.score = []

    def split_data(self):
        # Convert dataframe into array
        array = self.df.values
        # Devide array by independent and dependent variable
        # Last column should be dependent variable
        col_length = len(self.df.columns) - 1
        self.X_test = array[:, 0:col_length]
        self.Y_test = array[:, col_length]

    def linearRegression(self):
        # Fetch the pre-trained model from pickle
        linearRegression_filename = 'Model/' + self.modelName + '_lineraRegression.pkl'
        model_pkl = open(linearRegression_filename, 'rb')
        model = pickle.load(model_pkl)

        # Test the pre-trained model with new test data
        # Accuracy score
        score = model.score(self.X_test, self.Y_test)
        self.score.append(['Linear Regression', score])

    def neuralNetwork(self):
        # Fetch the pre-trained model from pickle
        neuralNetwork_filename = 'Model/' + self.modelName + '_neuralNetwork.pkl'
        model_pkl = open(neuralNetwork_filename, 'rb')
        model = pickle.load(model_pkl)

        # Test the pre-trained model with new test data
        # Accuracy score
        score = model.score(self.X_test, self.Y_test)
        self.score.append(['neuralNetwork', score])

    def ridgeRegression(self):
        # Fetch the pre-trained model from pickle
        ridgeRegression_filename = 'Model/' + self.modelName + '_ridgeRegression.pkl'
        model_pkl = open(ridgeRegression_filename, 'rb')
        model = pickle.load(model_pkl)

        # Test the pre-trained model with new test data
        # Accuracy score
        score = model.score(self.X_test, self.Y_test)
        self.score.append(['Ridge Regression', score])

    def supportVectorMachine(self):
        # Fetch the pre-trained model from pickle
        supportVectorMachine_filename = 'Model/' + \
            self.modelName + '_supportVectorMachine.pkl'
        model_pkl = open(supportVectorMachine_filename, 'rb')
        model = pickle.load(model_pkl)

        # Test the pre-trained model with new test data
        # Accuracy score
        score = model.score(self.X_test, self.Y_test)
        self.score.append(['Support Vector Machine', score])

    def gradientBoosting(self):
        # Fetch the pre-trained model from pickle
        gradientBoosting_filename = 'Model/' + self.modelName + '_gradientBoosting.pkl'
        model_pkl = open(gradientBoosting_filename, 'rb')
        model = pickle.load(model_pkl)

        # Test the pre-trained model with new test data
        # Accuracy score
        score = model.score(self.X_test, self.Y_test)
        self.score.append(['Gradient Boosting', score])

    def adaBoosting(self):
        # Fetch the pre-trained model from pickle
        adaBoosting_filename = 'Model/' + self.modelName + '_adaBoosting.pkl'
        model_pkl = open(adaBoosting_filename, 'rb')
        model = pickle.load(model_pkl)

        # Test the pre-trained model with new test data
        # Accuracy score
        score = model.score(self.X_test, self.Y_test)
        self.score.append(['Ada Boosting', score])


# ------------- Predict Regression Model ----------------------------

class RegressionPredictMoldel(object):
    """class for all regression algorithms"""

    def __init__(self, dataframe, modelName):
        self.df = dataframe
        self.modelName = modelName

        self.predition = pd.DataFrame()

    def linearRegression(self):
        # Fetch the pre-trained model from pickle
        linearRegression_filename = 'Model/' + self.modelName + '_lineraRegression.pkl'
        model_pkl = open(linearRegression_filename, 'rb')
        model = pickle.load(model_pkl)
        # Predict the dependent variable with the pre-trained model
        self.predition['Linear Regression'] = model.predict(self.df)

    def neuralNetwork(self):
        # Fetch the pre-trained model from pickle
        neuralNetwork_filename = 'Model/' + self.modelName + '_neuralNetwork.pkl'
        model_pkl = open(neuralNetwork_filename, 'rb')
        model = pickle.load(model_pkl)

        # Predict the dependent variable with the pre-trained model
        self.predition['Neural Network'] = model.predict(self.df)

    def ridgeRegression(self):
        # Fetch the pre-trained model from pickle
        ridgeRegression_filename = 'Model/' + self.modelName + '_ridgeRegression.pkl'
        model_pkl = open(ridgeRegression_filename, 'rb')
        model = pickle.load(model_pkl)

        # Predict the dependent variable with the pre-trained model
        self.predition['Ridge Regression'] = model.predict(self.df)

    def supportVectorMachine(self):
        # Fetch the pre-trained model from pickle
        supportVectorMachine_filename = 'Model/' + \
            self.modelName + '_supportVectorMachine.pkl'
        model_pkl = open(supportVectorMachine_filename, 'rb')
        model = pickle.load(model_pkl)

        # Predict the dependent variable with the pre-trained model
        self.predition['Support Vector Machine'] = model.predict(self.df)

    def gradientBoosting(self):
        # Fetch the pre-trained model from pickle
        gradientBoosting_filename = 'Model/' + self.modelName + '_gradientBoosting.pkl'
        model_pkl = open(gradientBoosting_filename, 'rb')
        model = pickle.load(model_pkl)

        # Predict the dependent variable with the pre-trained model
        self.predition['Gradient Boosting'] = model.predict(self.df)

    def adaBoosting(self):
        # Fetch the pre-trained model from pickle
        adaBoosting_filename = 'Model/' + self.modelName + '_adaBoosting.pkl'
        model_pkl = open(adaBoosting_filename, 'rb')
        model = pickle.load(model_pkl)

        # Predict the dependent variable with the pre-trained model
        self.predition['Ada Boosting'] = model.predict(self.df)

# ------------- Train Classification Model ----------------------------


class ClassificationTrainMoldel(object):
    """class for all classification algorithms"""

    def __init__(self, dataframe, modelName, test_size=0.33):
        self.df = dataframe
        self.modelName = modelName
        self.X_train = None
        self.X_test = None
        self.Y_train = None
        self.Y_test = None
        # Split the data into training/testing sets
        # 33% will be in test set and remaining training set
        self.test_size = test_size
        self.score = []
        self.alpha_score = []
        self.alpha_value = []
        self.C_score = []
        self.Rsquare_value = []
        self.C_value = []

    def split_data(self):

        # Convert dataframe into array
        array = self.df.values
        # Devide array by independent and dependent variable
        # Last column should be dependent variable
        col_length = len(self.df.columns) - 1
        X = array[:, 0:col_length]
        Y = array[:, col_length]

        seed = 7
        self.X_train, self.X_test, self.Y_train, self.Y_test = model_selection.train_test_split(
            X, Y, test_size=self.test_size, random_state=seed)

    # ---------- KNeighborsClassifier -------------
    def kNeighborsClassifier(self, n_neighbors=20):
        # Fit model
        model = KNeighborsClassifier(n_neighbors=n_neighbors)
        model.fit(self.X_train, self.Y_train)

        # Dump the trained linear regression with Pickle
        KNeighborsClassifier_filename = 'Model/' + \
            self.modelName + '_kNeighborsClassifier.pkl'
        model_pkl = open(KNeighborsClassifier_filename, 'wb')
        pickle.dump(model, model_pkl)
        model_pkl.close()

        # f1 score
        score = model.score(self.X_test, self.Y_test)
        self.score.append(['K Nearest Neighbour', score])

    # ---------- RandomForestClassifier -------------
    def randomForestClassifier(self, n_estimator=20, seed=9, n_jobs=-1, max_depth=10):
        # Fit model
        model = ensemble.RandomForestClassifier(n_estimators=n_estimator,
                                                random_state=seed,
                                                n_jobs=n_jobs,
                                                max_depth=max_depth)

        model.fit(self.X_train, self.Y_train)

        # Dump the trained linear regression with Pickle
        RandomForestClassifier_filename = 'Model/' + \
            self.modelName + '_randomForestClassifier.pkl'
        model_pkl = open(RandomForestClassifier_filename, 'wb')
        pickle.dump(model, model_pkl)
        model_pkl.close()

        # f1 score
        score = model.score(self.X_test, self.Y_test)
        self.score.append(['Random Forest Classification', score])

    # ---------- GradientBoostingClassifier -------------
    def gradientBoostingClassifier(self, seed=9, n_weekLearner=300):
        # Fit model
        model = ensemble.GradientBoostingClassifier(n_estimators=n_weekLearner,
                                                    random_state=seed)
        model.fit(self.X_train, self.Y_train)

        # Dump the trained linear regression with Pickle
        GradientBoostingClassifier_filename = 'Model/' + self.modelName + '_gradientBoostingClassifier.pkl'
        model_pkl = open(GradientBoostingClassifier_filename, 'wb')
        pickle.dump(model, model_pkl)
        model_pkl.close()

        # f1 score
        score = model.score(self.X_test, self.Y_test)
        self.score.append(['Gradient Boosting Classification', score])

    # ---------- LogisticRegression -------------
    def logisticRegression(self, seed=9):
        # Fit model
        model = LogisticRegression(multi_class='ovr',
                                   random_state=seed)
        model.fit(self.X_train, self.Y_train)

        # Dump the trained linear regression with Pickle
        LogisticRegression_filename = 'Model/' + self.modelName + '_logisticRegression.pkl'
        model_pkl = open(LogisticRegression_filename, 'wb')
        pickle.dump(model, model_pkl)
        model_pkl.close()

        # f1 score
        score = model.score(self.X_test, self.Y_test)
        self.score.append(['Logistic Regression', score])

    def adaBoostClassifier(self, decisionTreeDepth=4, n_weekLearner=300, seed=9):
        # Fit model
        model = AdaBoostClassifier(n_estimators=n_weekLearner,
                                   random_state=seed)
        model.fit(self.X_train, self.Y_train)

        # Dump the trained linear regression with Pickle
        AdaBoostClassifier_filename = 'Model/' + self.modelName + '_adaBoostClassifier.pkl'
        model_pkl = open(AdaBoostClassifier_filename, 'wb')
        pickle.dump(model, model_pkl)
        model_pkl.close()

        # Accuracy score
        score = model.score(self.X_test, self.Y_test)
        self.score.append(['Ada Boosting Classification', score])

    def supportVectorMachine_Classifier(self):
        # Need to look for C value 100 to 1000 by 1000 difference
        C_range = np.arange(100, 1000, 100)
        for i in range(0, len(C_range)):
            model = LinearSVC(C=C_range[i])
            model.fit(self.X_train, self.Y_train)
            score = model.score(self.X_test, self.Y_test)
            self.C_score.append([C_range[i], score])

        # C_score contains all the accuracy score with respect to C value
        self.C_score = np.array(self.C_score)

        # Finding the most accurate model and the alpha value of it
        max_score = max(self.C_score[:, 1])
        index_list = np.where(self.C_score[:, 1] == max_score)
        index = int(index_list[0][0])
        C = self.C_score[index][0]

        # Fit model with most suitable C value
        model = LinearSVC(C=C)
        model.fit(self.X_train, self.Y_train)

        # Dump the trained Ridge Regression with Pickle
        supportVectorMachine_Classifier_filename = 'Model/' + self.modelName + '_supportVectorMachine_Classifier.pkl'
        model_pkl = open(supportVectorMachine_Classifier_filename, 'wb')
        pickle.dump(model, model_pkl)
        model_pkl.close()

        # Accuracy score
        score = model.score(self.X_test, self.Y_test)
        self.score.append(['Support Vector Machine Classification', score])


# ------------- Test Classification Model ----------------------------

class ClassificationTestMoldel(object):
    """class for all classification algorithms"""

    def __init__(self, dataframe, modelName):
        self.df = dataframe
        self.modelName = modelName
        self.X_test = None
        self.Y_test = None

        self.score = []

    def split_data(self):
        # Convert dataframe into array
        array = self.df.values
        # Devide array by independent and dependent variable
        # Last column should be dependent variable
        col_length = len(self.df.columns) - 1
        self.X_test = array[:, 0:col_length]
        self.Y_test = array[:, col_length]

    def kNeighborsClassifier(self):
        # Fetch the pre-trained model from pickle
        KNeighborsClassifier_filename = 'Model/' + self.modelName + '_kNeighborsClassifier.pkl'
        model_pkl = open(KNeighborsClassifier_filename, 'rb')
        model = pickle.load(model_pkl)

        # Test the pre-trained model with new test data
        # Accuracy score
        score = model.score(self.X_test, self.Y_test)
        self.score.append(['K Nearest Neighbour', score])

    def randomForestClassifier(self):
        # Fetch the pre-trained model from pickle
        RandomForestClassifier_filename = 'Model/' + self.modelName + '_randomForestClassifier.pkl'
        model_pkl = open(RandomForestClassifier_filename, 'rb')
        model = pickle.load(model_pkl)

        # Test the pre-trained model with new test data
        # Accuracy score
        score = model.score(self.X_test, self.Y_test)
        self.score.append(['Random Forest Classification', score])

    def gradientBoostingClassifier(self):
        # Fetch the pre-trained model from pickle
        gradientBoostingClassifier_filename = 'Model/' + self.modelName + '_gradientBoostingClassifier.pkl'
        model_pkl = open(gradientBoostingClassifier_filename, 'rb')
        model = pickle.load(model_pkl)

        # Test the pre-trained model with new test data
        # Accuracy score
        score = model.score(self.X_test, self.Y_test)
        self.score.append(['Gradient Boosting Classification', score])

    def logisticRegression(self):
        # Fetch the pre-trained model from pickle
        LogisticRegression_filename = 'Model/' + self.modelName + '_logisticRegression.pkl'
        model_pkl = open(LogisticRegression_filename, 'rb')
        model = pickle.load(model_pkl)

        # Test the pre-trained model with new test data
        # Accuracy score
        score = model.score(self.X_test, self.Y_test)
        self.score.append(['Logistic Regression', score])

    def adaBoostClassifier(self):
        # Fetch the pre-trained model from pickle
        AdaBoostClassifier_filename = 'Model/' + self.modelName + '_adaBoostClassifier.pkl'
        model_pkl = open(AdaBoostClassifier_filename, 'rb')
        model = pickle.load(model_pkl)

        # Test the pre-trained model with new test data
        # Accuracy score
        score = model.score(self.X_test, self.Y_test)
        self.score.append(['Ada Boosting Classification', score])

    def supportVectorMachine_Classifier(self):
        # Fetch the pre-trained model from pickle
        supportVectorMachine_Classifier_filename = 'Model/' + self.modelName + '_supportVectorMachine_Classifier.pkl'
        model_pkl = open(supportVectorMachine_Classifier_filename, 'rb')
        model = pickle.load(model_pkl)

        # Test the pre-trained model with new test data
        # Accuracy score
        score = model.score(self.X_test, self.Y_test)
        self.score.append(['Support Vector Machine Classification', score])


# ------------- Predict Classificaion Model ----------------------------

class ClassificaionPredictMoldel(object):
    """class for all regression algorithms"""

    def __init__(self, dataframe, modelName):
        self.df = dataframe
        self.modelName = modelName

        self.predition = pd.DataFrame()

    def kNeighborsClassifier(self):
        # Fetch the pre-trained model from pickle
        KNeighborsClassifier_filename = 'Model/' + self.modelName + '_kNeighborsClassifier.pkl'
        model_pkl = open(KNeighborsClassifier_filename, 'rb')
        model = pickle.load(model_pkl)
        # Predict the dependent variable with the pre-trained model
        self.predition['K Nearest Neighbour'] = model.predict(self.df)

    def randomForestClassifier(self):
        # Fetch the pre-trained model from pickle
        RandomForestClassifier_filename = 'Model/' + self.modelName + '_randomForestClassifier.pkl'
        model_pkl = open(RandomForestClassifier_filename, 'rb')
        model = pickle.load(model_pkl)

        # Predict the dependent variable with the pre-trained model
        self.predition['Random Forest Classification'] = model.predict(self.df)

    def gradientBoostingClassifier(self):
        # Fetch the pre-trained model from pickle
        gradientBoostingClassifier_filename = 'Model/' + self.modelName + '_gradientBoostingClassifier.pkl'
        model_pkl = open(gradientBoostingClassifier_filename, 'rb')
        model = pickle.load(model_pkl)

        # Predict the dependent variable with the pre-trained model
        self.predition['Gradient Boosting Classification'] = model.predict(
            self.df)

    def logisticRegression(self):
        # Fetch the pre-trained model from pickle
        LogisticRegression_filename = 'Model/' + self.modelName + '_logisticRegression.pkl'
        model_pkl = open(LogisticRegression_filename, 'rb')
        model = pickle.load(model_pkl)

        # Predict the dependent variable with the pre-trained model
        self.predition['Logistic Regression'] = model.predict(self.df)

    def adaBoostClassifier(self):
        # Fetch the pre-trained model from pickle
        AdaBoostClassifier_filename = 'Model/' + self.modelName + '_adaBoostClassifier.pkl'
        model_pkl = open(AdaBoostClassifier_filename, 'rb')
        model = pickle.load(model_pkl)

        # Predict the dependent variable with the pre-trained model
        self.predition['Ada Boosting Classification'] = model.predict(self.df)

    def supportVectorMachine_Classifier(self):
        # Fetch the pre-trained model from pickle
        supportVectorMachine_Classifier_filename = 'Model/' + self.modelName + '_supportVectorMachine_Classifier.pkl'
        model_pkl = open(supportVectorMachine_Classifier_filename, 'rb')
        model = pickle.load(model_pkl)

        # Predict the dependent variable with the pre-trained model
        self.predition['Support Vector Machine Classification'] = model.predict(
            self.df)


class CheckRegressionOrClassification(object):

    def regression_or_classification(self, modelName):
        path = 'InputDataFrame//' + modelName + '.pkl'
        df = pd.read_pickle(path)

        r, c = df.shape
        #------To find the target in the dataset
        target = df.iloc[:, c - 1]
        a = list(df)[c - 1]
        grps = len(df.iloc[:, c - 1].unique())
        prcnt = 0.02
        #------Keeping 20% of the dataset cutoff for the  decision
        cutoffRange = math.floor(prcnt * r)
        if grps > cutoffRange:
            return ("Regression")
        else:
            return ("Classification")


class RunAlgorithm (threading.Thread):

    def __init__(self, algoName, algoObject):

        threading.Thread.__init__(self)
        self.algoName = algoName
        self.algoObject = algoObject

    def run(self):

        # algo_list = algo_name = ['Logistic Regression' , 'Support Vector Machine Classification' , 'Random Forest Classification', 'K Nearest Neighbour' , 'Gradient Boosting Classification' , 'Ada Boosting Classification']
        if self.algoName == 'Linear Regression':
            self.algoObject.linearRegression()

        if self.algoName == 'Neural Network':
            self.algoObject.neuralNetwork()

        elif self.algoName == 'Ridge Regression':
            self.algoObject.ridgeRegression()

        elif self.algoName == 'Support Vector Machine':
            self.algoObject.supportVectorMachine()

        elif self.algoName == 'Gradient Boosting':
            self.algoObject.gradientBoosting()

        elif self.algoName == 'Ada Boosting':
            self.algoObject.adaBoosting()

        elif self.algoName == 'Logistic Regression':
            self.algoObject.logisticRegression()

        elif self.algoName == 'Support Vector Machine Classification':
            self.algoObject.supportVectorMachine_Classifier()

        elif self.algoName == 'Random Forest Classification':
            self.algoObject.randomForestClassifier()

        elif self.algoName == 'K Nearest Neighbour':
            self.algoObject.kNeighborsClassifier()

        elif self.algoName == 'Gradient Boosting Classification':
            self.algoObject.gradientBoostingClassifier()

        elif self.algoName == 'Ada Boosting Classification':
            self.algoObject.adaBoostClassifier()
