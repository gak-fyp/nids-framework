from detection.classification.models.bayes import Bayes


class Classification:
    __save_folder  = ""
    __classes = []
    __ensemble = []

    def __init__(self, classes, save_folder):
        self.__classes = classes
        self.__save_folder = save_folder
        self.__set_ensemble()

    def train(self, X, y):
        for model in self.__ensemble:
            model.train(X, y)

    def predict(self, X):
        y_list = []
        for model in self.__ensemble:
            y_list.append(model.predict(X))
        return self.__merge_pred(y_list)

    def update(self, X, y):
        for model in self.__ensemble:
            model.update(X, y)

    def __set_ensemble(self):
        # TODO: Add new Models
        bae = Bayes(self.__save_folder, self.__classes)
        self.__ensemble.append(bae)

    def __merge_pred(self, y_list):
        # TODO: Update Merging Function after adding new models
        y_pred = y_list[0]
        return y_pred
