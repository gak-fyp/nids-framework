from detection.outlier.models.pca_outlier import PcaOutlier
from detection.outlier.models.kmeans import KMeans


class Outlier:
    __threshold_percentile = 0
    __save_folder = ""
    __ensemble = []

    def __init__(self, threshold_percentile, save_folder):
        """

        :param threshold_percentile:
        :param save_folder:

        """
        self.__threshold_percentile = threshold_percentile
        self.__save_folder = save_folder
        self.__set_ensemble()

    def train(self, truth):
        """

        :param truth:

        :return:
        """
        for model in self.__ensemble:
            model.train(truth)

    def predict(self, X):
        """

        :param X:

        :return:
        """
        y_list = []
        for model in self.__ensemble:
            y_list.append(model.predict(X))
        y_pred = self.__merge_pred(y_list)
        return y_pred

    def update(self, new_truth):
        """

        :param new_truth:

        :return:
        """
        for model in self.__ensemble:
            model.update(new_truth)

    def __set_ensemble(self):
        """
        Intialize Outlier Algorithms in Ensemble
        """
        pca = PcaOutlier(self.__threshold_percentile, self.__save_folder)
        km = KMeans(self.__threshold_percentile, self.__save_folder)
        self.__ensemble.append(pca)
        self.__ensemble.append(km)

    def __merge_pred(self, y_list):
        """

        :param y_list:

        :return:
        """
        y_pred = set(y_list[0])
        for y in y_list:
            y_pred = y_pred.union(y)
        return list(y_pred)
