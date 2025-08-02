# Model training and testing

# General Imports
import os
import csv
import sys, traceback

# Data science / Visualization libs
import pandas
from pandas.plotting import parallel_coordinates
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from mplcursors import cursor

# Globals
DATA_SET='/Users/zachmcfadden/Desktop/dev/tmp/smashStudyDataSet'
PLOTS_DIRECTORY="./tmp"

def errorStackTrace(e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    trace = traceback.format_exc()
    errorMessage = ("STACK TRACE ERROR :: " + str(e) + ".. Line number: " + str(
        exc_tb.tb_lineno) + "-- STACK TRACEBACK: " + str(trace))
    return errorMessage

# Util function for saving the plot to a file under './plots/'
def save_plot(plotName: str):
    # If dir isnt there, create it
    if not os.path.exists(PLOTS_DIRECTORY):
        print("Creating plots directory!")
        os.mkdir(PLOTS_DIRECTORY)

    print(f"Saving plot: {plotName}.png")
    plt.savefig(f"{PLOTS_DIRECTORY}{os.sep}{plotName}")

def printUnusableData():
    totalUnused = 0
    totalRecords = 0
    for category in DataLoader.SUBJECT_DATA_STRUCTURED.keys():
        for subjectId in DataLoader.SUBJECT_DATA_STRUCTURED[category].keys():
            sub: SubjectDataStructured = DataLoader.SUBJECT_DATA_STRUCTURED[category][subjectId]
            if sub.isUsableData == False:
                print(f"Following Subject datat not used: {sub.id}")
                totalUnused+=1
            totalRecords+=1
    print(f"Total Unused: {totalUnused}/{totalRecords}")

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
Simple utility enum for fetching data from the Feature vectors 
"""
class FeaturesLocation:
    avgErrorTesting = 0
    avgErrorTraining = 1
    goNoGoTrainingMean = 2
    goNoGoTestingMean = 3
    goTestingMin = 4
    goTrainingMi = 5
    avgTestingReactionTime = 6
    avgTrainingReactionTime = 7
    avgReactionTimeAcrossAllTrials = 8

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

    def __checkData(self):
        if len(self.taskSwitchingDataStructured) == 0 or \
            len(self.simpleReactionStructured) == 0 or \
            len(self.goNoGoStructured) == 0 or \
            len(self.posnerDataStructured) == 0:
            self.isUsableData = False

    # TODO - Add a 'reason' why the data is not usable (bad data format, outlier, etc..)
    def setNotUsable(self):
        self.isUsableData = False

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
        self.__checkData()

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
"""
class FeatureExtraction:

    # Holds all labels
    LABELS_VECTOR=[]

    # Holds all feature vectors
    FEATURES_VECTOR=[]

    @staticmethod
    def add_to_labels_vector(data: SubjectDataStructured):
        # Add objects category as the 'label'
        FeatureExtraction.LABELS_VECTOR.append(
            data.category
        )

    """
    FEATURES:
        * avgTrainingReactionTime - Average Reaction time during training set
        * avgTestingReactionTime - Average Reaction time during testing set
        * avgReactionTimeAcrossAllTrials - Average across all trials   
        
    Data Structure Reference:
            /*
                Ref: https://www.psytoolkit.org/experiment-library/deary_liewald.html
                1 - Test or trials 
                2 - training (1=training, 0=real data collection)
                3 - number of choices (1 in simple block, 4 in choice block)
                4 - time between response and next trial (between 1 and 3 seconds)
                5 - the x-coordinate of the target stimulus
                6 - the response time (ms)
                7 - status (1=correct, 2=error, 3=too slow)
            */
            "SimpleReaction" : [
                "TestOrTrial",
                "TrainingOrReal",
                "NumberOfChoices",
                "timeBetweenResponseAndNextTrial",
                "XCoordinateTargetStim",
                "ResponseTime",
                "StatusOfAnswer"
            ],
    """
    @staticmethod
    def extract_reaction_time_features(data: SubjectDataStructured) -> [int]:
        if len(data.simpleReactionStructured) == 0:
            # throw this record out
            return None

        totalTrainingRecords: int = 0
        totalTestingRecords: int = 0
        totalTrials: int = 0

        totalTrainingTime: int = 0
        totalTestingTime: int = 0
        totalTime: int = 0

        for reactionTimeData in data.simpleReactionStructured:

            if reactionTimeData["TrainingOrReal"] == '1':
                totalTrainingRecords+=1
                totalTrainingTime+=float(
                    reactionTimeData["ResponseTime"]
                )
            else:
                totalTestingRecords+=1
                totalTestingTime+=float(
                    reactionTimeData["ResponseTime"]
                )
            totalTrials+=1
            totalTime+=float(
                reactionTimeData["ResponseTime"]
            )

        avgTestingReactionTime=(
            totalTestingTime / totalTestingRecords
        )

        avgTrainingReactionTime = (
            totalTrainingTime / totalTrainingRecords
        )

        avgReactionTimeAcrossAllTrials = (
            totalTime / totalTrials
        )

        return [
            avgTestingReactionTime,
            avgTrainingReactionTime,
            avgReactionTimeAcrossAllTrials
        ]


    """
        TODO - Posner features
        
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
    @staticmethod
    def extract_posner_features(data: SubjectDataStructured)-> [int]:
        totalNumberTrainingCorrectResponseAndValidCue = 0
        totalResponeTimesTrainingCorrectResponseAndValidCue = 0

        totalResponeTimesTestingCorrectResponseAndValidCue = 0
        totalNumberTestingCorrectResponseAndValidCue = 0

        totalResponeTimesTrainingCorrectResponseAndInvalidCue = 0
        totalNumberTrainingCorrectResponseAndInvalidCue = 0

        totalResponeTimesTestingCorrectResponseAndInvalidCue = 0
        totalNumberTestingCorrectResponseAndInvalidCue = 0

        totalInvalidCuesTesting = 0
        totalInvalidCuesTraining = 0

        incorrectResponseForUncuedTraining = 0
        incorrectResponseForUncuedTesting = 0

        peakTestingValueValidCues = None
        peakTestingValueInvalidCues = None

        peakTrainingValueInvalidCues = None
        peakTrainingValueValidCues = None

        for posnerRecord in data.posnerDataStructured:

            isValidCue=(posnerRecord["CueValidity"] != "invalid")
            isUncued=(posnerRecord["CuedOrUncued"] == "uncued")
            isBadStatusOfAnswer=(posnerRecord["StatusOfAnswer"] != '1')
            isValidCueAndGoodStatus=(isValidCue and (not isBadStatusOfAnswer))
            isInvalidCueAndGoodStatus=(not isValidCue and (not isBadStatusOfAnswer))
            isIncorrectResponseForUncued=(isUncued and isBadStatusOfAnswer)


            responsetime=(
                float(
                    posnerRecord["ResponsetimeMS"]
                )
            )

            # Training processing
            if posnerRecord["TestOrTraining"] == "cueingBlockTraining":
                if isValidCueAndGoodStatus:
                    totalNumberTrainingCorrectResponseAndValidCue+=1
                    totalResponeTimesTrainingCorrectResponseAndValidCue+=responsetime
                elif isInvalidCueAndGoodStatus:
                    totalNumberTrainingCorrectResponseAndInvalidCue += 1
                    totalResponeTimesTrainingCorrectResponseAndInvalidCue += responsetime

                if not isValidCue:
                    totalInvalidCuesTraining += 1

                    if peakTrainingValueInvalidCues == None or peakTrainingValueInvalidCues > responsetime:
                        peakTrainingValueInvalidCues = responsetime
                else:
                    if peakTrainingValueValidCues == None or peakTrainingValueValidCues > responsetime:
                        peakTrainingValueValidCues = responsetime

                if isIncorrectResponseForUncued:
                    incorrectResponseForUncuedTraining += 1
            # Testing processing
            else:
                if isValidCueAndGoodStatus:
                    totalNumberTestingCorrectResponseAndValidCue += 1
                    totalResponeTimesTestingCorrectResponseAndValidCue += responsetime
                elif isInvalidCueAndGoodStatus:
                    totalNumberTestingCorrectResponseAndInvalidCue += 1
                    totalResponeTimesTestingCorrectResponseAndInvalidCue += responsetime

                if not isValidCue:
                    totalInvalidCuesTesting += 1
                    if peakTestingValueInvalidCues == None or peakTestingValueInvalidCues > responsetime:
                        peakTestingValueInvalidCues = responsetime
                else:
                    if peakTestingValueValidCues == None or peakTestingValueValidCues > responsetime:
                        peakTestingValueValidCues = responsetime

                if isIncorrectResponseForUncued:
                    incorrectResponseForUncuedTesting += 1

        avgValidCueResponseTimeTraining =  (totalResponeTimesTrainingCorrectResponseAndValidCue / totalNumberTrainingCorrectResponseAndValidCue)
        avgInvalidCueResponseTimeTraining = (totalResponeTimesTrainingCorrectResponseAndInvalidCue / totalNumberTrainingCorrectResponseAndInvalidCue)

        avgValidCueResponseTimeTesting = (totalResponeTimesTestingCorrectResponseAndValidCue / totalNumberTestingCorrectResponseAndValidCue)
        avgInvalidCueResponseTimeTesting = (totalResponeTimesTestingCorrectResponseAndInvalidCue / totalNumberTestingCorrectResponseAndInvalidCue)

        percentageMissedInvalidCuesTraining = (incorrectResponseForUncuedTraining / totalInvalidCuesTraining)
        percentageMissedInvalidCuesTesting = (incorrectResponseForUncuedTesting/ totalInvalidCuesTesting)

        return [
            avgValidCueResponseTimeTraining,
            avgValidCueResponseTimeTesting,
            avgInvalidCueResponseTimeTesting,
            avgInvalidCueResponseTimeTraining,
            percentageMissedInvalidCuesTraining,
            percentageMissedInvalidCuesTesting,
            peakTestingValueInvalidCues,
            peakTrainingValueInvalidCues,
            peakTestingValueValidCues,
            peakTrainingValueValidCues
        ]


    """
        Table Refer:
            /*
              1 - Name of task: go or nogo / training or trial
              2 - The response speed (in nogo trials, this is 2000, the timeout)
              3 - The error status (0 is correct, 1 is error)
            */
            "GoNoGo" : [
                "GoNoGoAndTestOrTrial", 
                 - 'goGoNoGoTraining', goGoNoGoTesting, nogoGoNoGoTraining, nogoGoNoGoTesting
                "ResponseTimeMs", 
                "ErrorStatus"
            ],
            
            // Craft the CSV 
            var finalData = {
                // Errors are on no go 
                "avgErrorTraining": (errorCounterTraining / NoGoTrials),
                "avgErrorTesting": (errorCounterTesting / NoGoTrials),
                "goNoGoTestingMinResponseTimeMS": goNoGoTestingMin,
                "goNoGoTrainingMinResponseTimeMS": goNoGoTrainingMin,
                "goNoGoTrainingMean": (goNoGoTrainingTotal / goNoGoTrainingTrials),
                "goNoGoTestingMean": (goNoGoTestingTotal / goNoGoTestingTrials)
            }
    """
    @staticmethod
    def extract_goNoGo_features(data: SubjectDataStructured)-> [int]:
        # Count errors for no go's
        totalNoGoTrialsTraining = 0
        totalNoGoTrialsTesting = 0
        totalNoGoTrainingErrors=0
        totalNoGoTestingErrors=0


        # Get Avg for training/testing go's
        totalGoTrialsTesting = 0
        totalGoTrialsTraining = 0
        totalGoResponseTimeTesting = 0
        totalGoResponseTimeTraining = 0

        # Get peaks (min) response time for go's
        goTestingMin = None
        goTrainingMin = None

        for goNoGoRecord in data.goNoGoStructured:
            """
            "GoNoGoAndTestOrTrial", 
                - 'goGoNoGoTraining', goGoNoGoTesting, nogoGoNoGoTraining, nogoGoNoGoTesting
            """
            if goNoGoRecord["GoNoGoAndTestOrTrial"] == "nogoGoNoGoTraining":
                totalNoGoTrialsTraining+=1
                if goNoGoRecord["ErrorStatus"] == "1":
                    totalNoGoTrainingErrors+=1
            elif goNoGoRecord["GoNoGoAndTestOrTrial"] == "goGoNoGoTesting":
                totalGoTrialsTesting+=1

                responeTime = float(
                    goNoGoRecord["ResponseTimeMs"]
                )

                totalGoResponseTimeTesting+=responeTime

                if goTestingMin == None or goTestingMin > responeTime:
                    goTestingMin = responeTime
            elif goNoGoRecord["GoNoGoAndTestOrTrial"] == "nogoGoNoGoTesting":
                totalNoGoTrialsTesting+= 1
                if goNoGoRecord["ErrorStatus"] == "1":
                    totalNoGoTestingErrors += 1
            else:
                # Inferred training go trials
                totalGoTrialsTraining += 1
                responeTime = float(
                    goNoGoRecord["ResponseTimeMs"]
                )

                totalGoResponseTimeTraining += responeTime


                if goTrainingMin == None or goTrainingMin > responeTime:
                    goTrainingMin = responeTime

        avgErrorTraining = (
            totalNoGoTrainingErrors / totalNoGoTrialsTraining
        )

        avgErrorTesting = (
            totalNoGoTestingErrors / totalNoGoTrialsTesting
        )

        goNoGoTrainingMean = (
            totalGoResponseTimeTraining / totalGoTrialsTraining
        )

        goNoGoTestingMean = (
            totalGoResponseTimeTesting / totalGoTrialsTesting
        )

        return [
            avgErrorTesting,
            avgErrorTraining,
            goNoGoTrainingMean,
            goNoGoTestingMean,
            goTestingMin,
            goTrainingMin
        ]


    """
        ## Task switching
        - Switch cost avg train - A->A
        - Switch cost avg train - A->B
        - Switch cost avg test  - A->A
        - Switch cost avg test  - A->B
    """
    @staticmethod
    def extract_task_switch_features(data: SubjectDataStructured) -> [int]:
        """
        // Algo:
        // - filter incorrect SWITCH trials
        // - calculate on switch-repeat pairs
        // -- 1=task switch , 0=task repeat 'taskSwitchOrTaskRepeat' column
        // -- status (1=correct, 2=error, 3=too slow)
        :param data:
        :return:
        """

        trainingTotalSwitchCost = 0
        trainingTotalSwitchEvents = 0
        trainingTotalSwitchErrors = 0

        testingTotalSwitchCost = 0
        testingTotalSwitchEvents = 0
        testingTotalSwitchErrors = 0

        """
            /*
              1 - letter | numbers | mixed and TestOrTrial
              2 - position of stimulus 1,2,3,4 (top left, top right, bottom right, bottom left
              3 - tasktype (1 or 2)
              4 - the letter stimulus
              5 - the number stimulus
              6 - type of block (1=just task 1; 2=just task 2; 0=both tasks mixed)
              7 - 1=task switch , 0=task repeat
              8 - status (1=correct, 2=error, 3=too slow)
              9 - response time (ms)
              10 - total time (response time + button release time)
            */
            "TaskSwitching" : [
                "TaskSwitchTypeAndTestOrTrial",
                "position",
                "taskType",
                "letterStimulus",
                "numberStimulus",
                "typeOfBlock",
                "taskSwitchOrTaskRepeat",
                "status",
                "responseTimeMs",
                "totalTimeMs"
            ],
        """
        i = 0
        for taskSwitchingData in data.taskSwitchingDataStructured:
            if "Training" in taskSwitchingData["TaskSwitchTypeAndTestOrTrial"]:
                # Task Switch
                if taskSwitchingData["taskSwitchOrTaskRepeat"] == '1':
                    trainingTotalSwitchEvents += 1

                    if taskSwitchingData["status"] == "1":
                        trainingTotalSwitchCost += (
                                float(data.taskSwitchingDataStructured[i]["responseTimeMs"]) -
                                float(data.taskSwitchingDataStructured[i+1]["responseTimeMs"])
                        )
                    else:
                        trainingTotalSwitchErrors+=1

                        # Punish total switch cost for errors
                        trainingTotalSwitchCost+=(float(data.taskSwitchingDataStructured[i+1]["responseTimeMs"]) * .25)
            else:
                # Task Switch
                if taskSwitchingData["taskSwitchOrTaskRepeat"] == '1':
                    testingTotalSwitchEvents += 1
                    if taskSwitchingData["status"] == "1":
                        testingTotalSwitchCost += (
                                float(data.taskSwitchingDataStructured[i]["responseTimeMs"]) -
                                float(data.taskSwitchingDataStructured[i+1]["responseTimeMs"])
                        )
                    else:
                        testingTotalSwitchErrors+=1

                        # Punish total switch cost for errors
                        testingTotalSwitchCost += (
                                float(data.taskSwitchingDataStructured[i + 1]["responseTimeMs"]) * .25
                        )
            # Used for [N] - [N-1]
            i+=1

        # Train data
        avgTrainingError = (
            trainingTotalSwitchErrors / trainingTotalSwitchEvents
        )
        trainingSwitchCost = (
            trainingTotalSwitchCost / trainingTotalSwitchEvents
        )

        # Test Data
        avgTestingError = (
            testingTotalSwitchErrors / testingTotalSwitchEvents
        )
        testingSwitchCost = (
            testingTotalSwitchCost / testingTotalSwitchEvents
        )

        return [
            avgTrainingError,
            trainingSwitchCost,
            avgTestingError,
            testingSwitchCost
        ]


    """
        Main entry point for featur extraction. Creates label AND feature vectors. 
    """
    @staticmethod
    def extractFeatures():
        print("Begin Feature Extraction")
        for category in DataLoader.SUBJECT_DATA_STRUCTURED.keys():
            for subjectId in DataLoader.SUBJECT_DATA_STRUCTURED[category].keys():
                subjectData: SubjectDataStructured = DataLoader.SUBJECT_DATA_STRUCTURED[category][subjectId]
                if subjectData.isUsableData:
                    try:
                        featuresHolder = []
                        # Feature Extraction. Implicitly adds to
                        featuresHolder.extend(
                            FeatureExtraction.extract_goNoGo_features(subjectData)
                        )
                        featuresHolder.extend(
                            FeatureExtraction.extract_reaction_time_features(subjectData)
                        )
                        featuresHolder.extend(
                            FeatureExtraction.extract_posner_features(subjectData)
                        )
                        featuresHolder.extend(
                            FeatureExtraction.extract_task_switch_features(subjectData)
                        )

                        # Creates a 2-Dimensional Array
                        FeatureExtraction.FEATURES_VECTOR.append(
                            featuresHolder
                        )

                        FeatureExtraction.add_to_labels_vector(subjectData)
                    except Exception as e:
                        print(f"Issue parsing this subject: {errorStackTrace(e)}")
                        print("This data is not usable.")
                        subjectData.setNotUsable()

        print("Feature Extraction complete")

class FeaturesVisualizations:

    @staticmethod
    def create_visualizations():
        FeaturesVisualizations.reaction_time_parallel_coordinate_plot()

        FeaturesVisualizations.go_no_go_stacked_bar_plot()

        FeaturesVisualizations.task_switching_mosaic_plot()

    @staticmethod
    def reaction_time_parallel_coordinate_plot():
        print("Creating reaction time parallel coordinate plot")
        # Grab the testing/training/total averages and average them per category

        parralelCoordinatePlotArray = []
        parralelCoordinatePlotDict = {}
        i = 0
        for featureData in FeatureExtraction.FEATURES_VECTOR:
            category = FeatureExtraction.LABELS_VECTOR[i]
            avgTrain = featureData[FeaturesLocation.avgTrainingReactionTime]
            avgTest = featureData[FeaturesLocation.avgTestingReactionTime]
            totalReact = featureData[FeaturesLocation.avgReactionTimeAcrossAllTrials]

            if category not in parralelCoordinatePlotDict.keys():
                parralelCoordinatePlotDict[category] = {}
                parralelCoordinatePlotDict[category]["totalTrain"] = 0
                parralelCoordinatePlotDict[category]["totalTest"] = 0
                parralelCoordinatePlotDict[category]["totalReact"] = 0
                parralelCoordinatePlotDict[category]["totalRecords"] = 0

            parralelCoordinatePlotDict[category]["totalTrain"] += avgTrain
            parralelCoordinatePlotDict[category]["totalTest"] += avgTest
            parralelCoordinatePlotDict[category]["totalReact"] += totalReact
            parralelCoordinatePlotDict[category]["totalRecords"] += 1
            i+=1


        # TODO -- Create plot w/ and without non-gamers
        # del parralelCoordinatePlotDict[DataCategories.NG]

        for category in parralelCoordinatePlotDict.keys():

            parralelCoordinatePlotArray.append(
                [
                    category,
                    parralelCoordinatePlotDict[category]["totalTrain"] / parralelCoordinatePlotDict[category]["totalRecords"],
                    parralelCoordinatePlotDict[category]["totalTest"] / parralelCoordinatePlotDict[category]["totalRecords"],
                    parralelCoordinatePlotDict[category]["totalReact"] / parralelCoordinatePlotDict[category]["totalRecords"]
                ]
            )



        parralelCoordinatePlotDf = pandas.DataFrame(
            parralelCoordinatePlotArray,
            columns=[
                "category",
                "avgTrain",
                "avgTest",
                "totalReact"
            ]
        )

        # parralelCoordinateDF = parralelCoordinatePlotDf.sort_values(
        #     by=["mean"],
        #     ascending=False
        # )

        plt.title('Reaction times by subject category', size=15, weight="bold")
        plt.ylabel("Reaction time (ms)", size=15, weight="bold")

        # # Setup parralel coordinates via DF with the legend collumn attached to 'key'
        pylab.rcParams.update(
            {
                # Adjust top display text
                "ytick.labelsize": 10,
                "xtick.labelsize": 10
            }
        )

        ax = parallel_coordinates(
            parralelCoordinatePlotDf,
            "category",
            axvlines=True,
        )
        ax.grid(True)

        # Adjust xaxix and yaxis ticket size for readability
        ax.xaxis.tick_top()
        ax.xaxis.set_tick_params(
            labelsize=20
        )
        ax.yaxis.set_tick_params(
            labelsize=20
        )
        #
        # # Attach legend with anchor to push it outside of the graph
        # # This keeps the graph less cluttered
        plt.legend(
            parralelCoordinatePlotDf["category"],
            loc='upper left',
            prop={
                'weight': 'bold',
                'size': 11.1
            },
            ncol=3
        )
        ap = [{'horizontalalignment': 'right', 'verticalalignment': 'top',
               'anncoords': 'offset points', 'position': (50, 50)}]
        cursor(hover=True, annotation_positions=ap)
        save_plot("parallel")
        plt.show()
        return


    @staticmethod
    def go_no_go_stacked_bar_plot():
        pass

    @staticmethod
    def task_switching_mosaic_plot():
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

def main():
    try:
        # Data mining step. Extract and structure all data
        DataLoader.load_and_serialize_all_data()

        # Feature Extraction step. Format and extract all relevant feature vectors and label data.
        FeatureExtraction.extractFeatures()

        # Simple Report on what data was actually usable, vs thrown out.
        printUnusableData()

        # Create some visualizations from preliminary data
        FeaturesVisualizations.create_visualizations()

    except Exception as e:
        print(f"Exception occurred: {errorStackTrace(e)}")
        raise e

if __name__ == "__main__":
    main()