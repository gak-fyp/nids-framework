import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder


def process_features(df_x, header_list, categories_list):
    """Convert categorical features to one hot vectors and add to DataFrame

    :param df_x: DataFrame containing categorical features, shape (n_samples, n_features)
    :param header_list: array of headers of columns containing categorical data, shape (n_categorical_features, )
    :param categories_list: array of list of all possible categories in each column,
                            shape (n_categorical_features, n_categories_per_feature) -> inconsitent shape
    :return: DataFrame containing new one-hot columns and all previous non-categorical columns
    """
    assert len(header_list) == np.shape(categories_list)[0]

    for i in range(len(header_list)):
        # Convert one columns to one-hot vectors
        one_hots = __categorical_to_one_hot(df_x[header_list[i]], categories_list[i])
        # Generate header names for new columns
        new_headers = [header_list[i] + "_" + s for s in categories_list[i]]
        # Add new columns to DataFrame
        df_x[new_headers] = one_hots
    # Delete old categorical columns
    new_df_X = df_x.drop(columns=header_list)
    return new_df_X


def __categorical_to_one_hot(df, categories):
    # Input: column of a DataFrame with categorical data, Array of categorical values
    # Output: New DataFrame containing one column for each category in one-hot notation
    assert np.array(categories).ndim == 1
    categories = [categories]

    val = np.reshape(df.values, (-1, 1))

    encoder = OneHotEncoder(categories=categories, sparse=False, dtype=np.int64)
    res = encoder.fit_transform(val)
    headers = encoder.categories_[0]

    return pd.DataFrame(res, columns=headers)

def process_labels(df_y, labels, classes):
    label_to_id = {labels[i] : classes[i] for i in range(len(labels))}
    values = np.ndarray.flatten(df_y.values)
    ids = []
    for val in values:
        ids.append(label_to_id[val])
    df_y['class'] = ids
    return df_y
