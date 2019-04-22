from detection.classification.models.bayes import Bayes
from detection.classification.models.sgd import SGD
from detection.classification.models.perceptron import Neuron
from detection.classification.models.passive_aggressive import PassiveAggressive

import numpy as np

class Classification:
    __save_folder  = ""
    __classes = []
    __ensemble = []
    __weights = []

    def __init__(self, classes, save_folder):
        """

        :param classes:
        :param save_folder:
        """

        self.__classes = classes
        self.__save_folder = save_folder
        self.__set_ensemble()
        self.__weights = [2, 1, 3]

    def train(self, X, y):
        """

        :param X:
        :param y:

        :return:
        """
        for model in self.__ensemble:
            model.train(X, y)

    def predict(self, X):
        """

        :param X:

        :return:
        """
        y_list = []
        for model in self.__ensemble:
            y_list.append(model.predict(X))
        return self.__merge_pred(np.asarray(y_list))

    def update(self, X, y):
        """

        :param X:
        :param y:

        :return:
        """
        for model in self.__ensemble:
            model.update(X, y)

    def __set_ensemble(self):
        """

        """
        bae = Bayes(self.__save_folder, self.__classes)
        sgd = SGD(self.__save_folder, self.__classes)
        pas = PassiveAggressive(self.__save_folder, self.__classes)
        self.__ensemble.append(bae)
        self.__ensemble.append(sgd)
        self.__ensemble.append(pas)

    def __merge_pred(self, y_list):
        """ Merge prediction by Weighted Majority Voting. If no majority, the smallest numbered class is chosen.

        :param y_list:

        :return:
        """
        y_pred = []
        for i in range(len(y_list[0])):
            pred_1y = []
            for j in range(len(self.__ensemble)):
                for k in range(self.__weights[j]):
                    pred_1y.append(y_list[j][i])
            count = np.bincount(pred_1y)
            argmax = np.argmax(count)
            y_pred.append(argmax)
        return y_pred