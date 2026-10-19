from k_nearest_neighbour import handle_nearest_neighbour_conductor_menu
from data_frame import handle_data_frame_menu
from data_partitioning_configuration import handle_data_partitioning_menu
from utility import get_items_as_string_with_indices

def main():
    has_menu_been_exited = False
    k_nearest_neighbour_conductors_without_indices = []

    while has_menu_been_exited == False:
        try:
            main_menu_input = int(input(("1. Load a dataset and create a configuration for the experiments."
                                         "\n2. Conduct experiments."
                                         "\n3. Show confusion matrix."
                                         "\n4. Save data to file."
                                         "\n0. Exit the application."
                                         "\nEnter the choice of how to continue, as an integer: ")))
        except:
            print("\nThe choice must be specified as an integer.\n")
        
        match main_menu_input:
            case 1:
                dataframe, normalized_and_encoded_dataframe = handle_data_frame_menu()
                data_partitioning_configuration = handle_data_partitioning_menu(dataframe.shape[0])
                k_nearest_neighbour_conductors_without_indices = handle_nearest_neighbour_conductor_menu(dataframe, normalized_and_encoded_dataframe, data_partitioning_configuration)

                experiment_configuration_text = ("\n*********************************************\n"
                                            "EXPERIMENT CONFIGURATION\n\n"
                                            "Data Partitioning Strategy:\n"
                                            f"{data_partitioning_configuration['data_partitioning_strategy_name']}\n\n"
                                            "k-NN Experiments:\n\n")

                k_nearest_neighbour_conductors_with_indices = get_items_as_string_with_indices(k_nearest_neighbour_conductors_without_indices)
                for current_index, current_k_nearest_neighbour_conductor in k_nearest_neighbour_conductors_with_indices.items():
                    experiment_configuration_text += f"Experiment: {current_index} {str(current_k_nearest_neighbour_conductor)}\n"  
                experiment_configuration_text += "*********************************************"
                print(experiment_configuration_text)
            
            case 2:
                if not k_nearest_neighbour_conductors_without_indices: # This is used to check if the list is empty, and a message is displayed if the list is empty. 
                    print("\nA configuration for the experiments was not found.\n")
                    continue

                for current_k_nearest_neighbour_conductor in k_nearest_neighbour_conductors_without_indices:
                    current_k_nearest_neighbour_conductor.execute_experiment()
            
            case 3:
                confusion_matrix_experiments_status_error = "\nExperiments must be conducted before display the corresponding confusion matrices.\n"
                try:
                    has_menu_been_exited = False
                    while has_menu_been_exited == False:
                        k_nearest_neighbour_conductors_with_indices_as_text = ""
                        for current_index, current_k_nearest_neighbour_conductor in k_nearest_neighbour_conductors_with_indices.items():
                            k_nearest_neighbour_conductors_with_indices_as_text += f"{current_index}. {str(current_k_nearest_neighbour_conductor)}\n"
                        
                        print(k_nearest_neighbour_conductors_with_indices_as_text)    
                        
                        confusion_matrix_index_input = 0
                        try:
                            confusion_matrix_index_input = int(input("Enter the number corresponding to the experiment for which you want to display the associated confusion matrix. Avoid this by enter '0': "))
                        except:
                            print("\nThe number representing an experiment must be an integer.\n")
                            
                        if 0 < confusion_matrix_index_input <= len(k_nearest_neighbour_conductors_with_indices.items()):
                            k_nearest_neighbour_conductors_with_indices[confusion_matrix_index_input].display_confusion_matrix()
                            has_menu_been_exited = True
                        else:
                            print(f"\nThe number must be between 0 and the number of experiments, i.e.{len(k_nearest_neighbour_conductors_with_indices.items())}\n")
                
                except:
                    print(confusion_matrix_experiments_status_error)

            case 4:
                try:  
                    file_name_input = input("Enter the file name that will contain all data: ")
                    complete_file_name = file_name_input
                    file_extension = ".txt"

                    if complete_file_name == "":
                        complete_file_name = f"experiments_save_file{file_extension}"

                    if not complete_file_name.endswith(file_extension):
                        complete_file_name += file_extension
                    
                    with open(complete_file_name, "w") as save_file:
                        save_file_text = ""

                        dataframe_row_count = 50
                        save_file_text += f"\nDataframes - First {dataframe_row_count} rows\n"
                        save_file_text += "\nRaw\n"
                        save_file_text += dataframe.head(dataframe_row_count).to_string()

                        save_file_text += f"\nNormalised and encoded\n"
                        save_file_text += normalized_and_encoded_dataframe.head(dataframe_row_count).to_string()


                        save_file_text += "\n\nData partitioning configuration\n\n"
                        for current_configuration_name, current_configuration_value in data_partitioning_configuration.items():
                            save_file_text += f"{current_configuration_name}: {current_configuration_value}\n"


                        
                        save_file.write(save_file_text)
                        
                        print("\The data was successfully saved.\n")
                except Exception as exception:
                    print(f"\nError: {exception}\n")
            case 0:
                print("\nExiting...\n")
                has_menu_been_exited = True
                
            case _:
                print("\nInvalid choice. The integer must correspond to one of the stated choices.\n")


main()