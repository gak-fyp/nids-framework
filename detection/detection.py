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

    def __init__(self, classes, threshold_percentile, truth_size, truth_update_frac, truth_save_folder,
                 outlier_save_folder, classifier_save_folder):
        """ Class constructor

        :param classes:
        :param threshold_percentile:
        :param truth_size:
        :param truth_update_frac:
        :param truth_save_folder:
        :param outlier_save_folder:
        :param classifier_save_folder:
        """

        self.__classes = classes
        self.__threshold_percentile = threshold_percentile
        self.__truth_size = truth_size
        self.__truth_update_frac = truth_update_frac

        self.__outlier = Outlier(threshold_percentile, outlier_save_folder)
        self.__truth = Truth(truth_size, truth_update_frac, truth_save_folder)
        self.__cls = Classification(self.__classes, classifier_save_folder)

    def initialize(self, normal_data, X, y):
        """

        :param normal_data:
        :param X:
        :param y:

        :return:
        """
        self.__truth.set_truth(normal_data)
        self.__outlier.train(self.__truth.get_truth())
        self.__cls.train(X, y)

    def detect_outliers(self, X):
        """

        :param X:

        :return:
        """
        outlier_indices = self.__outlier.predict(X)
        return outlier_indices

    def classfiy(self, X):
        """

        :param X:

        :return:
        """
        y_pred = self.__cls.predict(X)
        return y_pred

    def update_outlier(self, new_truth):
        """

        :param new_truth:

        :return:
        """
        if len(new_truth) > 0:
            self.__truth.update_truth(new_truth)
            self.__outlier.update(self.__truth.get_truth())

    def update_classifier(self, X, y):
        """

        :param X:
        :param y:

        :return:
        """
        self.__cls.update(X, y)