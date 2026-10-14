from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder

import pandas
import numpy

def normalize_dataframe_containing_features(dataframe_to_normalize):
    """
    This ensures the distances calculated by the model are contributing equally, regardless of units.
    """
    # Creating an object of MinMaxScaler.
    min_max_scaler = MinMaxScaler()

    normalized_dataframe = pandas.DataFrame()
    for current_feature_to_normalize in dataframe_to_normalize:
        normalized_dataframe[[current_feature_to_normalize]] = min_max_scaler.fit_transform(dataframe_to_normalize[[current_feature_to_normalize]])
    
    return normalized_dataframe

def encode_categorical_features(dataframe_to_encode):
    ordinal_categories = [["no", "Sometimes", "Frequently", "Always"],["no", "Sometimes", "Frequently", "Always"]]
    ordinal_features = ['CAEC', 'CALC']

    nominal_features = ['Gender', 'family_history_with_overweight','SMOKE', 'FAVC', 'SCC', 'MTRANS']

    categorical_transformer = ColumnTransformer(transformers=[('ordinal',OrdinalEncoder(categories=ordinal_categories), ordinal_features),
                                                              ('nominal',OneHotEncoder(sparse_output=False),nominal_features)]) # sparse_output = False ensures the result will be in the correct format.
    categorical_transformer.set_output(transform="pandas")

    encoded_dataframe = categorical_transformer.fit_transform(dataframe_to_encode)

    return encoded_dataframe   


def get_normalized_and_encoded_dataframe(dataframe):
    """
    Separate data based on type to perform type specific operations, e.g. normalisation and ordinal encoding.

    Returns: A dataframe containing the normalized data in addition to the encoded data.
    """
    raw_numerical_sub_dataframe = dataframe.select_dtypes(include=[numpy.number])
    normalized_sub_dataframe = normalize_dataframe_containing_features(raw_numerical_sub_dataframe)
        
    raw_categorical_sub_dataframe = dataframe.select_dtypes(exclude=[numpy.number])
    encoded_categorical_sub_dataframe = encode_categorical_features(raw_categorical_sub_dataframe)
    
    normalized_and_encoded_dataframe = pandas.concat([normalized_sub_dataframe, encoded_categorical_sub_dataframe], axis=1)
    return normalized_and_encoded_dataframe
