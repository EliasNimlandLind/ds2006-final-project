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

def validate_user_input_integer(text_to_display, value_error_message = "Enter an integer", maximum_input_value = 0, minimum_input_value = 1):
    """
    This function tries to convert an integer represented as a string, gathered from the user.
    
    Returns: An integer representation of the integer represented as string is returned if the validation succeed.
    """
    user_input_as_string = input(text_to_display)
    try:
        user_input_as_integer = int(user_input_as_string)
        
        if maximum_input_value > minimum_input_value:
            if minimum_input_value <= user_input_as_integer <= maximum_input_value:
                return user_input_as_integer
            else:
                raise ValueError(f"\n{value_error_message}, between {minimum_input_value} and {maximum_input_value}.\n")
            
        if minimum_input_value <= user_input_as_integer:
            return user_input_as_integer
        else:
            raise ValueError(f"\n{value_error_message}, greater than {minimum_input_value}.\n")
            
    except ValueError as value_error:
        print(f"\nInvalid input: {value_error}\n")

def save_strings_to_file(strings_to_save, save_file_name = "experiments_save_file", file_extension = ".txt"):
    was_all_save_operations_successful = False
    complete_file_name = save_file_name

    if not complete_file_name.endswith(file_extension):
        complete_file_name += file_extension

    # Usage of "With" minimises errors such as corruption by not requiring manual opening and closing of files.
    try:
        with open(complete_file_name, mode="w") as save_file:
            for current_string_to_save in strings_to_save:
                save_file.write(current_string_to_save)

        was_all_save_operations_successful = True
    except IOError as io_error:
        print(f"Input or output error: {io_error}")
    
    return was_all_save_operations_successful 