def get_items_with_indices(items_without_indices):
    """
        Returns a dictionary comprising each index as a key and each corresponding value being an item based on the argument.
    """
    items_with_indices = {
        current_index: current_item
        for current_index, current_item in enumerate(items_without_indices, start=1)
    }
    return items_with_indices