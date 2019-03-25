from sklearn.metrics import classification_report
from sklearn.exceptions import UndefinedMetricWarning
import numpy as np
import pandas as pd

from config.config import *
from outlier.outlier import Outlier
from classification.classification import Classification
from outlier.truth import Truth
from preprocessing.preprocessing import process_features
from preprocessing.preprocessing import process_labels

import time

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=UndefinedMetricWarning)

class Detection:
    __outlier = None
    __cls = None
    __truth = None
    __headers = []
    __labels = []
    __classes = []
    __features = []
    __target = []
    __cat_header_list = []
    __categories_list = []
    __truth_size = 0
    __truth_update_frac = 0.0

    def __init__(self, headers, labels, features, target, cat_header_list, categories_list, truth_size, truth_update_frac,
                 threshold_percentile):
        self.__headers = headers
        self.__labels = labels
        self.__classes = [i for i in range(len(labels))]
        self.__features = features
        self.__target = target
        self.__cat_header_list = cat_header_list
        self.__categories_list = categories_list
        self.__truth_size = truth_size
        self.__truth_update_frac = truth_update_frac

        self.__outlier = Outlier(threshold_percentile)
        self.__truth = Truth(truth_size=truth_size, truth_update_frac=truth_update_frac)
        self.__cls = Classification(self.__classes)

        self.__only_cls = Classification(self.__classes)


    def train(self, train_dir):
        self.__log("Loading training data")
        df = pd.read_csv(train_dir, header = None, names = self.__headers)
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

        self.__log("Training base classifier")

        self.__only_cls.train(df_X, df_y['class'].values)

        print("DONE")
        time.sleep(1)

        self.__log("Training outlier ensemble")
        print("")

        normal_X = df_X.iloc[df_y.loc[df_y[self.__target[0]] == 'normal'].index]
        self.__truth.set_truth(normal_X)

        self.__outlier.train(self.__truth.get_truth())

        time.sleep(1)

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

    def __overall_report(self, df_y, y_pred_dict):
        """

        :param df_y: DataFrame containing true classification
        :param y_pred_dict: Dictionary {index : class} where index is member of outlier_indices
        :return: Print overall classiifcation report
        """
        final_pred = np.zeros((df_y.shape[0]))
        for k, v in y_pred_dict.items():
            final_pred[k] = v

        print(classification_report(df_y, final_pred))


    def __outlier_report(self, df_y, outlier_indices):
        detected_attack = 0
        detected_normal = 0
        false_negtive = 0
        false_positive = 0
        count = 0
        max_count = len(outlier_indices)

        for i in range(df_y.shape[0]):
            label = df_y[self.__target[0]][i]
            if count < max_count and i == outlier_indices[count]:
                if label != 'normal':
                    detected_attack += 1
                else:
                    false_positive += 1
                count += 1
            else:
                if label != 'normal':
                    false_negtive += 1
                else:
                    detected_normal += 1
        total = detected_attack + detected_normal + false_positive + false_negtive
        print("")
        print("=========================================")
        print("             OUTLIER ACCURACY            ")
        print("=========================================")
        print("          |   Det Attack       Det Normal  ")
        print("----------|--------------------------------")
        print("Is Attack |   ", detected_attack, "          ", false_negtive)
        print("Is Normal |   ", false_positive, "           ", detected_normal)
        print("")
        print("          |  Det Attack        Det Normal ")
        print("-----------------------------------------")
        print("Is Attack |  ", round(detected_attack / total * 100, 4), "         ", round(false_negtive / total * 100, 4))
        print("Is Normal |  ", round(false_positive / total * 100, 4), "          ", round(detected_normal/total * 100, 4))
        print("")

    def __log(self, message):
        print(message, end='')
        time.sleep(0.3)
        print(".", end='')
        time.sleep(0.3)
        print(".", end='')
        time.sleep(0.3)
        print(".", end='')
        time.sleep(0.3)

if __name__ == '__main__':
    data_directoy = "../../NSL-KDD/"
    train_file = data_directoy + "KDDTrain+.csv"
    train_file_20_percent = data_directoy + "KDDTrain+_20Percent.csv"
    test_file = data_directoy + "KDDTest+.csv"

    det = Detection(headers=headers, labels=labels, features=features, target=target, cat_header_list=cat_header_list,
                    categories_list=categories_list, truth_size=truth_size, truth_update_frac=truth_update_frac,
                    threshold_percentile=threshold_percentile)

    print("==================================================================================")
    print("                                     TRAINING                                     ")
    print("==================================================================================")

    det.train(train_file)

    print("==================================================================================")
    print("                                     TESTING                                      ")
    print("==================================================================================")

    det.predict(test_file)
