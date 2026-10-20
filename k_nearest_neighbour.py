import os

import numpy
import pandas
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score, classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
import matplotlib.pyplot as mathplotlib

from data_frame import handle_data_frame_menu
from data_partitioning_configuration import data_partitioning_strategy_names
from data_preprocessing import DataProcessor
from utility import get_last_column_as_a_separate_dataframe, get_last_column_of_dataframe

class K_nearest_neighbour_conductor():
    def __init__(self, k_value, dataframe, normalized_and_encoded_dataframe, data_partitioning_configuration):
        self.k_value = k_value
        self.dataframe = dataframe
        self.normalized_and_encoded_dataframe = normalized_and_encoded_dataframe
        self.data_partitioning_strategy = data_partitioning_configuration
        
    def get_k_value_text(self):
        return f"k = {self.k_value}"

    def __str__(self):
        model_statistics = ""
        
        if (self.data_partitioning_strategy['data_partitioning_strategy_name'] == data_partitioning_strategy_names.TRAIN_TEST_SPLIT.value):
                # Obtains the predictions from the kNN classifier:
                model_statistics = (f"\n{self.get_k_value_text()}\n"
                                        f"Accuracy: {accuracy_score(self.classes_test, self.predictions)}\n\n"
                                        f"  {classification_report(self.classes_test, self.predictions)}\n\n"
                                        )
        else:
            score_types = ["accuracy", 
                            "average_precision", 
                            "recall_micro", 
                            "f1_micro"]
            
            model_statistics = f"\n{self.get_k_value_text()}"
            for current_score_type in score_types:
                scores = ""
                cv = None
                if self.data_partitioning_strategy["is_stratified"] == False:
                    cv = self.data_partitioning_strategy['number_of_folds']
                else:
                    cv = StratifiedKFold(n_splits=self.data_partitioning_strategy['number_of_folds'])

                scores = cross_val_score(self.k_neighbours_classifier, X=self.features, y=self.classes, cv=cv, scoring=current_score_type)
        
                model_statistics += f"\n{current_score_type}:\n    {scores}\n    Mean: {scores.mean()}\n\n"
    
        return model_statistics

    def display_confusion_matrix(self):
        try:
            confusion_matrix_display = ConfusionMatrixDisplay.from_estimator(
                self.k_neighbours_classifier,
                self.features_test,
                self.classes_test,
                cmap=mathplotlib.cm.Blues,
                normalize="true"
            )
            confusion_matrix_display.ax_.set_title("Confusion matrix")
            mathplotlib.show()

        except Exception as exception:
            print(exception)
        
    def execute_experiment(self):        
        features = self.normalized_and_encoded_dataframe.drop(get_last_column_of_dataframe(self.normalized_and_encoded_dataframe), axis=1)
        # Creates a dataframe from solely the data in the last column.
        classes = get_last_column_as_a_separate_dataframe(self.dataframe)
        
        if (self.data_partitioning_strategy['is_stratified'] == True):
            which_part_base_stratification_on = classes

        # Split the data into train/test sets 
        features_train, features_test, classes_train, classes_test = train_test_split(
        features, classes, test_size=self.data_partitioning_strategy['testing_percentage'], random_state=10, stratify=which_part_base_stratification_on
        )   

        self.features_test = features_test

        self.classes = classes
        self.classes_test = classes_test
        
        # Creates a Knn Classifier Object.
        self.k_neighbours_classifier = KNeighborsClassifier(n_neighbors=self.k_value)
        # Trains this Knn Classifier with the training set obtained previously:
        self.k_neighbours_classifier.fit(features_train, classes_train)
        self.predictions = self.k_neighbours_classifier.predict(features_test)

