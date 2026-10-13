import os


def get_items_as_string_with_indices(items_without_indices):
    """
        Returns a dictionary comprising each index as a key and each corresponding value being an item based on the argument.
    """
    items_with_indices = {
        current_index: current_item
        for current_index, current_item in enumerate(items_without_indices, start=1)
    }
    return items_with_indices

def list_content_of_directory(directory_name):
    if os.path.exists(directory_name) == False:
        os.mkdir(directory_name)
        
    return os.listdir(directory_name)

def get_last_column_as_a_separate_dataframe(dataframe):
    return dataframe[get_last_column_of_dataframe(dataframe)]

def get_last_column_of_dataframe(dataframe):
    """
    This can be used to get the classes, if these are contained in the last column.
    """
    return dataframe.columns[-1]