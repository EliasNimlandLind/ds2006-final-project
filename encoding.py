from sklearn.preprocessing import MinMaxScaler
import pandas as pandas

def normalize_dataframe_containing_features(dataframe_to_normalize):
    # Creating an instance of the sklearn.preprocessing.MinMaxScaler()
    min_max_scaler = MinMaxScaler()

    # Scaling the Price column of the created dataFrame and storing
    # the result in ScaledPrice Column
    normalized_dataframe = pandas.DataFrame()

    for current_feature in list(dataframe_to_normalize):
        normalized_dataframe[[current_feature]] = min_max_scaler.fit_transform(dataframe_to_normalize[[current_feature]])

    return normalized_dataframe