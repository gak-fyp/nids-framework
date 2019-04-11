import pandas as pd
import numpy as np
from sklearn.metrics import classification_report
from sklearn.exceptions import UndefinedMetricWarning

import matplotlib.pyplot as plt

import random as rd
import time
import sys

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=UndefinedMetricWarning)

from config.config import *

from detection.detection import Detection
from detection.preprocessing.preprocessing import process_features
from detection.preprocessing.preprocessing import process_labels


def load_data(data_file, categorical_feature_list, categories_list):
    df_X = pd.read_csv(data_file)
    df_X = process_features(df_X, categorical_feature_list, categories_list)
    df_X = df_X.astype(np.float64)
    return df_X


def load_labels(labels_file, labels, classes):
    df_y = pd.read_csv(labels_file)
    df_y = process_labels(df_y, labels, classes)
    return df_y

def process_labels(df_y, labels, classes):
    label_to_id = {labels[i] : classes[i] for i in range(len(labels))}
    values = np.ndarray.flatten(df_y.values)
    ids = []
    for val in values:
        ids.append(label_to_id[val])
    ids = pd.DataFrame(ids, columns=["class"])
    return ids


def overall_report(df_y, y_pred_dict):
    """
    :param df_y: DataFrame containing true classification
    :param y_pred_dict: Dictionary {index : class} where index is member of outlier_indices
    :return: Print overall classiifcation report
    """
    final_pred = np.zeros((df_y.shape[0]))
    for k, v in y_pred_dict.items():
        final_pred[k] = v

    print(classification_report(df_y, final_pred))


def outlier_report(df_y, outlier_indices):
    detected_attack = 0
    detected_normal = 0
    false_negtive = 0
    false_positive = 0
    count = 0
    max_count = len(outlier_indices)

    for i in range(df_y.shape[0]):
        label_num = df_y[i]

        if count < max_count and i == outlier_indices[count]:
            if label_num != 0:
                detected_attack += 1
            else:
                false_positive += 1
            count += 1
        else:
            if label_num != 0:
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
    print("Is Normal |  ", round(false_positive / total * 100, 4), "          ",
          round(detected_normal / total * 100, 4))
    print("")


def __log(message):
    print(message, end='')
    time.sleep(0.3)
    print(".", end='')
    time.sleep(0.3)
    print(".", end='')
    time.sleep(0.3)
    print(".", end='')
    time.sleep(0.3)

def classification_result(y, y_pred):
    assert len(y) == len(y_pred)
    correct = []
    wrong = []
    for i in range(len(y)):
        if y[i] == y_pred[i]:
            correct.append(i)
        else:
            wrong.append(i)
    return correct, wrong

def read_file(name):
    df = pd.read_csv(name, na_values="Infinity", dtype=dtypes)
    df = df.replace("Infinity", sys.maxsize)
    df = df.fillna(sys.maxsize)

    df_X = df.iloc[:, 0:-1].copy()
    df_X = df_X.apply(pd.to_numeric)

    df_y = df.iloc[:, -1].copy()
    df_y = process_labels(df_y, labels, classes)

    return df_X, df_y

