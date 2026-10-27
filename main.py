from k_nearest_neighbour import handle_confusion_matrix_menu, handle_nearest_neighbour_conductor_menu, handle_classify_unforeseen_sample_menu

from data_processing import DataProcessor
from data_frame import handle_data_frame_menu, print_dataframe_statistics
from data_partitioning_configuration import handle_data_partitioning_menu

from utility import get_items_as_a_indexed_dictionary, save_strings_to_file, get_valid_user_input_integer


def main():
    
    k_nearest_neighbour_conductors_without_indices = []
    
    data_processor = DataProcessor()

    has_menu_been_exited = False
    while has_menu_been_exited == False:
        main_menu_option_selection_text = ("1. Load a dataset and create a configuration for the training of the classifiers.\n"
                                           "2. Train classifiers.\n"
                                           "3. Show confusion matrix.\n"
                                           "4. Save data to file.\n"
                                           "5. Display model statistics.\n"
                                           "6. Classify an unforeseen sample.\n"
                                           "0. Exit the application.\n"
                                           "Enter the choice of how to continue, as an integer: ")
        main_menu_selected_option = get_valid_user_input_integer(main_menu_option_selection_text, "The choice must be specified as an integer.", 6, 0)
    
        match main_menu_selected_option:
            case 1:
                dataframe, normalized_and_encoded_dataframe = handle_data_frame_menu(data_processor)
                print_dataframe_statistics(data_processor, dataframe, normalized_and_encoded_dataframe)
                
                data_partitioning_configuration = handle_data_partitioning_menu(dataframe.shape[0])
                k_nearest_neighbour_conductors_without_indices = handle_nearest_neighbour_conductor_menu(dataframe, normalized_and_encoded_dataframe, data_partitioning_configuration)

                training_configuration_text = ("\n*********************************************\n"
                                            "EXPERIMENT CONFIGURATION\n\n"
                                            "Data Partitioning Strategy:\n"
                                            f"{data_partitioning_configuration['data_partitioning_strategy_name']}\n\n"
                                            "k-NN Experiments:\n\n")

                k_nearest_neighbour_conductors_with_indices = get_items_as_a_indexed_dictionary(k_nearest_neighbour_conductors_without_indices)
                for current_index, current_k_nearest_neighbour_conductor in k_nearest_neighbour_conductors_with_indices.items():
                    training_configuration_text += f"Experiment: {current_index} {current_k_nearest_neighbour_conductor.get_k_value_text()}\n"  
                training_configuration_text += "*********************************************"
                print(training_configuration_text)
            
            case 2:
                # This is used to avoid trying to execute the training of conductors that have not been initialised, and to display an error message if the conductors are not initialised. 
                if not k_nearest_neighbour_conductors_without_indices:
                    print("\nA configuration for the training was not found.\n")
                    continue

                for current_k_nearest_neighbour_conductor in k_nearest_neighbour_conductors_without_indices:
                    current_k_nearest_neighbour_conductor.execute_training(data_processor)

                print("\nThe classifiers were successfully trained.\n")
            
            case 3:
                handle_confusion_matrix_menu(k_nearest_neighbour_conductors_with_indices)

            case 4:
                try:
                    file_name_input = input("Enter the file name that will contain all data: ")
                    texts_to_save = []
    
                    dataframe_row_count = 50
                    dataframes_text_to_save = f"Dataframes - First {dataframe_row_count} rows\n"
                    dataframes_text_to_save += "\nRaw\n\n"
                    dataframes_text_to_save += f"{dataframe.head(dataframe_row_count).to_string()}\n"

                    dataframes_text_to_save += f"\nNormalised and encoded\n\n"
                    dataframes_text_to_save += normalized_and_encoded_dataframe.head(dataframe_row_count).to_string()
                    texts_to_save.append(dataframes_text_to_save)

                    data_partitioning_text_to_save = "\n\nData partitioning configuration\n\n"
                    for current_configuration_name, current_configuration_value in data_partitioning_configuration.items():
                        data_partitioning_text_to_save += f"{current_configuration_name}: {current_configuration_value}\n"
                    texts_to_save.append(data_partitioning_text_to_save)

                    model_text_to_save = "\nThe models\n\n"
                    for current_k_nearest_neighbour_conductor in k_nearest_neighbour_conductors_without_indices:
                        model_text_to_save += str(current_k_nearest_neighbour_conductor)
                    texts_to_save.append(model_text_to_save)
                    
                    was_all_save_operations_successful = save_strings_to_file(texts_to_save, file_name_input)

                    if was_all_save_operations_successful == True:
                        print("\nThe data was successfully saved.\n")

                except Exception as exception:
                    print(f"\n{exception}\n")

            case 5:
                if not k_nearest_neighbour_conductors_without_indices:
                    print("\nTrained classifiers are required to display the statistics.\n")
                    continue

                for current_k_nearest_neighbour_conductor in k_nearest_neighbour_conductors_without_indices:
                    print(str(current_k_nearest_neighbour_conductor))            

            case 6:
                handle_classify_unforeseen_sample_menu(k_nearest_neighbour_conductors_with_indices, data_processor)

            case 0:
                print("\nExiting...\n")
                has_menu_been_exited = True
                
            case _:
                print("\nInvalid choice. The integer must correspond to one of the stated choices.\n")


if __name__ == "__main__":
    main()