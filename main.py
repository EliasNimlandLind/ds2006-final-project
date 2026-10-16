from k_nearest_neighbour import handle_nearest_neighbour_conductor_menu
from data_frame import handle_data_frame_menu
from data_partitioning_configuration import handle_data_partitioning_menu
from utility import get_items_as_string_with_indices

def main():
    has_menu_been_exited = False
    k_nearest_neighbour_conductors_without_indices = []

    while has_menu_been_exited == False:
        try:
            main_menu_input = int(input("1. Load a dataset and create a configuration for the experiments.\n2. Conduct experiments.\n3. Show confusion matrix.\n0. Exit the application.\nEnter the choice of how to continue, as an integer: "))
        except:
            print("\nThe choice must be specified as an integer.\n")
        
        match main_menu_input:
            case 1:
                dataframe, normalized_features_as_a_dataframe = handle_data_frame_menu()
                data_partitioning_configuration = handle_data_partitioning_menu(dataframe.shape[0])
                k_nearest_neighbour_conductors_without_indices = handle_nearest_neighbour_conductor_menu(dataframe, normalized_features_as_a_dataframe, data_partitioning_configuration)

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
                    print("\nA configuration for experiments was not found.\n")
                    continue

                for current_k_nearest_neighbour_conductor in k_nearest_neighbour_conductors_without_indices:
                    current_k_nearest_neighbour_conductor.execute_experiment()
            
            case 3:
                has_menu_been_exited = False
                while has_menu_been_exited == False:
                    confusion_matrix_index_input = 0
                    try:
                        confusion_matrix_index_input = int(input("Enter the number corresponing to the experiment for which you want to display the associated confusion matrix. Avoid this by enter '0': "))
                    except:
                        print("\nThe number of experiments to conduct must be an integer.\n")

                    if not k_nearest_neighbour_conductors_without_indices: # This is used to check if the list is empty, and a message is displayed if the list is empty. 
                        print("\n Experiments must be conducted before display the corresponding confusion matrices.\n")
                        continue
        
                    if 0 < confusion_matrix_index_input <= len(k_nearest_neighbour_conductors_with_indices.items()):
                        k_nearest_neighbour_conductors_with_indices[confusion_matrix_index_input].display_confusion_matrix()
                                     
                    else:
                        print(f"\nThe number must be between 0 and the number of experiemnts, i.e.{len(k_nearest_neighbour_conductors_with_indices.items())}\n")

            case 0:
                print("\nExiting...\n")
                has_menu_been_exited = True
                
            case _:
                print("\nInvalid choice. The integer must correspond to one of the stated choices.\n")


main()