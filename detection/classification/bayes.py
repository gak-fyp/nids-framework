from sklearn.naive_bayes import MultinomialNB


class Bayes:
    __bae = None

    def __init__(self):
        self.__bae = MultinomialNB()

    def train(self, X, y, classes):
        self.__bae.partial_fit(X, y, classes=classes)

    def predict(self, X):
        return self.__bae.predict(X)
