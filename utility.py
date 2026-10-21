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
