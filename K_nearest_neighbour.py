from sklearn.metrics import accuracy_score, classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, cross_val_score, KFold

from data_partitioning_configuration import data_partitioning_strategy_names

class K_nearest_neighbour_conductor():
    def __init__(self, k_value, dataframe, data_partitioning_configuration):
        self.k_value = k_value
        self.dataframe = dataframe
        self.data_partitioning_strategy = data_partitioning_configuration

    def __str__(self):
        return f"k = {self.k_value}"

    def execute_experiment(self):        
        features = self.dataframe.drop(self.dataframe.columns[-1],axis=1)
        # Creates a dataframe from solely the data in the last column.
        classes = self.dataframe[self.dataframe.columns[-1]]
        
        if (self.data_partitioning_strategy['is_stratified'] == True):
            what_to_stratify = classes

        # Creates a Knn Classifier Object.
        k_neighbours_classifier = KNeighborsClassifier(n_neighbors=self.k_value)

        # Split the data into train/test sets 
        features_train, features_test, classes_train, classes_test = train_test_split(
        features, classes, test_size=self.data_partitioning_strategy['testing_percentage'], random_state=10, stratify=what_to_stratify
        )     

        k_neighbours_classifier.fit(features_train, classes_train)

        model_statistics = ""

        if (self.data_partitioning_strategy['data_partitioning_strategy_name'] == data_partitioning_strategy_names.TRAIN_TEST_SPLIT.value):
            # Trains this Knn Classifier with the training set obtained previously:

            # Obtains the predictions from the kNN classifier:
            predictions = k_neighbours_classifier.predict(features_test)
            model_statistics = (f"\n{str(self)}\n"
                                f"Accuracy: {accuracy_score(classes_test, predictions)}\n\n"
                                f"  {classification_report(classes_test, predictions)}\n\n"
                                )
        else:
            cross_val_scores = cross_val_score(k_neighbours_classifier, X=features, y=classes, cv=self.data_partitioning_strategy['number_of_folds'], scoring="accuracy")
            model_statistics = f"\n{str(self)}\nAccuracy:\n    {cross_val_scores}\n    Mean: {cross_val_scores.mean()}"
        
        print(model_statistics)
            
        self.k_neighbours_classifier = k_neighbours_classifier

def handle_nearest_neighbour_conductor_menu(dataframe, data_partitioning_configuration):
    k_nearest_neighbour_conductors = []

    has_menu_been_exited = False
    while has_menu_been_exited == False:
        input_number_of_experiments_using_k_nearest_neighbours = 0

        try:
            input_number_of_experiments_using_k_nearest_neighbours = int(input("Enter the number of experiments to conduct using k nearest neighbour: "))
        except:
            print("\nThe number of experiments to conduct must be an integer.\n")

        if (input_number_of_experiments_using_k_nearest_neighbours > 0):
            for current_k_nearest_neighbour_conductor_index in range(input_number_of_experiments_using_k_nearest_neighbours):
                is_current_k_value_valid = False
                while is_current_k_value_valid == False:
                    try:
                        current_k_value = int(input(f"Enter the k value for experiment number {current_k_nearest_neighbour_conductor_index + 1}: "))
                    except:
                        print("\nThe current k value must be an integer.\n")

                    if (current_k_value > 0):
                        current_k_nearest_neighbour_conductor = K_nearest_neighbour_conductor(current_k_value, dataframe, data_partitioning_configuration)
                        k_nearest_neighbour_conductors.append(current_k_nearest_neighbour_conductor)
                        is_current_k_value_valid = True
                    else:
                        print("\nThe k value must be greater than 0.\n")
            has_menu_been_exited = True
        else: 
            print("\nThe number of experiments to conduct must be greater than 0.\n")
    return k_nearest_neighbour_conductors