if __name__ == '__main__':
    data_directoy = "../MachineLearningCVE/"
    filemon = "Monday-WorkingHours.pcap_ISCX.csv"
    filetue = "Tuesday-WorkingHours.pcap_ISCX.csv"
    filewed = "Wednesday-workingHours.pcap_ISCX.csv"
    filethr1 = "Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv"
    filethr2 = "Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv"
    filefri1 = "Friday-WorkingHours-Morning.pcap_ISCX.csv"
    filefri2 = "Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv"
    filefri3 = "Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"

    file_list = [filemon, filetue, filewed, filethr1, filethr2, filefri1, filefri2, filefri3]
    file_list = [data_directoy + x for x in file_list]


    print("Loading data...")
    df_X, df_y = read_file(file_list[0])
    print("Done")

    det = Detection(classes=classes , threshold_percentile=threshold_percentile, truth_size=truth_size,
                    truth_update_frac=truth_update_frac, truth_save_folder=truth_save_folder,
                    outlier_save_folder=outlier_save_folder, classifier_save_folder=classifier_save_folder)

    print("Initializing detectors...")
    i = 0
    size = df_X.shape[0]
    minsize = 50
    maxsize = 1000
    new_features = df_X.columns
    while i < size:
        print(str(i) + "/" + str(size))
        j = rd.randint(i + minsize, i + maxsize)
        j = min(j, size)
        X= pd.DataFrame(df_X[i:j].values, columns=new_features, dtype=np.float64)
        y= np.ndarray.flatten(pd.DataFrame(df_y[i:j].values, columns=['class'], dtype=np.int64).values)
        if i == 0:
            det.initialize(X, X, y)
            i = j
            continue
        det.update_outlier(X)
        det.update_classifier(X, y)
        i = j

    print("Done")
    breakpoints = {x : [] for x in file_list[1:]}

    for file in file_list[1:]:
        print("Loading data...")
        df_X, df_y = read_file(file)
        print("Done")
        print("Detecting file " + file)

        out_idx = []
        final_pred = []
        y_pred_list = []

        i = 0
        c = 0
        size = df_X.shape[0]
        while i < size:
            breakpoints[file].append(i)
            print(str(i) + "/" + str(size))
            j = rd.randint(i + minsize, i + maxsize)
            j = min(j, size)
            X = pd.DataFrame(df_X[i:j].values, columns=new_features, dtype=np.float64)
            y = pd.DataFrame(df_y[i:j].values, columns=['class'], dtype=np.int64)
            y_1d = np.ndarray.flatten(y.values)

            outlier_indices = det.detect_outliers(X)
            outlier_report(y_1d, outlier_indices)
            out_idx.extend([x + breakpoints[file][c] for x in outlier_indices])
            c += 1

            normal_indices = X.index.difference(outlier_indices)
            det.update_outlier(X.iloc[normal_indices])

            outlier_X = X.iloc[outlier_indices]
            outlier_y = y.iloc[outlier_indices]
            outlier_y_1d = y_1d[outlier_indices]

            y_pred = det.classfiy(outlier_X)
            print(classification_report(outlier_y_1d, y_pred, labels=classes))

            det.update_classifier(outlier_X, outlier_y)

            outcount = 0
            for k in range(X.shape[0]):
                if outlier_indices[min(outcount, len(outlier_indices) - 1)] == j:
                    final_pred.append(y_pred[outcount])
                    outcount += 1
                else:
                    final_pred.append(0)  # Class Normal
            y_pred_list.extend(y_pred)

            i = j
        print("FINAL REPORT OF FILE")
        print("======================================================================================")
        print(classification_report(df_y.iloc[out_idx].values, y_pred_list, labels=classes))
        print("======================================================================================")
        print(classification_report(df_y.values, final_pred, labels=classes))
        print("======================================================================================")
    exit()
    i = 0
    while i < s:
        breakpoints.append(i)
        j = rd.randint(i + minsize, i + maxsize)
        j = min(j, s)
        Xt_slice = pd.DataFrame(Xt[i:j].values, columns=new_features, dtype=np.float64)
        yt_slice = pd.DataFrame(yt_cls[i:j].values, columns=['class'], dtype=np.int64)
        list_Xt.append(Xt_slice)
        list_yt.append(yt_slice)
        i = j

    y_pred_list = []
    out_idx = []
    """
    normal_X = list_Xt[0].iloc[list_yt[0].loc[list_yt[0]['class'] == 0].index].copy()
    truth_size = min(truth_size, normal_X.shape[0])
    # Choose "truth_size" randomly sampled rows from all normal records
    truth = normal_X.sample(n=truth_size, random_state=None)

    det.update_outlier(truth)

    df_X = list_Xt[0].drop(truth.index)
    df_y = list_yt[0].drop(truth.index)

    det.update_classifier(df_X, df_y)
    """
    #cls_report = []
    #xaxis = []

    final_pred = []

    for i in range(len(list_Xt)):
        #xaxis.append(i)
        print("Step " + str(i))
        X = list_Xt[i]
        y = list_yt[i]
        y_cls = y

        outlier_indices = det.detect_outliers(X)
        outlier_report(y_cls.values, outlier_indices)

        out_idx.extend([x + breakpoints[i] for x in outlier_indices])

        normal_indices = X.index.difference(outlier_indices)
        det.update_outlier(X.iloc[normal_indices])

        outlier_X = X.iloc[outlier_indices]
        y_pred = det.classfiy(outlier_X)
        outlier_y = y_cls.iloc[outlier_indices]
        print("")
        #cls_report.append(classification_report(outlier_y.values, y_pred, output_dict=True, labels=classes))

        print(classification_report(outlier_y.values, y_pred, labels=classes))

        """

        correct_indices, wrong_indices = classification_result(outlier_y.values, y_pred)

        correct_X = outlier_X.iloc[correct_indices]
        wrong_X = outlier_X.iloc[wrong_indices]
        wrong_y = outlier_y.iloc[wrong_indices]

        update_X = outlier_X.append(wrong_X)
        update_y = outlier_y.append(wrong_y)
        """
        #det.update_classifier(update_X, update_y)
        #det.update_classifier(wrong_X, wrong_y)
        det.update_classifier(outlier_X, outlier_y)

        outcount = 0
        for j in range(list_Xt[i].shape[0]):
            if outlier_indices[min(outcount, len(outlier_indices) - 1)] == j:
                final_pred.append(y_pred[outcount])
                outcount += 1
            else:
                final_pred.append(0) # Class Normal

        y_pred_list.extend(y_pred)

        # inidx = X.index.difference(outidx)
        print("")
    """
    precision = [[] for i in range(len(classes))]
    recall = [[] for i in range(len(classes))]
    f1 = [[] for i in range(len(classes))]
    support = [[] for i in range(len(classes))]

    for report in cls_report:
        for i in classes:
            precision[i].append(report[str(i)]['precision'])
            recall[i].append(report[str(i)]['recall'])
            f1[i].append(report[str(i)]['f1-score'])
            support[i].append(report[str(i)]['support'])

    for i in classes:
        plt.plot(precision[i], c="r", label="Precision")
        plt.plot(recall[i], c="g", label="Recall")
        plt.plot(f1[i], c="b", label="F1")
        plt.legend()
        #plt.xticks(xaxis, support[i])
        plt.show()
    """
    print(classification_report(yt_cls, final_pred, labels=classes))
    print(classification_report(yt_cls.iloc[out_idx], y_pred_list, labels=classes))

    plt.plot([0,1,2])
    plt.show()

