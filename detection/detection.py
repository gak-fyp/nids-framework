import numpy as np
import pandas as pd
import time

from detection.outlier.outlier import Outlier
from detection.classification.classification import Classification
from detection.outlier.truth.truth import Truth


class Detection:
    __outlier = None
    __cls = None
    __truth = None
    __scale_cls = None

    __classes = []
    __threshold_percentile = 0.0
    __truth_size = 0
    __truth_update_frac = 0.0

    def __init__(self, classes, threshold_percentile, truth_size, truth_update_frac, truth_save_folder, outlier_save_folder,
                 classifier_save_folder):
        self.__classes = classes
        self.__threshold_percentile = threshold_percentile
        self.__truth_size = truth_size
        self.__truth_update_frac = truth_update_frac

        self.__outlier = Outlier(threshold_percentile, outlier_save_folder)
        self.__truth = Truth(truth_size, truth_update_frac, truth_save_folder)
        self.__cls = Classification(self.__classes, classifier_save_folder)

    def initialize(self, normal_data, X, y):
        self.__truth.set_truth(normal_data)
        self.__outlier.train(self.__truth.get_truth())
        self.__cls.train(X, y)

    def detect_outliers(self, X):
        self.__log("Detecting outliers")
        print("")
        outlier_indices = self.__outlier.predict(X)
        return outlier_indices

    def classfiy(self, X):
        y_pred = self.__cls.predict(X)
        return y_pred

    def update_outlier(self, new_truth):
        if len(new_truth) > 0:
            self.__truth.update_truth(new_truth)
            self.__outlier.update(self.__truth.get_truth())

    def update_classifier(self, X, y):
        self.__cls.update(X, y)

    def train(self, train_file):



        """
        print("Training accuracy...")
        outlier_indices = self.__outlier.predict(df_X)

        self.__outlier_report(df_y, outlier_indices)

        
        # Temporary Block
        #---------------------------------------------------
        print("Training Classifier directly...")
        cls_X = df_X
        cls_y = df_y['class'].values

        cls = Classification(self.__classes)
        cls.train(cls_X, cls_y)

        print("Checking classification accuracy...")
        cls_pred = cls.predict(cls_X)

        print(classification_report(cls_y, cls_pred))
        # ---------------------------------------------------
        """

        self.__log("Finding outliers in training data for classification training")
        print("")
        outlier_indices = self.__outlier.predict(df_X)

        self.__log("Training classification ensemble")
        cls_X = df_X.iloc[outlier_indices]
        cls_y = df_y['class'].iloc[outlier_indices].values

        self.__cls.train(cls_X, cls_y)

        print("DONE")
        time.sleep(1)

        """
        print("Training accuracy...")
        cls_pred = self.__cls.predict(cls_X)
        y_pred_dict = {outlier_indices[i] : cls_pred[i] for i in range(len(outlier_indices))}
        self.__overall_report(df_y['class'], y_pred_dict)
        """

    def __log(self, message):
        print(message, end='')
        time.sleep(0.3)
        print(".", end='')
        time.sleep(0.3)
        print(".", end='')
        time.sleep(0.3)
        print(".", end='')
        time.sleep(0.3)

    def predict(self, test_dir):

        self.__log("Loading testing data")
        df = pd.read_csv(test_dir, header=None, names=self.__headers)
        print("DONE")
        time.sleep(1)

        self.__log("Preprocessing data")
        df_X = df[self.__features].copy()
        df_X = process_features(df_X, self.__cat_header_list, self.__categories_list)
        df_X = df_X.astype(np.float64)

        df_y = df[self.__target].copy()
        df_y = process_labels(df_y, self.__target, self.__labels, self.__classes)

        print("DONE")
        time.sleep(1)


        # Temporary Block
        #------------------------------------------------------------
        self.__log("Running classifier only")
        print("")
        time.sleep(1)

        cls_X = df_X
        cls_y = df_y['class'].values

        cls_pred = self.__only_cls.predict(cls_X)

        print("=========================================")
        print("          CLASSIFICATION ACCURACY        ")
        print("=========================================")

        print(classification_report(cls_y, cls_pred))
        cls_X = 0
        cls_y = 0
        cls_pred = 0
        # ------------------------------------------------------------


        self.__log("Running IDS")
        print("")
        time.sleep(1)
        self.__log("Detecting outliers")
        print("")

        outlier_indices = self.__outlier.predict(df_X)

        print("")
        time.sleep(1)

        self.__outlier_report(df_y, outlier_indices)

        self.__log("Predicting attack classes")

        cls_X = df_X.iloc[outlier_indices]
        cls_y = df_y['class'].iloc[outlier_indices].values

        cls_pred = self.__cls.predict(cls_X)

        print("DONE")
        time.sleep(1)

        y_pred_dict = {outlier_indices[i]: cls_pred[i] for i in range(len(outlier_indices))}

        print("=========================================")
        print("         OUTLIER + CLASSIFICATION        ")
        print("=========================================")

        self.__overall_report(df_y['class'], y_pred_dict)

