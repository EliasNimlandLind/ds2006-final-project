import os

import pandas

from data_preprocessing import encode_categorical_dataframe, normalize_numerical_dataframe, get_normalized_and_encoded_dataframe
from utility import get_last_column_as_a_separate_dataframe, get_last_column_of_dataframe, get_items_as_string_with_indices, list_content_of_directory    

dataframe = None

def handle_data_frame_menu():
    datasets_directory_name = "datasets"
    datasets_found_in_directory = list_content_of_directory(datasets_directory_name)
    
    datasets_with_indices = get_items_as_string_with_indices(datasets_found_in_directory)

    dataset_selection_menu_text = ""
    for current_index, dataset in datasets_with_indices.items():
        dataset_selection_menu_text += f"\n{current_index}. {dataset}"
    dataset_selection_menu_text += (f"\n{len(datasets_with_indices) + 1}. A dataset not located in the default directory.\n"
                                    "Select a dataset to load by typing the corresponding number: ")
    
    path_to_dataset_to_load = ""

    has_menu_been_exited = False
    while has_menu_been_exited == False:
        input_dataset_selection = 0
        try:
            input_dataset_selection = int(input(dataset_selection_menu_text))
        except: 
            print("Enter an integer.\n")

        if (0 < input_dataset_selection <= len(datasets_with_indices)):
            path_to_dataset_to_load = f"{datasets_directory_name}/{datasets_with_indices[input_dataset_selection]}"
            has_menu_been_exited = True
            
        elif (len(datasets_with_indices) < input_dataset_selection < len(datasets_with_indices) + 2): # This alternative should only be true if the selected value between the length of all identified datasets and less than the length + 2.
            dataset_selection_menu_text = "Enter the path to the dataset: "
            input_dataset_selection = input(dataset_selection_menu_text)

            path_to_dataset_to_load = input_dataset_selection

            if os.path.exists(path_to_dataset_to_load) == False:
                print("\nNo such directory exists.")
                continue # If the directory specified by the user does not exists, the loop iterates without assigning has_menu_been_exited to true.

            has_menu_been_exited = True

        else:
            print("Enter a valid integer.\n")

    dataframe = pandas.read_csv(path_to_dataset_to_load)
    normalized_and_encoded_dataframe = get_normalized_and_encoded_dataframe(dataframe)
    
    dataframe_column_names_text = ""
    for current_feature_name in dataframe.columns[:-1]: # Using [:-1] is done to limit the iteration to item before the last one to avoid concatenate the name of the target classes.
        dataframe_column_names_text += f"\n{str(current_feature_name)}"

    dataframe_target_classes_text = ""
    for current_target_class_name in get_last_column_as_a_separate_dataframe(dataframe).unique(): # This gets all unique values from the last column, i.e. the target classes.
        dataframe_target_classes_text += f"\n{str(current_target_class_name)}"

    # Using a collection leads to high readability due to all data being viewable at once due to vertical alignment.
    dataframe_complete_information_text = (f"\n\nThe values of the 10 first rows before encoding and normalization are:\n"
                                           f"{dataframe.head(10)}\n\n"
                                           f"The values of the 10 first rows after encoding and normalization are:\n"
                                           f"{normalized_and_encoded_dataframe.head(10)}\n\n"
                                           f"The number of rows: {dataframe.shape[0]}\nThe number of columns: {dataframe.shape[1]}\n\n"
                                           f"The names of the features: {dataframe_column_names_text}\n\n"
                                           f"The names of the target classes are: {dataframe_target_classes_text}\n\n"
                                           f"{dataframe.describe()}\n\n{get_last_column_as_a_separate_dataframe(dataframe).value_counts()}\n"
                                           f"\nThe dataset was loaded correctly.\n")
    
    print(dataframe_complete_information_text)
    return dataframe, normalized_and_encoded_dataframe