def handle_nearest_neighbour_conductor_menu(dataframe, normalized_and_encoded_dataframe, data_partitioning_configuration):
    k_nearest_neighbour_conductors = []

    has_menu_been_exited = False
    while has_menu_been_exited == False:
        input_number_of_experiments_using_k_nearest_neighbours = 0

        try:
            input_number_of_experiments_using_k_nearest_neighbours = int(input("Enter the number of experiments to conduct using k nearest neighbour: "))
        except:
            print("\nThe number of experiments to conduct must be an integer.\n")

        if (input_number_of_experiments_using_k_nearest_neighbours > 0):
            for current_k_nearest_neighbour_conductor_index in range(input_number_of_experiments_using_k_nearest_neighbours):
                is_current_k_value_valid = False
                while is_current_k_value_valid == False:
                    try:
                        current_k_value = int(input(f"Enter the k value for experiment number {current_k_nearest_neighbour_conductor_index + 1}: "))
                    except:
                        print("\nThe current k value must be an integer.\n")

                    if (current_k_value > 0):
                        current_k_nearest_neighbour_conductor = K_nearest_neighbour_conductor(current_k_value, dataframe, normalized_and_encoded_dataframe, data_partitioning_configuration)
                        k_nearest_neighbour_conductors.append(current_k_nearest_neighbour_conductor)
                        is_current_k_value_valid = True
                    else:
                        print("\nThe k value must be greater than 0.\n")

            has_menu_been_exited = True

        else: 
            print("\nThe number of experiments to conduct must be greater than 0.\n")
            
    return k_nearest_neighbour_conductors


def handle_classify_unforeseen_sample_menu(k_nearest_neighbour_conductors, data_processor):
    if not k_nearest_neighbour_conductors:
        return print("\nResults from experiments are required to classify unforeseen samples.\n")

    k_neighbours_classifier = ""
    input_features  = []

    try:
        has_menu_been_exited = False
        while has_menu_been_exited == False:
            classify_unforeseen_sample_classifier_menu_text = "\n"

            for current_index, current_k_nearest_neighbour_conductor in k_nearest_neighbour_conductors.items():
                classify_unforeseen_sample_classifier_menu_text += f"{current_index}. {current_k_nearest_neighbour_conductor.get_k_value_text()}\n"
            classify_unforeseen_sample_classifier_menu_text += "Select a model to use to classify the sample by typing the corresponding number: "
            
            classify_unforeseen_sample_k_neighbours_classifier_input = 0
            try:
                classify_unforeseen_sample_k_neighbours_classifier_input = int(input(classify_unforeseen_sample_classifier_menu_text))
            except:
                print("\nThe number representing a model must be an integer.\n")

            if (0 < classify_unforeseen_sample_k_neighbours_classifier_input <= len(k_nearest_neighbour_conductors)):
                k_neighbours_classifier = k_nearest_neighbour_conductors[classify_unforeseen_sample_k_neighbours_classifier_input].k_neighbours_classifier
                has_menu_been_exited = True
            else:
                print("\nEnter a valid integer.\n")

        has_menu_been_exited = False
        while has_menu_been_exited == False:
            classify_unforeseen_sample_input_features_menu_text = "1. Load input features from a file\n2. Manually input all input features.\nSelect an option by typing the corresponding number: "

            try:
                classify_unforeseen_sample_input_features_input = int(input(classify_unforeseen_sample_input_features_menu_text))
            except:
                print("\nThe number representing an option must be an integer.\n")
            
            raw_dataframe_loaded_from_file = pandas.read_csv("datasets/unforeseen/unforeseen_sample.csv")

            match classify_unforeseen_sample_input_features_input:
                case 1:
                    input_features = data_processor.get_transformed_normalized_and_encoded_dataframe(raw_dataframe_loaded_from_file)
                case 2:
                    intermediate_values = {}
                
                    """ for label, values in raw_dataframe_loaded_from_file.head(2).items():
                        intermediate_raw_dataframe_loaded_from_file[label] = input(f"Enter value for {label}: ") """

                    for label, values in raw_dataframe_loaded_from_file.head(2).items():
                        intermediate_values[label] = input(f"Enter value for {label}: ") 

                    """
                    Male
                    22
                    1.78
                    89.8
                    no
                    no
                    2
                    1
                    Sometimes
                    no
                    2
                    no
                    0
                    0
                    Sometimes
                    Public_Transportation
                    """
                    raw_dataframe_loaded_from_intermediate_values = pandas.DataFrame(intermediate_values, index=[0])
                    input_features = data_processor.get_transformed_normalized_and_encoded_dataframe(raw_dataframe_loaded_from_intermediate_values)
                case _:
                    print("Invalid option.")

            prediction = k_neighbours_classifier.predict(input_features)
            print(f"\nThe unforeseen sample was predicted to be: {prediction}\n")
            has_menu_been_exited = True

    except Exception as exception:
        print(f"\n{exception}\n")