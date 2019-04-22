from sklearn.linear_model import SGDClassifier
from joblib import dump, load
import os.path


class SGD:
    __classes = []
    __savefile_sgd = ""
    __sgd = None

    def __init__(self, save_folder, classes):
        self.__classes = classes
        self.__savefile_sgd = save_folder + "sgd.joblib"
        self.__sgd = SGDClassifier()

    def train(self, X, y):
        self.__sgd.partial_fit(X, y, classes=self.__classes)
        self.__save_model()

    def predict(self, X):
        if self.__sgd is None:
            self.__load_model()
        return self.__sgd.predict(X)

    def update(self, X, y):
        self.train(X, y)
        # TODO: If no longer using train(), add save_model()

    def __save_model(self):
        dump(self.__sgd, self.__savefile_sgd)

    def __load_model(self):
        if os.path.exists(self.__savefile_sgd):
            self.__sgd = load(self.__savefile_sgd)
        else:
            print("ERROR: SGD not initialized. Run train() first.")