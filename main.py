from data_frame import handle_data_frame_menu
from data_partitioning_names import data_partitioning_strategy_names, handle_data_partitioning_menu

def main():
    dataframe = handle_data_frame_menu()
    data_partitioning_configuration = handle_data_partitioning_menu()

    print(dataframe)
    print(data_partitioning_configuration)
main()