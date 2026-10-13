from k_nearest_neighbour import handle_nearest_neighbour_conductor_menu
from data_frame import handle_data_frame_menu
from data_partitioning_configuration import handle_data_partitioning_menu
from utility import get_items_as_string_with_indices

def main():
    has_menu_been_exited = False
    while has_menu_been_exited == False:
        try:
            main_menu_input = int(input("1. Load a dataset and create a configuration for the experiments.\n2. Conduct experiments.\n3. Exit the application.\nEnter the choice of how to continue, as an integer: "))
        except:
            print("\nThe choice must be specified as an integer.\n")
        
        k_nearest_neighbour_conductors_without_indices = []
        match main_menu_input:
            case 1:
                dataframe = handle_data_frame_menu()
                data_partitioning_configuration = handle_data_partitioning_menu(dataframe.shape[0])
                k_nearest_neighbour_conductors_without_indices = handle_nearest_neighbour_conductor_menu(dataframe, data_partitioning_configuration)
                
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
                if not k_nearest_neighbour_conductors_without_indices: 
                    print("\nA configuration for experiments was not found.\n")
                    continue

                for current_k_nearest_neighbour_conductor in k_nearest_neighbour_conductors_without_indices:
                    current_k_nearest_neighbour_conductor.execute_experiment()

            case 3:
                print("Exiting...")
                has_menu_been_exited = True
                
            case _:
                print("\nInvalid choice. The integer must correspond to one of the stated choices.\n")

main()