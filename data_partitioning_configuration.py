from enum import Enum

from utility import get_items_with_indices


class data_partitioning_strategy_names(Enum):
    TRAIN_TEST_SPLIT = "Train/Test Split"
    X_FOLD_CROSS_VALIDATION = "X-Fold Cross-Validation"

def handle_data_partitioning_menu(number_of_rows):
    data_partitioning_configuration = {
        "is_stratified": True,
        "data_partitioning_strategy_name": data_partitioning_strategy_names.TRAIN_TEST_SPLIT,
        "number_of_folds": 0,
        "training_percentage": 0,
        "testing_percentage": 0
    }
    
    partitioning_strategy_names_with_indices = get_items_with_indices(data_partitioning_strategy_names)

    data_partitioning_strategy_selection_menu_text = ""
    for current_index, current_partitioning_strategy in partitioning_strategy_names_with_indices.items():
        data_partitioning_strategy_selection_menu_text += f"\n{current_index}. {current_partitioning_strategy.value}"
    data_partitioning_strategy_selection_menu_text += "\nSelect a partitioning strategy to use by typing the corresponding number: "

    has_menu_been_exited = False
    while has_menu_been_exited == False:
        input_data_partitioning_strategy_selection = 0
        try:
            input_data_partitioning_strategy_selection = int(input(data_partitioning_strategy_selection_menu_text))
        except: 
            print("\nEnter an integer.\n")
        if (0 < input_data_partitioning_strategy_selection <= len(partitioning_strategy_names_with_indices)):
            data_partitioning_configuration["data_partitioning_strategy_name"] = partitioning_strategy_names_with_indices[input_data_partitioning_strategy_selection].value

            while has_menu_been_exited == False:
                if (data_partitioning_configuration["data_partitioning_strategy_name"] == data_partitioning_strategy_names.TRAIN_TEST_SPLIT.value):
                    training_split_input = 0
                    testing_split_input = 0

                    try:
                        training_split_input = int(input("Enter the training percentage of the split as an integer: "))
                        testing_split_input = int(input("Enter the testing percentage of the split as an integer: "))

                        data_partitioning_configuration["training_percentage"] = training_split_input
                        data_partitioning_configuration["testing_percentage"] = testing_split_input
                    except: 
                        print("\nEnter an integer.\n")

                    if (training_split_input + testing_split_input == 100):
                        has_menu_been_exited = True
                    else:
                        print("training split input + testing split input != 100%")
                else:
                    number_of_k_fold_input = 0

                    try:
                        number_of_k_fold_input = int(input("Enter number of folds to be used for cross validation, specified as an integer: "))
                        data_partitioning_configuration["number_of_folds"] = number_of_k_fold_input

                        if (number_of_k_fold_input < number_of_rows):
                            has_menu_been_exited = True
                        else:
                            print(f"The number of k folds must be less than the number of rows, i.e. {number_of_rows}.")
                    except:
                        print("\nEnter an integer.\n")

        else:
            print("Enter a valid integer.\n")

    has_menu_been_exited = False
    while has_menu_been_exited == False:
        stratified_sampling_menu_text = "Do you want to use a stratified sample [y/n]: "
        input_stratified_sampling_selection = input(stratified_sampling_menu_text)
        input_stratified_sampling_selection = input_stratified_sampling_selection.lower()

        if (input_stratified_sampling_selection == "y"):
            data_partitioning_configuration["is_stratified"] = True
            has_menu_been_exited = True
        elif (input_stratified_sampling_selection == "n"):
            data_partitioning_configuration["is_stratified"] = False
            has_menu_been_exited = True
        else:
            print("Enter y or n.")

    return data_partitioning_configuration