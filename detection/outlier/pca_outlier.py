import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


class PcaOutlier:
    __pca = None
    __scale = None
    __ev = []
    __threshold = 0

    def __init__(self):
        self.__pca = PCA()
        self.__scale = StandardScaler()

    def train(self, truth, threshold_percentile):
        self.__scale.fit(truth)
        std_truth = self.__standardize(truth)
        self.__pca.fit(std_truth)
        self.__set_ev()
        self.__set_threshold(std_truth, threshold_percentile)

    def predict(self, X):
        std_X = self.__standardize(X)
        score = self.__calculate_score(std_X)
        outlier_indices = []
        for i in range(len(score)):
            if score[i] >= self.__threshold:
                outlier_indices.append(i)
        return np.array(outlier_indices)

    def __standardize(self, X):
        return self.__scale.transform(X)

    def __set_ev(self):
        variance_ratio = self.__pca.explained_variance_ratio_
        total_ratio = np.sum(variance_ratio)
        self.__ev = [np.sum(variance_ratio[0:j+1]) / total_ratio for j in range(len(variance_ratio))]

    def __set_threshold(self, truth, threshold_percentile):
        score = self.__calculate_score(truth)
        # Threshold is the "threshold_percentile" percentile of score
        self.__threshold = np.percentile(score, threshold_percentile)

    def __calculate_score(self, X):
        score = np.zeros((X.shape[0],))
        p = 0
        for e in self.__ev:
            p += 1
            if e > 0.5:
                break
        W = self.__pca.components_.T[:, 0:p]
        m = self.__pca.mean_
        for j in range(W.shape[1]):
            # Applying PCA Projection using top j eigenvectors to produce Y from X
            weight = W[:, 0:j+1]
            Y = np.dot(X - m, weight)
            # Apply reverse transformation to reproduce X from Y
            R = np.dot(Y, np.transpose(weight)) + m
            # Score = Weighted difference between original X and reproduced X
            for i in range(X.shape[0]):
                score[i] += np.sum(np.abs(X[i] - R[i])) * self.__ev[j]

            print ("Step "+ str(j + 1) + " of " + str(W.shape[1]) + "...", end='\r')
        print("")
        print("DONE")
        return score
