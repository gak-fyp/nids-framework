from detection.outlier.models.pca_outlier import PcaOutlier


class Outlier:
    __threshold_percentile = 0
    __save_folder = ""
    __ensemble = []

    def __init__(self, threshold_percentile, save_folder):
        self.__threshold_percentile = threshold_percentile
        self.__save_folder = save_folder
        # Intialize Outlier Algorithms in Ensemble
        self.__set_ensemble()

    def train(self, truth):
        for model in self.__ensemble:
            model.train(truth)

    def predict(self, X):
        y_list = []
        for model in self.__ensemble:
            y_list.append(model.predict(X))
        y_pred = self.__merge_pred(y_list)
        return y_pred

    def update(self, new_truth):
        for model in self.__ensemble:
            model.update(new_truth)

    def __set_ensemble(self):
        # TODO: Add new models
        pca = PcaOutlier(self.__threshold_percentile, self.__save_folder)
        self.__ensemble.append(pca)

    def __merge_pred(self, y_list):
        # TODO: Update Merging Function
        y_pred = y_list[0]
        return y_pred
