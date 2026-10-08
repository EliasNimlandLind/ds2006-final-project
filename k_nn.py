class K_nn_conductor():
    def __init__(self, k_value, dataframe):
        self.k_value = k_value
        self.dataframe = dataframe

    def __str__(self):
        return f"k = {self.k_value}"

def handle_k_nn_menu():
    