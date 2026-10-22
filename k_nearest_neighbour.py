from enum import IntEnum

import pandas
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
import matplotlib.pyplot as mathplotlib

from data_partitioning_configuration import data_partitioning_strategy_names

from data_preprocessing import DataProcessor
from utility import validate_user_input_integer

class K_nearest_neighbour_conductor():
    def __init__(self, k_value, dataframe, normalized_and_encoded_dataframe, data_partitioning_configuration):
        self.k_value = k_value
        self.dataframe = dataframe
        self.normalized_and_encoded_dataframe = normalized_and_encoded_dataframe
        self.data_partitioning_strategy = data_partitioning_configuration
        
    def get_k_value_text(self):
        return f"k = {self.k_value}"

    def __str__(self):
        try:
            model_statistics = ""
            
            if (self.data_partitioning_strategy['data_partitioning_strategy_name'] == data_partitioning_strategy_names.TRAIN_TEST_SPLIT):
                    # Obtains the predictions from the kNN classifier:
                    model_statistics = (f"{self.get_k_value_text()}\n"
                                            f"Accuracy: {accuracy_score(self.classes_test, self.predictions)}\n\n"
                                            f"  {classification_report(self.classes_test, self.predictions)}\n\n"
                                            )
            else:
                number_of_folds = self.data_partitioning_strategy['number_of_folds']
                if number_of_folds <= 0:
                    raise ValueError("The number of folds must be greater than 0.")
                
                score_types = ["accuracy", 
                                "average_precision", 
                                "recall_micro", 
                                "f1_micro"]
                
                model_statistics = f"\n{self.get_k_value_text()}"
                for current_score_type in score_types:
                    scores = ""
                    cv = None
                    if self.data_partitioning_strategy["is_stratified"] == False:
                        cv = number_of_folds
                    else:
                        cv = StratifiedKFold(n_splits=number_of_folds)

                    scores = cross_val_score(self.k_neighbours_classifier, X=self.features, y=self.classes, cv=cv, scoring=current_score_type)
            
                    model_statistics += f"\n{current_score_type}:\n    {scores}\n    Mean: {scores.mean()}\n\n"
        except Exception as exception:
            print(f"\n{exception}\n")
        
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
            print(f"\n{exception}\n")
        
    def execute_training(self, data_processor: DataProcessor):        
        all_features = self.normalized_and_encoded_dataframe.drop(data_processor.get_last_column_of_dataframe(self.normalized_and_encoded_dataframe), axis=1)
        # Creates a dataframe from solely the data in the last column.
        all_classes = data_processor.get_last_column_as_a_separate_dataframe(self.dataframe)
        
        if (self.data_partitioning_strategy['is_stratified'] == True):
            which_part_base_stratification_on = all_classes

        # Split the data into train/test sets 
        features_train, features_test, classes_train, classes_test = train_test_split(
        all_features, all_classes, test_size=self.data_partitioning_strategy['testing_percentage'], random_state=10, stratify=which_part_base_stratification_on
        )   

        self.features_test = features_test

        self.classes = all_classes
        self.classes_test = classes_test
        
        # Creates a Knn Classifier Object.
        self.k_neighbours_classifier = KNeighborsClassifier(n_neighbors=self.k_value)
        # Trains this Knn Classifier with the training set obtained previously:
        self.k_neighbours_classifier.fit(features_train, classes_train)
        self.predictions = self.k_neighbours_classifier.predict(features_test)

def handle_nearest_neighbour_conductor_menu(dataframe, normalized_and_encoded_dataframe, data_partitioning_configuration):
    k_nearest_neighbour_conductors = []
    if data_partitioning_configuration['use_test_mode'] == True:
        for current_k_nearest_neighbour_conductor_index in range(1, 5):
            current_k_nearest_neighbour_conductor = K_nearest_neighbour_conductor(current_k_nearest_neighbour_conductor_index, dataframe, normalized_and_encoded_dataframe, data_partitioning_configuration)
            k_nearest_neighbour_conductors.append(current_k_nearest_neighbour_conductor)
        
        return k_nearest_neighbour_conductors       
        
    has_menu_been_exited = False
    while has_menu_been_exited == False:
        input_number_of_classifiers_to_train_using_k_nearest_neighbours = 0
        input_number_of_classifiers_to_train_using_k_nearest_neighbours = validate_user_input_integer("Enter the number of classifiers to train using k nearest neighbour: ", "The number of classifiers to train must be an integer", 100, 1)

        if (input_number_of_classifiers_to_train_using_k_nearest_neighbours > 0):
            for current_k_nearest_neighbour_conductor_index in range(input_number_of_classifiers_to_train_using_k_nearest_neighbours):
                is_current_k_value_valid = False
                while is_current_k_value_valid == False:
                    current_k_value = validate_user_input_integer(f"Enter the k value for the classifier with index {current_k_nearest_neighbour_conductor_index + 1}: ", "The current k value must be an integer")

                    if (current_k_value > 0):
                        current_k_nearest_neighbour_conductor = K_nearest_neighbour_conductor(current_k_value, dataframe, normalized_and_encoded_dataframe, data_partitioning_configuration)
                        k_nearest_neighbour_conductors.append(current_k_nearest_neighbour_conductor)
                        is_current_k_value_valid = True
                    else:
                        print("\nThe k value must be greater than 0.\n")

            has_menu_been_exited = True

        else: 
            print("\nThe number of classifiers to train must be greater than 0.\n")
            
    return k_nearest_neighbour_conductors

