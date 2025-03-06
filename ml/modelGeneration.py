# Model training and testing

# Imports
import os
import csv


# Globals
DATA_SET='/Users/zachmcfadden/Desktop/dev/tmp/smashStudyDataSet'

"""
    Simple enum for all data categories 
"""
class DataCategories:
    CAS: str = "CAS"
    NG:  str = "NG"
    MOBA:str = "MOBA"
    COS :str = "COS"
    ES  :str = "ES"
    FPS :str = "FPS"
    # In case there's an untracked data category to clean up later
    UNKNOWN: str = "UNKNOWN"


"""
    Simple storage class for participant data 
"""
class SubjectDataStructured:

    @staticmethod
    def csv_to_dict(csv_filepath):
        data = []
        with open(csv_filepath, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        return data


    def __serializeCSVs(self):
        print(f"Serializing {self.id}")

        for sCSV in self.__originalCSVs:

            if "TaskSwitching" in sCSV:
                self.taskSwitchingDataStructured = SubjectDataStructured.csv_to_dict(
                    sCSV
                )
            elif "PosnerCue" in sCSV:
                self.posnerDataStructured = SubjectDataStructured.csv_to_dict(
                    sCSV
                )
            elif "GoNoGo" in sCSV:
                self.goNoGoStructured = SubjectDataStructured.csv_to_dict(
                    sCSV
                )
            elif "SimpleReaction" in sCSV:
                self.simpleReactionStructured = SubjectDataStructured.csv_to_dict(
                    sCSV
                )
            else:
                print("Unrecognized CSV format!")
                # If this happens, investigate whats wrong with the data
                self.isUsableData = False
                break


    def __init__(
        self,
         id: str,
         category: str,
         originalCsvs: [str]
    ):
        self.id = id
        self.category = category
        self.__originalCSVs = originalCsvs
        self.taskSwitchingDataStructured = []
        self.posnerDataStructured = []
        self.goNoGoStructured = []
        self.simpleReactionStructured = []
        self.isUsableData: bool = True
        self.__serializeCSVs()

"""
Data mining
    1. Serialize raw CSV data into nice object collections.
"""
class DataLoader:
    # Stores things like 'ES', 'CAS' 'MOBA' etc...
    CATEGORIES = []
    ALL_CSVS = {

    }
    SUBJECT_DATA_STRUCTURED={}

    @staticmethod
    def load_categories():
        DataLoader.CATEGORIES = os.listdir(DATA_SET)

        for category in DataLoader.CATEGORIES:
            DataLoader.ALL_CSVS[category] = {}

    """
        Grabs all the CSVs and stores them into a temp dictionary for parsing later 
    """
    @staticmethod
    def find_all_csvs():

        for category in DataLoader.CATEGORIES:
            categoryFullPath = f"{DATA_SET}/{category}"
            print(f"{category} -- find CSVs.. @ path:  '{categoryFullPath}'")
            for path, subdirs, files in os.walk(categoryFullPath):
                for name in files:
                    fullPath = os.path.join(path, name)
                    subjectID = os.path.basename(path)
                    print(f"{fullPath} - for subject '{subjectID}'")


                    if(".csv" in fullPath):
                        if subjectID not in DataLoader.ALL_CSVS[category].keys():
                            DataLoader.ALL_CSVS[category][subjectID] = []

                        DataLoader.ALL_CSVS[category][subjectID].append(
                            fullPath
                        )
        print(DataLoader.ALL_CSVS)

        for category in DataLoader.ALL_CSVS.keys():
            print(f"{category} has {len(DataLoader.ALL_CSVS[category].keys())} participants so far")

    """
        Loop all CSV files, structure into objects we can work with later. 
    """
    @staticmethod
    def structure_all_csvs_as_objects():
        for category in DataLoader.ALL_CSVS.keys():
            DataLoader.SUBJECT_DATA_STRUCTURED[category] = {}
            for subjectId in DataLoader.ALL_CSVS[category].keys():
                DataLoader.SUBJECT_DATA_STRUCTURED[category][subjectId] = SubjectDataStructured (
                    id=subjectId,
                    category=category,
                    originalCsvs=DataLoader.ALL_CSVS[category][subjectId]
                )

        print("CSV Structure done")

    """
        Data loader 'main' function 
    """
    @staticmethod
    def load_and_serialize_all_data():
        DataLoader.load_categories()

        DataLoader.find_all_csvs()

        DataLoader.structure_all_csvs_as_objects()

"""
    Static collection of methods
        for extracting features from the raw CSV data set for the various experiments.
    Creates sets of feature vectors. For each experiment, gather the following for the feature vector set:
        - Simple Reaction time average (train/test)

        ## Go/no-go metrics
        - Go/No-go training - reaction time
        - Go/No-go testing - reaction time
        - No-go error - training
        - No-go error - testing

        ## Task switching
        - Switch cost avg train - A->A
        - Switch cost avg train - A->B
        - Switch cost avg test  - A->A
        - Switch cost avg test  - A->B

        ## Posner
        All of this crap:
        "avgValidCueResponseTimeTraining": (totalResponeTimesTrainingCorrectResponseAndValidCue / totalNumberTrainingCorrectResponseAndValidCue),
        "avgValidCueResponseTimeTesting": (totalResponeTimesTestingCorrectResponseAndValidCue / totalNumberTestingCorrectResponseAndValidCue),
        "avgInvalidCueResponseTimeTraining": (totalResponeTimesTrainingCorrectResponseAndInvalidCue / totalNumberTrainingCorrectResponseAndInvalidCue),
        "avgInvalidCueResponseTimeTesting": (totalResponeTimesTestingCorrectResponseAndInvalidCue / totalNumberTestingCorrectResponseAndInvalidCue),
        "totalInvalidCuesTesting": totalInvalidCuesTesting,
        "totalInvalidCuesTraining":totalInvalidCuesTraining,
        "percentageMissedInvalidCuesTraining": (incorrectResponseForUncuedTraining / totalInvalidCuesTraining),
        "percentageMissedInvalidCuesTesting": (incorrectResponseForUncuedTesting/ totalInvalidCuesTesting),
        "peakTestingValueValidCues": peakTestingValueValidCues,
        "peakTestingValueInvalidCues": peakTestingValueInvalidCues,
        "peakTrainingValueInvalidCues": peakTrainingValueInvalidCues,
        "peakTrainingValueValidCues": peakTrainingValueValidCues

"""
class FeatureExtraction:

    @staticmethod
    def extract_reaction_time_features():
        pass

    @staticmethod
    def extract_posner_features():
        pass

    @staticmethod
    def extract_goNoGo_features():
        pass

    @staticmethod
    def extract_task_switch_features():
        pass

    @staticmethod
    def extractFeatures():
        # TODO NEXT
        # -- Will create all needed feature vectors + label vector
        pass

"""  
    Naive bayes: 
    
    rom sklearn.model_selection import train_test_split
    from sklearn.naive_bayes import GaussianNB
    from sklearn.metrics import accuracy_score
    from sklearn.datasets import make_classification
    
    # Generate a synthetic dataset
    X, y = make_classification(n_samples=100, n_features=2, n_redundant=0, n_clusters_per_class=1, random_state=42)
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize Gaussian Naive Bayes model
    gnb = GaussianNB()
    
    -- !!!! TODO  REMEMBER OUTPUT MODEL TO FILE WHICH WE CAN USE LATER IN A WEB SERVICE 
    
    # Train the model
    gnb.fit(X_train, y_train)
    
    # Predict on the test set
    y_pred = gnb.predict(X_test)
    
    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy}") 

"""
class ModelTraining:
    pass


"""
TODO
"""
class ModelTesting:
    pass


DataLoader.load_and_serialize_all_data()

FeatureExtraction.extractFeatures()