from data_frame import get_dataframe_rows, handle_data_frame_menu
from data_partitioning_configuration import handle_data_partitioning_menu

def main():
    dataframe = handle_data_frame_menu()
    data_partitioning_configuration = handle_data_partitioning_menu(get_dataframe_rows())

    print(data_partitioning_configuration)
main()