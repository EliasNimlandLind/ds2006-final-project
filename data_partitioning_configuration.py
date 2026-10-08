from enum import Enum


class data_partitioning_strategy_names(Enum):
    TRAIN_TEST_SPLIT = "Train/Test Split"
    X_FOLD_CROSS_VALIDATION = "X-Fold Cross-Validation"

def handle_data_partitioning_menu():
    data_partitioning_configuration = {
        "is_stratified": True,
        "data_partitioning_strategy_name": data_partitioning_strategy_names.TRAIN_TEST_SPLIT,
        "number_of_folds": 0,
        "training_percentage": 0,
        "test_percentage": 0
    }
    
    partitioning_strategy_names_with_indices = {index: data_partitioning_name
                                                for index, data_partitioning_name in enumerate(list(data_partitioning_strategy_names), start=1)
                                                }  

    data_partitioning_strategy_selection_menu_text = ""
    for index, current_partitioning_strategy in partitioning_strategy_names_with_indices.items():
        data_partitioning_strategy_selection_menu_text += f"\n{index}. {current_partitioning_strategy.value}"
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
            
            if (data_partitioning_configuration["data_partitioning_strategy_name"] == data_partitioning_strategy_names.TRAIN_TEST_SPLIT.value):
                
            has_menu_been_exited = True
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