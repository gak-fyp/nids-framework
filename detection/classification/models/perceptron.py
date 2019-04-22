from sklearn.linear_model import Perceptron
from joblib import dump, load
import os.path


class Neuron:
    __classes = []
    __savefile_per = ""
    __per = None

    def __init__(self, save_folder, classes):
        self.__classes = classes
        self.__savefile_per = save_folder + "per.joblib"
        self.__per = Perceptron()

    def train(self, X, y):
        self.__per.partial_fit(X, y, classes=self.__classes)
        self.__save_model()

    def predict(self, X):
        if self.__per is None:
            self.__load_model()
        return self.__per.predict(X)

    def update(self, X, y):
        self.train(X, y)
        # TODO: If no longer using train(), add save_model()

    def __save_model(self):
        dump(self.__per, self.__savefile_per)

    def __load_model(self):
        if os.path.exists(self.__savefile_per):
            self.__per = load(self.__savefile_per)
        else:
            print("ERROR: Perceptron not initialized. Run train() first.")