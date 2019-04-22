import numpy as np
from joblib import dump, load
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import MiniBatchKMeans

import os.path

class KMeans:
    __km = None
    __scale = None
    __ev = []
    __threshold = 0
    __threshold_percentile = 0.0

    __savefile_km = ""
    __savefile_scale = ""
    __savefile_threshold = ""
    __savefile_ev = ""

    def __init__(self, threshold_percentile, save_folder):
        """

        :param threshold_percentile:
        :param save_folder:

        """
        self.__threshold_percentile = threshold_percentile
        self.__savefile_km = save_folder + "km.joblib"
        self.__savefile_scale = save_folder + "km_scale.joblib"
        self.__savefile_threshold = save_folder + "threshold.joblib"
        self.__savefile_ev = save_folder + "ev.joblib"

        self.__km = MiniBatchKMeans(n_clusters=1)
        self.__scale = StandardScaler()

    def train(self, truth):
        """

        :param truth:

        :return:
        """
        self.__scale.fit(truth)
        std_truth = self.__standardize(truth)
        self.__km.fit(std_truth)
        self.__set_threshold(std_truth, self.__threshold_percentile)
        self.__save_model()

    def predict(self, X):
        """

        :param X:

        :return:
        """
        if self.__km is None:
            self.__load_model()
        std_X = self.__standardize(X)
        score = self.__calculate_score(std_X)
        outlier_indices = []
        for i in range(len(score)):
            if score[i] >= self.__threshold:
                outlier_indices.append(i)
        return np.array(outlier_indices)

    def update(self, new_truth):
        """

        :param new_truth:

        :return:
        """
        self.train(new_truth)
        # If no longer using train(), add save_model()

    def __standardize(self, X):
        """

        :param X:

        :return:
        """
        return self.__scale.transform(X)

    def __set_threshold(self, truth, threshold_percentile):
        """

        :param truth:
        :param threshold_percentile:

        :return:
        """
        score = self.__calculate_score(truth)
        # Threshold is the "threshold_percentile" percentile of score
        self.__threshold = np.percentile(score, threshold_percentile)

    def __calculate_score(self, X):
        """

        :param X:

        :return:
        """
        score = []
        for i in range(X.shape[0]):
            s = np.linalg.norm(X[i] - self.__km.cluster_centers_[0])
            score.append(s)
        return score

    def __save_model(self):
        """

        """
        dump(self.__km, self.__savefile_km)
        dump(self.__scale, self.__savefile_scale)
        dump(self.__threshold, self.__savefile_threshold)
        dump(self.__ev, self.__savefile_ev)

    def __load_model(self):
        """

        """
        if os.path.exists(self.__savefile_km) and os.path.exists(self.__savefile_scale) and\
            os.path.exists(self.__savefile_threshold) and os.path.exists(self.__savefile_ev):
            self.__km = load(self.__savefile_km)
            self.__scale = load(self.__savefile_scale)
            self.__threshold = load(self.__savefile_threshold)
            self.__ev = load(self.__savefile_ev)
        else:
            print("ERROR: KMeans not initialized. Run train() first.")