from classification.bayes import Bayes

class Classification:
    __classes = []
    __ensemble = []

    def __init__(self, classes):
        self.__classes = classes
        self.__set_ensemble()

    def train(self, X, y):
        for model in self.__ensemble:
            model.train(X, y, self.__classes)

    def predict(self, X):
        y_list = []
        for model in self.__ensemble:
            y_list.append(model.predict(X))
        return self.__merge_pred(y_list)

    def __set_ensemble(self):
        bae = Bayes()
        self.__ensemble.append(bae)

    def __merge_pred(self, y_list):
        # TODO: Update Merging Function
        y_pred = y_list[0]
        return y_pred
