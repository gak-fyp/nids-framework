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

    i = 0
    minsize = 5000000
    maxsize = 20000000
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

