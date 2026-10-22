from enum import Enum

from utility import get_items_as_a_indexed_dictionary, get_valid_user_input_integer


class data_partitioning_strategy_names(Enum):
    TRAIN_TEST_SPLIT = "Train/Test Split"
    K_FOLD_CROSS_VALIDATION = "K-Fold Cross-Validation"

def handle_data_partitioning_menu(number_of_rows):
    data_partitioning_configuration = {
        'is_stratified': True,
        'data_partitioning_strategy_name': data_partitioning_strategy_names.TRAIN_TEST_SPLIT,
        'number_of_folds': 0,
        'training_percentage': 0.8,
        'testing_percentage': 0.2,
        'use_test_mode': False
    }

    partitioning_strategy_names_with_indices = get_items_as_a_indexed_dictionary(data_partitioning_strategy_names)

    data_partitioning_strategy_selection_menu_text = ""
    for current_index, current_partitioning_strategy in partitioning_strategy_names_with_indices.items():
        data_partitioning_strategy_selection_menu_text += f"\n{current_index}. {current_partitioning_strategy.value}"

    default_data_partitioning_configuration_index = len(partitioning_strategy_names_with_indices.keys()) + 1
    data_partitioning_strategy_selection_menu_text += f"\n{default_data_partitioning_configuration_index}. Use the default configuration.\n"
    data_partitioning_strategy_selection_menu_text += "\nSelect a partitioning strategy to use by typing the corresponding number: "

    has_menu_been_exited = False
    while has_menu_been_exited == False:
        number_of_menu_options = len(partitioning_strategy_names_with_indices)
        
        input_data_partitioning_strategy_selection = 0
        input_data_partitioning_strategy_selection = get_valid_user_input_integer(data_partitioning_strategy_selection_menu_text, number_of_menu_options)

        if input_data_partitioning_strategy_selection == default_data_partitioning_configuration_index:
            data_partitioning_configuration["use_test_mode"] = True
            return data_partitioning_configuration
        
        if (0 < input_data_partitioning_strategy_selection <= number_of_menu_options):
            data_partitioning_configuration['data_partitioning_strategy_name'] = partitioning_strategy_names_with_indices[input_data_partitioning_strategy_selection].value

            while has_menu_been_exited == False:
                training_split_input = 0
                testing_split_input = 0
                
                training_split_input = get_valid_user_input_integer("Enter the training percentage of the split as an integer: ", "The value must be an integer", maximum_input_value=100)
                testing_split_input = get_valid_user_input_integer("Enter the testing percentage of the split as an integer: ", "The value must be an integer", maximum_input_value=100)

                data_partitioning_configuration['training_percentage'] = training_split_input / 100 # Division is done to get the floating point representation.
                data_partitioning_configuration['testing_percentage'] = testing_split_input / 100 

                if (training_split_input + testing_split_input == 100):
                    has_menu_been_exited = True
                else:
                    print("training split input + testing split input != 100%")
                
                if (data_partitioning_configuration['data_partitioning_strategy_name'] == data_partitioning_strategy_names.K_FOLD_CROSS_VALIDATION.value):
                    number_of_k_fold_input = 0
                
                    try:
                        number_of_k_fold_input = int(input("Enter number of folds to be used for cross validation, specified as an integer: "))
                        data_partitioning_configuration['number_of_folds'] = number_of_k_fold_input

                        if (2 <= number_of_k_fold_input < number_of_rows):
                            has_menu_been_exited = True
                        else:
                            print(f"The number of k folds must be less than the number of rows, i.e. {number_of_rows}, in addition to being less than or equal to two.")
                    except:
                        print("\nEnter an integer.\n")
        else:
            print("Enter a valid integer.\n")

    has_menu_been_exited = False
    while has_menu_been_exited == False:
        stratified_sampling_menu_text = "Do you want to use a stratified sample [y/n]: "
        input_stratified_sampling_selection = input(stratified_sampling_menu_text).lower()

        if (input_stratified_sampling_selection == "y"):
            data_partitioning_configuration['is_stratified'] = True
            has_menu_been_exited = True
        elif (input_stratified_sampling_selection == "n"):
            data_partitioning_configuration['is_stratified'] = False
            has_menu_been_exited = True
        else:
            print("\n\nEnter y or n.\n\n")

    return data_partitioning_configuration