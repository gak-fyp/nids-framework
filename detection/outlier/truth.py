class Truth:
    __truth = []
    __truth_size = 0
    __truth_update_frac = 0

    def __init__(self, truth_size, truth_update_frac):
        self.__truth_size = truth_size
        self.__truth_update_frac = truth_update_frac

    def set_truth(self, normal_X):
        num_normal = normal_X.shape[0]
        truth_size = min(self.__truth_size, num_normal)
        # Choose "truth_size" randomly sampled rows from all normal records
        self.__truth = normal_X.sample(n=truth_size, random_state=None)

    def update_truth(self, normal):
        # TODO: Complete Update Truth Function
        pass

    def get_truth(self):
        return self.__truth
