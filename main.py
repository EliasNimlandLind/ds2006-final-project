from K_nearest_neighbour import handle_nearest_neighbour_conductor_menu
from data_frame import handle_data_frame_menu
from data_partitioning_configuration import handle_data_partitioning_menu

def main():
    dataframe = handle_data_frame_menu()
    data_partitioning_configuration = handle_data_partitioning_menu(dataframe.shape[0])

    handle_nearest_neighbour_conductor_menu(dataframe, data_partitioning_configuration["data_partitioning_strategy_name"])
    print(data_partitioning_configuration)
main()