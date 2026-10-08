import os

import pandas

def main():
    datasets_directory_name = "datasets"
    datasets_found_in_directory = os.listdir(datasets_directory_name)
    
    datasets_with_indices = {
        index: dataset
        for index, dataset in enumerate(datasets_found_in_directory, start=1)
    }

    dataset_selection_menu_text = "Select a dataset to load by typing the corresponding number"
    for index, dataset in datasets_with_indices.items():
        dataset_selection_menu_text += f"\n{index}. {dataset}"
    dataset_selection_menu_text += f"\n{len(datasets_with_indices) + 1}. Another dataset.\n"

    path_to_dataset_to_load = ""
    input_dataset_selection = int(input(dataset_selection_menu_text))
    if (0 < input_dataset_selection <= len(datasets_with_indices)):
        path_to_dataset_to_load = f"{datasets_directory_name}/{datasets_with_indices[input_dataset_selection]}"
    
    elif (len(datasets_with_indices) < input_dataset_selection < len(datasets_with_indices) + 2): # This alternative should only be true if the selected value between the length of all identified datasets and less than the length + 2-.
        dataset_selection_menu_text = "Enter the path to the dataset: "
        input_dataset_selection = input(dataset_selection_menu_text)

        path_to_dataset_to_load = input_dataset_selection

    else:
        print("Invalid input.")

    dataframe = pandas.read_csv(path_to_dataset_to_load)

    dataframe_column_names_text = ""
    for current_feature_name in dataframe.columns[:-1]: # Using [:-1] is done to limit the iteration to item before the last one to avoid concatenate the name of the target classes.
        dataframe_column_names_text += f"\n{str(current_feature_name)}"

    dataframe_target_classes_text = ""
    for current_target_class_name in dataframe[dataframe.columns[-1]].unique(): # This gets all unique values from the last column, i.e. the target classes.
        dataframe_target_classes_text += f"\n{str(current_target_class_name)}"

    # Using a collection leads to high readability due to all data being viewable at once due to vertical alignment.
    dataframe_complete_information_text = (f"\nThe dataset was loaded correctly.\n\n" 
                                           f"{dataframe.head(10)}\n\n"
                                           f"The number of rows: {dataframe.shape[0]}\nThe number of columns: {dataframe.shape[1]}\n\n"
                                           f"The names of the features: {dataframe_column_names_text}\n\n"
                                           f"The names of the target classes are: {dataframe_target_classes_text}\n\n"
                                           f"{dataframe.describe()}\n\n{dataframe[dataframe.columns[-1]].value_counts()}")
    
    print(dataframe_complete_information_text)
main()