def handle_confusion_matrix_menu(k_nearest_neighbour_conductors_with_indices):
    try:
        if not k_nearest_neighbour_conductors_with_indices:
            raise ValueError("Classifiers must be trained before display the corresponding confusion matrices.")

        has_menu_been_exited = False
        while has_menu_been_exited == False:
            k_nearest_neighbour_conductors_with_indices_as_text = ""
            for current_index, current_k_nearest_neighbour_conductor in k_nearest_neighbour_conductors_with_indices.items():
                k_nearest_neighbour_conductors_with_indices_as_text += f"{current_index}. {current_k_nearest_neighbour_conductor.get_k_value_text()}\n"
            
            print(k_nearest_neighbour_conductors_with_indices_as_text)    
            
            confusion_matrix_index_input = 0
            
            confusion_matrix_index_input = validate_user_input_integer("Enter the index of the classifier for which you want to display the associated confusion matrix: ", "The number representing a classifier must be an integer", len(k_nearest_neighbour_conductors_with_indices.items()))
                
            if 0 < confusion_matrix_index_input <= len(k_nearest_neighbour_conductors_with_indices.items()):
                k_nearest_neighbour_conductors_with_indices[confusion_matrix_index_input].display_confusion_matrix()
                has_menu_been_exited = True
            else:
                print(f"\nThe number must be between 0 and the number of classifiers to train, i.e.{len(k_nearest_neighbour_conductors_with_indices.items())}\n")
    
    except Exception as exception:
        print(f"\n{exception}\n")

def handle_classify_unforeseen_sample_menu(k_nearest_neighbour_conductors, data_processor):
    if not k_nearest_neighbour_conductors:
        return print("\nTrained classifiers are required to classify unforeseen samples.\n")

    k_neighbours_classifier = ""
    input_features  = []
    has_menu_been_exited = False
    while has_menu_been_exited == False:
        try:
            classify_unforeseen_sample_classifier_menu_text = "\n"

            for current_index, current_k_nearest_neighbour_conductor in k_nearest_neighbour_conductors.items():
                classify_unforeseen_sample_classifier_menu_text += f"{current_index}. {current_k_nearest_neighbour_conductor.get_k_value_text()}\n"
            
            classify_unforeseen_sample_classifier_menu_text += "Select a model to use to classify the sample by typing the corresponding number: "

            number_of_classifiers = len(k_nearest_neighbour_conductors)
    
            selected_classifier_input = validate_user_input_integer(text_to_display=classify_unforeseen_sample_classifier_menu_text, maximum_input_value=number_of_classifiers)

            if (selected_classifier_input is None):
                raise ValueError("Invalid input: The input was likely not an integer.")
        
            if (0 < selected_classifier_input <= number_of_classifiers):
                k_neighbours_classifier = k_nearest_neighbour_conductors[selected_classifier_input].k_neighbours_classifier
                has_menu_been_exited = True
            else:
                print("\nEnter a valid integer.\n")

        except Exception as exception:
            print(f"\n{exception}\n")
    
    try:
        has_menu_been_exited = False
        while has_menu_been_exited == False:
            classify_unforeseen_sample_input_features_menu_text = "1. Load input features from a file\n2. Manually input all input features.\nSelect an option by typing the corresponding number: "

            try:
                classify_unforeseen_sample_input = int(input(classify_unforeseen_sample_input_features_menu_text))
            except:
                print("\nThe number representing an option must be an integer.\n")
            
            raw_dataframe_loaded_from_file = pandas.DataFrame()
            """Male,22,1.78,89.8,no,no,2,1,Sometimes,no,2,no,0,0,Sometimes,Public_Transportation"""

            match classify_unforeseen_sample_input:
                case 1:
                    raw_dataframe_loaded_from_file = pandas.read_csv("datasets/training/ObesityDataSet_raw_and_data_sinthetic.csv.csv")
                    input_features = data_processor.get_transformed_normalized_and_encoded_dataframe(raw_dataframe_loaded_from_file)
                    has_menu_been_exited = True
                    
                case 2:
                    raw_dataframe_loaded_from_input = pandas.DataFrame(index=[0])
                    for current_key in raw_dataframe_loaded_from_file.columns:
                        
                        unique_values = (
                            raw_dataframe_loaded_from_file[current_key]
                            .astype(str)
                            .unique()
                        )

                        has_the_current_value_been_assigned = False
                        while has_the_current_value_been_assigned == False:
                            key_value_input = input(
                                f"Enter value for {current_key}: "
                            ).strip()

                            if key_value_input in unique_values:
                                raw_dataframe_loaded_from_input[current_key] = key_value_input
                                has_the_current_value_been_assigned = True
                            else:
                                print(
                                    f"\n{key_value_input} was not found "
                                    f"in column {current_key}.\n"
                                )
                    
                    input_features = data_processor.get_transformed_normalized_and_encoded_dataframe(
                        raw_dataframe_loaded_from_input
                    )
        
                case _:
                    print("\nThe input must be 1 or 2.\n")
                    continue

            classify_unforeseen_sample_input
            prediction = k_neighbours_classifier.predict(input_features)
            print(f"\nThe unforeseen sample was predicted to be: {prediction}.\n")

    except Exception as exception:
        print(f"\n{exception}\n")