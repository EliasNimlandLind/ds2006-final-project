from K_nearest_neighbour import handle_nearest_neighbour_conductor_menu
from data_frame import handle_data_frame_menu
from data_partitioning_configuration import handle_data_partitioning_menu
from utility import get_items_with_indices

def main():
    dataframe = handle_data_frame_menu()
    data_partitioning_configuration = handle_data_partitioning_menu(dataframe.shape[0])

    k_nearest_neighbour_conductors_without_indices = handle_nearest_neighbour_conductor_menu(dataframe, data_partitioning_configuration["data_partitioning_strategy_name"])
    experiment_configuration_text = ("\n*********************************************\n"
                                "EXPERIMENT CONFIGURATION\n\n"
                                "Data Partitioning Strategy:\n"
                                f"{data_partitioning_configuration['data_partitioning_strategy_name']}\n\n"
                                "k-NN Experiments:\n\n")

    k_nearest_neighbour_conductors_with_indices = get_items_with_indices(k_nearest_neighbour_conductors_without_indices)
    for current_index, current_k_nearest_neighbour_conductor in k_nearest_neighbour_conductors_with_indices.items():
        experiment_configuration_text += f"Experiment: {current_index} {str(current_k_nearest_neighbour_conductor)}\n"
        
    experiment_configuration_text += "*********************************************"
    print(experiment_configuration_text)
main()