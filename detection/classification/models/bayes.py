from sklearn.naive_bayes import GaussianNB
from joblib import dump, load
import os.path


class Bayes:
    __classes = []
    __savefile_bae = ""
    __bae = None

    def __init__(self, save_folder, classes):
        """

        :param save_folder:
        :param classes:
        """

        self.__classes = classes
        self.__savefile_bae = save_folder + "bayes.joblib"
        self.__bae = GaussianNB()

    def train(self, X, y):
        """

        :param X:
        :param y:

        :return:
        """
        self.__bae.partial_fit(X, y, classes=self.__classes)
        self.__save_model()

    def predict(self, X):
        """

        :param X:

        :return:
        """
        if self.__bae is None:
            self.__load_model()
        return self.__bae.predict(X)

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
        dump(self.__bae, self.__savefile_bae)

    def __load_model(self):
        """

        """
        if os.path.exists(self.__savefile_bae):
            self.__bae = load(self.__savefile_bae)
        else:
            print("ERROR: Bayes not initialized. Run train() first.")