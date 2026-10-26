import pandas

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, OrdinalEncoder

from utility import read_content_from_json_file


class DataProcessor:
    def __init__(self):
        self.raw_dataframe = pandas.DataFrame()
        self.features = []
        
        # "passthrough" is included to avoid encoding numerical values.
        self.transformer = ColumnTransformer(
                transformers=[
                    (
                        "ordinal",
                        OrdinalEncoder(categories=self.get_ordinal_values()[0]),
                        self.get_ordinal_values()[1],
                    ),
                    (
                        "nominal",
                        OneHotEncoder(
                            sparse_output=False,
                        ),
                        self.get_nominal_vales(),
                    ),
                ],
                remainder="passthrough", 
                ).set_output(transform="pandas")
            
        
        self.min_max_scaler = MinMaxScaler()

    def get_ordinal_values(self) -> list[str]:
        json_data = read_content_from_json_file("categorical_feature_definitions")
    
        categories = json_data["ordinalValues"][0]["categories"]
        features = json_data["ordinalValues"][1]["features"]
        ordinal_values = [categories, features]
        
        return ordinal_values

    def get_nominal_vales(self) -> list[str]:
        json_data = read_content_from_json_file("categorical_feature_definitions")
        nominal_values = json_data["nominalValues"]
        
        return nominal_values

    def fit_transform(self, raw_features):
        self.features = raw_features.columns.tolist()
        processed_features = raw_features

        # This will fail if no numerical features are found, however, this means that this operation is not appropriate.
        # Thus, will the variable contain the raw features, and the exception being passed.
        try:
            processed_features = self.transformer.fit_transform(raw_features)
        except ValueError as value_error:
            pass
        
        return pandas.DataFrame(
            self.min_max_scaler.fit_transform(processed_features),
            columns=processed_features.columns,
            index=raw_features.index,
        )

    def get_transformed_normalized_and_encoded_dataframe(self, raw_dataframe):
        features = raw_dataframe[self.features]
        encoded_features = self.transformer.transform(features)

        return pandas.DataFrame(
            self.min_max_scaler.transform(encoded_features)
        )

    def get_fitted_normalized_and_encoded_dataframe(self):
        target_name = self.get_last_column_of_dataframe(self.raw_dataframe)

        features = self.raw_dataframe.drop(columns=[target_name])
        target = self.raw_dataframe[[target_name]]

        return pandas.concat(
            [self.fit_transform(features), target],
            axis=1,
        )

    def get_last_column_as_a_separate_dataframe(self, dataframe: pandas.DataFrame):
        return dataframe[self.get_last_column_of_dataframe(dataframe)]

    def get_last_column_of_dataframe(self, dataframe: pandas.DataFrame):
        """
        This can be used to get the classes, if these are contained in the last column.
        """
        return dataframe.columns[-1]