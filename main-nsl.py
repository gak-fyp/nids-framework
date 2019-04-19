import pandas as pd
import numpy as np
from sklearn.metrics import classification_report
from sklearn.exceptions import UndefinedMetricWarning

import matplotlib.pyplot as plt

import random as rd
import time

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

if __name__ == '__main__':

    X = [[],[],[],[],[],[],[]]
    X[0] = [5.4, 99.8, 10.25,89, 95, 92,94, 97, 95]
    X[1] = [49.4, 94.6, 64.9,28 ,49, 36,43, 62, 51]
    X[2] = [2.3, 99.3, 4.5,	98, 70, 82,	99 ,84, 91]
    X[3] = [0.02, 97.2, 0.04,100 ,80, 89,100, 87, 93]
    X[4] = [1.8, 99.8, 3.54,95, 62, 75,	98, 79, 87]
    X[5] = [68.5, 98.2, 80.7,31, 12, 18,43, 29, 35]
    X[6] = [66, 99.9, 79.5,	34, 18 ,24,	43,29, 35]

    y = [[],[],[],[],[],[],[]]
    y[0] = [5.2,99.8,9.88,97,95,95,98,97,97]
    y[1] = [50.5,97.8,66.6, 96,72,81,96,79,86]
    y[2] = [2.4,99.3,4.69,98,72,83,99,85,92]
    y[3] = [0.02,97.2, 0.04, 100, 79, 88, 100,86,93]
    y[4] = [1.9,99.7,3.73, 98,42,58,99,70,81]
    y[5] = [70,99.2, 82.1,100,82,87 ,99,85,91]
    y[6] = [65.7,96.3,78.1, 100,79,87,97,81,88]

    b = [0.1938, 0.301, 0.07404, 0.1254, 0.083, 0.1245, 0.0981]

    for i in range(7):
        X[i] = [b[i] * x for x in X[i]]
        y[i] = [b[i] * x for x in y[i]]

    j = [0,0,0,0,0,0,0,0,0]
    j2 = [0,0,0,0,0,0,0,0,0]
    for k in range(9):
        for i in range(7):
            j[k] += X[i][k]
            j2[k] += y[i][k]
    print(j)
    print(j2)
    exit()
    data_directoy = "../NSL-KDD/"
    train_file = data_directoy + "KDDTrain+.csv"
    train_file_20_percent = data_directoy + "KDDTrain+_20Percent.csv"
    test_file = data_directoy + "KDDTest+.csv"

    normal_file = data_directoy + "20/normal.csv"
    data_file = data_directoy + "20/data.csv"
    labels_file = data_directoy + "20/labels.csv"

    det = Detection(classes=classes , threshold_percentile=threshold_percentile, truth_size=truth_size,
                    truth_update_frac=truth_update_frac, truth_save_folder=truth_save_folder,
                    outlier_save_folder=outlier_save_folder, classifier_save_folder=classifier_save_folder)
    """
    normal_data = load_data(normal_file, categorical_feature_list=categorical_feature_list, categories_list=categories_list)

    X = load_data(data_file, categorical_feature_list=categorical_feature_list, categories_list=categories_list)

    y = load_labels(labels_file, labels=labels, classes=classes)
    y_cls = y['class']
    """

    df = pd.read_csv(data_directoy + train_file, header=None, names=headers)
    df_X = df[features].copy()
    df_y = df[target].copy()

    df_X = process_features(df_X, categorical_feature_list, categories_list)
    df_X = df_X.astype(np.float64)
    df_y = process_labels(df_y, labels, classes)

    normal_X = df_X.iloc[df_y.loc[df_y[target[0]] == 'normal'].index]
    truth_size = min(truth_size, normal_X.shape[0])
    # Choose "truth_size" randomly sampled rows from all normal records
    truth = normal_X.sample(n=truth_size, random_state=None)

    df_X = df_X.drop(truth.index)
    df_y = df_y.drop(truth.index)
    y_cls = df_y['class']

    det.initialize(truth, df_X, y_cls)

    df_t = pd.read_csv(data_directoy + test_file, header=None, names=headers)
    Xt = df_t[features].copy()
    yt = df_t[target].copy()

    Xt = process_features(Xt, categorical_feature_list, categories_list)
    Xt = Xt.astype(np.float64)
    yt = process_labels(yt, labels, classes)
    yt_cls = yt['class']

    """
    #normal_X = Xt.iloc[yt.loc[yt['class'] == 0].index]
    #det.update_outlier(normal_X)
    #det.update_classifier(Xt, yt_cls)

    outlier_indices = det.detect_outliers(Xt)
    outlier_report(yt_cls.values, outlier_indices)

    normal_indices = Xt.index.difference(outlier_indices)
    #det.update_outlier(Xt.iloc[normal_indices])

    outlier_Xt = Xt.iloc[outlier_indices]
    y_pred = det.classfiy(outlier_Xt)
    outlier_yt = yt_cls.iloc[outlier_indices]

    print(classification_report(outlier_yt.values, y_pred, labels=classes))
    final_pred = []
    outcount = 0
    for j in range(Xt.shape[0]):
        if outlier_indices[min(outcount, len(outlier_indices) - 1)] == j:
            final_pred.append(y_pred[outcount])
            outcount += 1
        else:
            final_pred.append(0)  # Class Normal
    print(classification_report(yt_cls.values, final_pred, labels=classes))
    exit()
    """
    i = 0
    minsize = 50
    maxsize = 200
    s = Xt.shape[0]
    list_Xt = []
    list_yt = []
    new_features = Xt.columns.values

    breakpoints = []

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
        #outlier_report(y_cls.values, outlier_indices)

        out_idx.extend([x + breakpoints[i] for x in outlier_indices])

        normal_indices = X.index.difference(outlier_indices)
        det.update_outlier(X.iloc[normal_indices])

        outlier_X = X.iloc[outlier_indices]
        y_pred = det.classfiy(outlier_X)
        outlier_y = y_cls.iloc[outlier_indices]
        print("")
        #cls_report.append(classification_report(outlier_y.values, y_pred, output_dict=True, labels=classes))

        #print(classification_report(outlier_y.values, y_pred, labels=classes))


        correct_indices, wrong_indices = classification_result(outlier_y.values, y_pred)

        correct_X = outlier_X.iloc[correct_indices]
        wrong_X = outlier_X.iloc[wrong_indices]
        wrong_y = outlier_y.iloc[wrong_indices]

        update_X = outlier_X.append(wrong_X)
        update_y = outlier_y.append(wrong_y)

        det.update_classifier(update_X, update_y)
        #det.update_classifier(wrong_X, wrong_y)
        #det.update_classifier(outlier_X, outlier_y)

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

    print("==================================================================================")
    print("FINAL REPORT")

    outlier_report(yt_cls, out_idx)
    print(classification_report(yt_cls.iloc[out_idx], y_pred_list, labels=classes))
    print(classification_report(yt_cls, final_pred, labels=classes))

    plt.plot([0,1,2])
    plt.show()

