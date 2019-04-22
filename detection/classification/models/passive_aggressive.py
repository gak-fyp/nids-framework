from sklearn.linear_model import PassiveAggressiveClassifier
from joblib import dump, load
import os.path


class PassiveAggressive:
    __classes = []
    __savefile_pas = ""
    __pas = None

    def __init__(self, save_folder, classes):
        """

        :param save_folder:
        :param classes:
        """

        self.__classes = classes
        self.__savefile_pas = save_folder + "pas.joblib"
        self.__pas = PassiveAggressiveClassifier()

    def train(self, X, y):
        """

        :param X:
        :param y:

        :return:
        """
        self.__pas.partial_fit(X, y, classes=self.__classes)
        self.__save_model()

    def predict(self, X):
        """

        :param X:

        :return:
        """
        if self.__pas is None:
            self.__load_model()
        return self.__pas.predict(X)

    def update(self, X, y):
        """

        :param X:
        :param y:

        :return:
        """
        self.train(X, y)
        # If no longer using train(), add save_model()

    def __save_model(self):
        """

        """
        dump(self.__pas, self.__savefile_pas)

    def __load_model(self):
        """

        """
        if os.path.exists(self.__savefile_pas):
            self.__pas = load(self.__savefile_pas)
        else:
            print("ERROR: PassiveAggressive not initialized. Run train() first.")