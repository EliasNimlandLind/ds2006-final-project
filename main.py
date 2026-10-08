from data_frame import handle_data_frame_menu
from data_partitioning_configuration import handle_data_partitioning_menu

def main():
    dataframe = handle_data_frame_menu()
    number_of_rows = dataframe.shape[0]
    data_partitioning_configuration = handle_data_partitioning_menu(number_of_rows)

    print(data_partitioning_configuration)
main()