import pandas as pd
import random as rd
truth_size = 20000

headers = ["duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes", "land", "wrong_fragment", "urgent",
            "hot", "num_failed_logins", "logged_in", "num_compromised", "root_shell", "su_attempted", "num_root",
            "num_file_creations", "num_shells", "num_access_files", "num_outbound_cmds", "is_hot_login",
            "is_guest_login", "count", "srv_count", "serror_rate", "srv_error_rate", "rerror_rate", "srv_rerror_rate",
            "same_srv_rate", "diff_srv_rate", "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count",
            "dst_host_same_srv_rate", "dst_host_diff_srv_rate", "dst_host_same_src_port_rate",
            "dst_host_srv_diff_host_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate", "dst_host_rerror_rate",
            "dst_host_srv_rerror_rate", "label", "difficulty_inverse"]

features = headers[:-2]
target = ["label"]


def create_files(filepath):
    global truth_size, headers, features, target

    df = pd.read_csv(filepath, header=None, names=headers)

    df_X = df[features]
    df_y = df[target]

    normal_X = df_X.iloc[df_y.loc[df_y[target[0]] == 'normal'].index]
    truth_size = min(truth_size, normal_X.shape[0])
    # Choose "truth_size" randomly sampled rows from all normal records
    truth = normal_X.sample(n=truth_size, random_state=None)

    truth.to_csv("./NSL-KDD/Batched/normal.csv", index=False)

    df_X = df_X.drop(truth.index)
    df_y = df_y.drop(truth.index)

    i = 0
    minsize = 500
    maxsize = 2000
    s = df_X.shape[0]
    while i < s:
        j = rd.randint(i + minsize, min())

    n = 200000  # chunk row size
    list_df = [df[i:i + n] for i in range(0, df.shape[0], n)]

    df_X.to_csv("./data.csv", index=False)
    df_y.to_csv("./labels.csv", index= False)

if __name__ == '__main__':
    data_directoy = "NSL-KDD/"
    train_file = data_directoy + "KDDTrain+"
    train_file_20_percent = data_directoy + "KDDTrain+_20Percent"
    test_file = data_directoy + "KDDTest+"

    create_files(train_file)



