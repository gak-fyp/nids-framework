import pandas as pd
import os.path


class Truth:
    __truth = pd.DataFrame()
    __truth_size = 0
    __truth_update_frac = 0
    __save_folder = ""

    def __init__(self, truth_size, truth_update_frac, save_folder):
        """

        :param truth_size:
        :param truth_update_frac:
        :param save_folder:

        """
        self.__truth_size = truth_size
        self.__truth_update_frac = truth_update_frac
        self.__save_folder = save_folder

    def set_truth(self, normal_X):
        """

        :param normal_X:

        :return:
        """
        truth_size = min(self.__truth_size, normal_X.shape[0])
        # Choose "truth_size" randomly sampled rows from all normal records
        self.__truth = normal_X.sample(n=truth_size, random_state=None)
        self.__save_truth()

    def update_truth(self, new_X):
        """

        :param new_X:

        :return:
        """
        self.__load_truth()
        num_missing = self.__truth_size - self.__truth.shape[0]
        new_size = min(max(int(self.__truth_update_frac * self.__truth_size), num_missing), new_X.shape[0])
        new_X = new_X.sample(n=new_size, random_state=None)

        replace_size = max(0, new_size - num_missing)
        if replace_size > 0:
            replace = self.__truth.sample(n=replace_size, random_state=None)
            self.__truth.drop(index=replace.index, inplace=True)
        self.__truth = self.__truth.append(new_X)
        self.__save_truth()

    def get_truth(self):
        """

        """
        self.__load_truth()
        return self.__truth

    def __save_truth(self):
        """

        """
        self.__truth.to_pickle(self.__save_folder + "truth.pkl")

    def __load_truth(self):
        """

        """
        if self.__truth.empty:
            if os.path.exists(self.__save_folder):
                self.__truth = pd.read_pickle(self.__save_folder + "truth.pkl")
            else:
                print("ERROR: Truth not set. Empty DataFrame returned. Run set_truth() first.")