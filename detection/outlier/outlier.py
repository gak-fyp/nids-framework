from outlier.pca_outlier import PcaOutlier

class Outlier:
    __threshold_percentile = 0
    __ensemble = []

    def __init__(self, threshold_percentile):
        self.__threshold_percentile = threshold_percentile
        # Intialize Outlier Algorithms in Ensemble
        self.__set_ensemble()

    def train(self, truth):
        for model in self.__ensemble:
            model.train(truth, self.__threshold_percentile)

    def predict(self, X):
        y_list = []
        for model in self.__ensemble:
            y_list.append(model.predict(X))
        return self.__merge_pred(y_list)

    def __set_ensemble(self):
        # TODO: Add new models
        pca = PcaOutlier()
        self.__ensemble.append(pca)

    def __merge_pred(self, y_list):
        # TODO: Update Merging Function
        y_pred = y_list[0]
        return y_pred
