/**
  * Author: Zach McFadden
  * Date: July 8, 2024
  * Simple utility script written on top of the compiled psytoolkit HTML experiments
  * Effectively what this does is listen to existing psytoolkit events (specifically showing the data).
  * Once the data is ready to show, we simply take the data and output it to a CSV file. 
  * This operation runs in the background:
  *  1. the beginning (to bootstrap the listener)
  *  2. At the end once the data is ready to show (this will trigger the listener at the end of the experiment)
  * 
  * Update: July 23, 2024 - Auto-full screen, CSV File named per experiment, X-Axis collumn names 
  * Update: December 6, 2024:
    - Add Versioning to HTML Title
    - Automated stats upon experiment completion 
  * Update: January 3, 2025 - fix automated stats bug?
  * Update: February 4th, 2025 - Switch cost automated calculation.
  * Update: February 8th, 2025 - Make trials configurable (ex demo site). 
    - Go/No-go automated status enhancement. Deprecate old automated stats method 
  * Update: February 8th, 2025 - Posner Stats 
  * Update: August 1st, 2025 - Japanese Translations (specifically the otter)
*/ 

// Semantic versioning for the app 
VERSION="1.0.7"

// Store global vars 
var GLOBAL_VARIABLE_STASH = {}

// Trial variables 
var TOTAL_TRIALS_VAR = 60 // used by posner and task switch
var SimpleReactionTrain = 10 // reaction time vars
var SimpleReactionTest = 20 
// go/no-go vars
var GoTrials = 20
var NoGoTrials = 5 
var isDemoSite = false 

/*
 * Simple utility function for downloading a document of a particular content type.
*/
function downloadBlob(content, filename, contentType) {
  // Create a blob
  var blob = new Blob([content], { type: contentType });
  var url = URL.createObjectURL(blob);

  // Create a link to download it
  var pom = document.createElement('a');
  pom.href = url;
  pom.setAttribute('download', filename);
  pom.click();
}


/**
 * Generates a Formatted, and (hopefully) unique file name, based on the current date.
 *
 */
function generateOutputFileName(baseName) {
  return  `${baseName}_${new Date().toLocaleString().replaceAll("/","-").replaceAll(" ","_")}.csv`
}

/*
 * Converts space separated data into a CSV string. 
 *  Passes to downloadBlob to automatically download the file 
 *
 */
function outputDataToCSV(data, outputFileName) {
    
    // Update - 8/1/24 -- need to trim extra white space to 1! 
    // Then split by single white space into a CSV 
    var dataToWrite = data.replace(/\s{2,}/g, ' ').replaceAll(' ', ',')
    console.log(dataToWrite)

    downloadBlob(
      dataToWrite, 
      generateOutputFileName(outputFileName), 
      'text/csv;charset=utf-8;'
    )  
}

// Contains mapping from experiments --> column names 
function getExperimentToColumnNamesMap(experimentName){
  var experimentToColumnNamesMapping = {

    /*
      1 - Name of task: go or nogo / training or trial
      2 - The response speed (in nogo trials, this is 2000, the timeout)
      3 - The error status (0 is correct, 1 is error)
    */
    "GoNoGo" : [
        "GoNoGoAndTestOrTrial", 
        "ResponseTimeMs", 
        "ErrorStatus"
    ],
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
    /*
    Ref: https://www.psytoolkit.org/experiment-library/cueing.html
      1 - Test or training data
      2 - cue position (cueleft, cueright)
      3 - target position (targetleft, targetright)
      4 - cue validity (cued, uncued)
      5 - cued or uncued 
      6 - cue validity as number (1=cued, 0=uncued)
      7 - Response time (ms)
      8 - Status (1=correct, 2=wrong, 3=timeout)
    */ 
    "PosnerCue": [
      "TestOrTraining",
      "CuePosition",
      "TargetPosition",
      "CueValidity",
      "CuedOrUncued",
      "CueValidityAsNumber",
      "ResponsetimeMS",
      "StatusOfAnswer"
    ],
  }

  return experimentToColumnNamesMapping[experimentName]
}

/**
  * Get total trials for the experiment 
**/
function getTotalTrials(experimentName){
  if(experimentName == "TaskSwitching" || experimentName == "PosnerCue"){
    console.log(`Total Trials: ${TOTAL_TRIALS_VAR}`)
    return TOTAL_TRIALS_VAR
  } else if(experimentName == "SimpleReactionTrain"){
    return SimpleReactionTrain
  } else if(experimentName == "SimpleReactionTest"){
    return SimpleReactionTest
  } else if(experimentName == "GoTrials"){
    return GoTrials
  } else if(experimentName == "NoGoTrials"){
    return NoGoTrials
  }
}

/**
  * Parse relevant HTTP args 
  *
**/
function parseHttpArgs(experimentName){
  var selfReferenceURL = new URL(window.location.href);

  var trials = selfReferenceURL.searchParams.get("totalTrials")
  if(trials != null) {
    TOTAL_TRIALS_VAR = parseInt(trials)
  } 

  var simpleReactionTrain = selfReferenceURL.searchParams.get("simpleReactionTrain")
  if(simpleReactionTrain != null){
     SimpleReactionTrain = parseInt(simpleReactionTrain)
     console.log(SimpleReactionTrain)
  }

  var simpleReactionTest = selfReferenceURL.searchParams.get("simpleReactionTest")
  if(simpleReactionTest != null){
    SimpleReactionTest = parseInt(simpleReactionTest)
    console.log(SimpleReactionTest)
  }

  var goTrials = selfReferenceURL.searchParams.get("GoTrials")
  if(goTrials != null){
    GoTrials = goTrials
  }

  var noGoTrials = selfReferenceURL.searchParams.get("NoGoTrials")
  if(noGoTrials != null){
    NoGoTrials = noGoTrials
  }

  var isDemo = selfReferenceURL.searchParams.get("isDemoSite")
  if(isDemo != null){
    isDemoSite = true 
  }

}

/**
  * Initialize relevant global vars 
*/ 
function initGlobalVariableStash(experimentName){
    console.log("Global variables stash init")
    if(experimentName == "PosnerCue"){
      TOTAL_TRIALS_VAR = 13 // 13 for posner 
    }
    parseHttpArgs(experimentName)
}


/**
  * Convert poorly formatted output data to a hash table
  *     -- Easier to work with programatically
**/
function serializeOutputDataToTable(data, experimentName){
    var dataFormatted = data.split("\n")
    var rData = {
        // Place data here
    }

    // KEYS OF THE HASH TABLE
    var columnNameMapping = getExperimentToColumnNamesMap(experimentName)

    // Initialize dictionary keys
    for(var i = 0; i < columnNameMapping.length; i++){
        rData[columnNameMapping[i]] = []
    }

    // Iterate each data entry
    for(var i = 0; i < dataFormatted.length; i++){
       var formatLineAsArray = dataFormatted[i].replace(/\s{2,}/g, ' ').split(" ")

       // Iterate each column
       for(var j = 0; j < formatLineAsArray.length; j++){
            rData[columnNameMapping[j]].push(formatLineAsArray[j])
       }
    }

    return rData
}

/**
  * Calculate switch cost based on next trial
**/
function isSwitchTrial(trial){
    // -- 1=task switch , 0=task repeat 'taskSwitchOrTaskRepeat' column
    return trial == "1"
}

function isTrialCorrect(trial){
    // -- status (1=correct, 2=error, 3=too slow)
    return trial == "1"
}

function initialize2DArray(rows, cols) {
  return Array.from({ length: rows }, () => Array(cols).fill(null));
}

/**
  * Calculates the 'switch cost' of a task switching experiment
  * If the current task is 'even' (say N=2),
  *     -- we can calculate the switch cost as the difference between val(N) - (val(N-1))
  *
*/
function calculateSwitchCost(data){
    console.log("Calculate switch cost...")
    console.log(data)
    var dataSerialized = serializeOutputDataToTable(
        data,
        "TaskSwitching"
    )

    console.log(dataSerialized)

    var switchCosts = {

    }

    // populate the table
    for(var i = 0; i < dataSerialized["TaskSwitchTypeAndTestOrTrial"].length; i++){
        if(dataSerialized["TaskSwitchTypeAndTestOrTrial"][i] in switchCosts == false){
            switchCosts[dataSerialized["TaskSwitchTypeAndTestOrTrial"][i]]={
                mean: 0
            }
        }
    }

    // Algo:
    // - filter incorrect SWITCH trials
    // - calculate on switch-repeat pairs
    // -- 1=task switch , 0=task repeat 'taskSwitchOrTaskRepeat' column
    // -- status (1=correct, 2=error, 3=too slow)
    for(var i = 0; i < dataSerialized["responseTimeMs"].length; i++){
        if(isSwitchTrial(dataSerialized["taskSwitchOrTaskRepeat"][i])
        ){
            // check [N+1] - (N)
            var keyToUse = `${i}_cost`
            if(isTrialCorrect(dataSerialized["status"][i])){
            switchCosts[dataSerialized["TaskSwitchTypeAndTestOrTrial"][i]][keyToUse] = parseFloat(dataSerialized["responseTimeMs"][i] - dataSerialized["responseTimeMs"][i+1])
            } else {
                switchCosts[dataSerialized["TaskSwitchTypeAndTestOrTrial"][i]][keyToUse] = "INCORRECT"
            }
        }
    }

    // Gather the mean values
    for (const [key, value] of Object.entries(switchCosts)) {
        console.log(`${key}: ${value}`);
        var total = 0
        var numberOfEntries = 0

        for (const [testEntryKey, testEntryValue] of Object.entries(switchCosts[key])) {
          console.log(`${testEntryKey}: ${testEntryValue}`);


          if(testEntryKey == "mean"){
            continue
          } else {
             if(!isNaN(switchCosts[key][testEntryKey])){
                numberOfEntries+=1
                total+= switchCosts[key][testEntryKey]
             }
          }
        }
        console.log(`${total} vs # entries ${numberOfEntries}`)
        switchCosts[key]["mean"] = (total / numberOfEntries)
    }

    // cache old map
    var copyOfData = JSON.parse(JSON.stringify(switchCosts));

    // Out dict to a CSV
    var statsCsvName = "TaskSwitching_stats"
    var csv = initialize2DArray(100,100)
    // Create mean columns first and remove from map
    var columnPointer = 0
    var rowPointer = 0

    // Initialize header first
    for (const key of Object.keys(switchCosts)) {
        var columnName = `${key}_mean`
        csv[rowPointer][columnPointer] = columnName
        columnPointer+=1
    }

    rowPointer+=1
    columnPointer=0
    for (const key of Object.keys(switchCosts)) {
        console.log(switchCosts[key]['mean'])
        csv[rowPointer][columnPointer] = switchCosts[key]['mean']
        columnPointer+=1
        delete switchCosts[key]['mean']
    }

    rowPointer = 0
    // Now create columns for non-mean values
    for (const key of Object.keys(switchCosts)) {
        var columnName = `${key}_switchCosts`
        csv[rowPointer][columnPointer] = columnName
        rowPointer+=1
        for(const trialKey of Object.keys(switchCosts[key])){
            csv[rowPointer][columnPointer] = switchCosts[key][trialKey]
            rowPointer+=1
        }
        rowPointer=0
        columnPointer+=1

    }

    console.log("csv...")
    console.log(csv)
    var finalCsvString = ""
    // Create the final CSV string
    for(var i = 0; i < csv.length; i++){
        for(var j = 0; j < csv[i].length; j++){
            if(csv[i][j] != null){
                finalCsvString+=`${csv[i][j]},`
            } else {
                finalCsvString+= ","
            }
        }
        // new line per row
        finalCsvString+="\n"
    }
    downloadBlob(
        finalCsvString,
        generateOutputFileName(statsCsvName),
        'text/csv;charset=utf-8;'
    )

    return copyOfData
}


function isErrorStatus(status){
  return status == "1"
}

/**
  * Automated Stats calculator for Go/No-go 
**/ 
function calculateGoNoGo(data) {
  var dataSerialized = serializeOutputDataToTable(
      data,
      "GoNoGo"
  )

  var goNoGoTrainingTotal = 0 
  var goNoGoTrainingTrials = 0 
  var goNoGoTrainingMin = null 

  var goNoGoTestingTotal = 0
  var goNoGoTestingTrials = 0 
  var goNoGoTestingMin = null 

  // Count errors and divide by # of noGo
  var errorCounterTraining = 0
  var errorCounterTesting = 0


  for(var i = 0; i < dataSerialized["ResponseTimeMs"].length; i++){
    console.log(dataSerialized["ResponseTimeMs"][i])
    var responseTimeParsed = parseFloat(dataSerialized["ResponseTimeMs"][i])

    if(dataSerialized["GoNoGoAndTestOrTrial"][i] == '"goGoNoGoTraining"'){
      goNoGoTrainingTotal+=responseTimeParsed
      goNoGoTrainingTrials+=1
      if(goNoGoTrainingMin == null || responseTimeParsed < goNoGoTrainingMin){
        goNoGoTrainingMin = responseTimeParsed
      }
    } else if(dataSerialized["GoNoGoAndTestOrTrial"][i] == '"goGoNoGoTesting"'){
      goNoGoTestingTotal+=responseTimeParsed
      goNoGoTestingTrials+=1
      if(goNoGoTestingMin == null || responseTimeParsed < goNoGoTestingMin){
        goNoGoTestingMin = responseTimeParsed
      }
    } else if(dataSerialized["GoNoGoAndTestOrTrial"][i] == '"nogoGoNoGoTraining"') {
      if(isErrorStatus(dataSerialized["ErrorStatus"][i])){
        errorCounterTraining+=1
      }
    } else if(dataSerialized["GoNoGoAndTestOrTrial"][i] == '"nogoGoNoGoTesting"'){
      if(isErrorStatus(dataSerialized["ErrorStatus"][i])){
        errorCounterTesting+=1
      }
    } else {
      console.log("Skip?")
    }

  }

  // Craft the CSV 
  var finalData = {
    "avgErrorTraining": (errorCounterTraining / NoGoTrials),
    "avgErrorTesting": (errorCounterTesting / NoGoTrials),
    "goNoGoTestingMinResponseTimeMS": goNoGoTestingMin,
    "goNoGoTrainingMinResponseTimeMS": goNoGoTrainingMin,
    "goNoGoTrainingMean": (goNoGoTrainingTotal / goNoGoTrainingTrials),
    "goNoGoTestingMean": (goNoGoTestingTotal / goNoGoTestingTrials)
  }

  var csv = "avgErrorTraining, avgErrorTesting, goNoGoTestingMinResponseTimeMS, goNoGoTrainingMinResponseTimeMS, goNoGoTrainingMean, goNoGoTestingMean\n"
  csv    += `${finalData["avgErrorTraining"]},${finalData["avgErrorTesting"]},${finalData["goNoGoTestingMinResponseTimeMS"]},${finalData["goNoGoTrainingMinResponseTimeMS"]},${finalData["goNoGoTrainingMean"]},${finalData["goNoGoTestingMean"]},` 

  downloadBlob(
      csv,
      generateOutputFileName("GoNoGoStats"),
      'text/csv;charset=utf-8;'
  )

  return finalData
}

function countTowardCues(CueValidityAsNumber, StatusOfAnswer){
  console.log(CueValidityAsNumber)
  console.log(StatusOfAnswer)

  return parseInt(CueValidityAsNumber) == 1 && parseInt(StatusOfAnswer) == 1
}

function countTowardInvalidCues(CueValidityAsNumber, StatusOfAnswer){
  return parseInt(CueValidityAsNumber) == 0 && parseInt(StatusOfAnswer) == 1
}

function countTowardIncorrectOnInvalidCues(CueValidityAsNumber, StatusOfAnswer){
  return parseInt(CueValidityAsNumber) == 0 && parseInt(StatusOfAnswer) != 1  
}

function calculatePosnerCueStats(data){
  var dataSerialized = serializeOutputDataToTable(data, "PosnerCue")
  // Cue block training and testing means (response time for CueValidityAsNumber=1 && StatusOfAnswer=1)
  var totalCues = 0
  var sumCueResponseTimes = 0

  var totalInvalidCues = 0 
  var sumInvalidCueResponseTimes = 0 

  var totalIncorrectOnInvalidCues = 0 
  console.log(dataSerialized)
  for(var i = 0; i < dataSerialized["ResponsetimeMS"].length; i++){
    console.log(dataSerialized['CueValidityAsNumber'][i])
    console.log(dataSerialized['StatusOfAnswer'][i])

    var responseTimeParsed = parseFloat(dataSerialized["ResponsetimeMS"][i])
    console.log(responseTimeParsed)
    if(countTowardCues(dataSerialized['CueValidityAsNumber'][i],dataSerialized['StatusOfAnswer'][i])){
        console.log("cue count")
        totalCues+=1
        sumCueResponseTimes+=responseTimeParsed
    } else if(countTowardInvalidCues(dataSerialized['CueValidityAsNumber'][i],dataSerialized['StatusOfAnswer'][i])){
        console.log("Count invalid cue")
        totalInvalidCues+=1
        sumInvalidCueResponseTimes+=responseTimeParsed
    } else if(countTowardIncorrectOnInvalidCues(dataSerialized['CueValidityAsNumber'][i],dataSerialized['StatusOfAnswer'][i])){
        totalIncorrectOnInvalidCues+=1
    } else {
      console.log("skip")
    }
  }

  console.log(sumCueResponseTimes)
  console.log(sumInvalidCueResponseTimes)

  var finalData = {
    "avgValidCueResponseTime": (sumCueResponseTimes / totalCues),
    "avgInvalidCueResponseTime": (sumInvalidCueResponseTimes / totalInvalidCues),
    "percentageMissedInvalidCues": (totalIncorrectOnInvalidCues / totalInvalidCues)
  }


  var csv = "avgValidCueResponseTime, avgInvalidCueResponseTime, percentageMissedInvalidCues\n"
  csv    += `${finalData["avgValidCueResponseTime"]},${finalData["avgInvalidCueResponseTime"]},${finalData["percentageMissedInvalidCues"]}` 

  downloadBlob(
      csv,
      generateOutputFileName("PosnerStats"),
      'text/csv;charset=utf-8;'
  )

  return finalData
}

/** @Deprecated
  * If a user responds to no-go, count towards % of no-goes 
  * Remember JS is pass by reference for tables, s
  * so we can pass original data table and modify it!
*/
// function goNoGoPercent(data, originalDataCollection, dataCategory) {
//   console.log(`${dataCategory} -- Go no go custom stat!! -- ${data} -- ${JSON.stringify(originalDataCollection)}`)
  
//   // For no-gos, we want to track % of go vs no goes 
//   if(dataCategory.substr(0,4) == 'nogo'){
//     console.log("This is a no go trial")
//     var keyToUse = `CUSTOM_${dataCategory}_NoGoPercentCalculator`

//     if(keyToUse in originalDataCollection == false){
//       originalDataCollection[keyToUse] = {
//         "totalTrials" : 0,
//         "totalMisses" : 0,
//         "percentMisses":0
//       }
//     }

//     originalDataCollection[keyToUse]["totalTrials"] += 1
//     if(data == 1){
//       originalDataCollection[keyToUse]["totalMisses"] += 1
//     }

//     originalDataCollection[keyToUse]["percentMisses"] = originalDataCollection[keyToUse]["totalMisses"] / originalDataCollection[keyToUse]["totalTrials"] 
//   }
//   console.log(originalDataCollection)
//   return originalDataCollection
// }

// @Deprecated
// Custom stats thats effectively a 'null' function. Does nothing 
// Intended for stats we want to skip. Not sure if we'll need or not. 
// function noOpSkipFunction(data, originalDataCollection, dataCategory){}

/**
  * Simple mapping for 'custom' statistics calculations.  
  *
  * @Deprecated
*/ 
// function customStatsLogic(experimentName) {
//       var customLogicMapper = {
//         "GoNoGo" : {},
//         "PosnerCue" : {},
//         "TaskSwitching" : {},
//         "SimpleReaction" : {}
//       }

//       customLogicMapper["GoNoGo"]["ErrorStatus"] = (data, originalDataCollection, dataCategory) => goNoGoPercent(data, originalDataCollection, dataCategory)

//       return customLogicMapper[experimentName]
// }


/**
  * Generates a secondary CSV with specified experiment stats.
  * By default will include peak vals (of test vs real). And means for test and real. 
  *
  */
function calculateAutomatedStats(experimentName, data){

  if(experimentName == "TaskSwitching"){
    return calculateSwitchCost(data)
  } else if(experimentName == "GoNoGo"){
    return calculateGoNoGo(data)
  } else if(experimentName == "PosnerCue"){
    return calculatePosnerCueStats(data)
  }

  // @Deprecated 
  // else{

  //     var columnNameMapping = getExperimentToColumnNamesMap(experimentName)

  //     var dataFormatted = data.split("\n")

  //     var customStatisLogic = customStatsLogic(experimentName)

  //     console.log(customStatsLogic)

  //     // Stores the resultant data in a nice hash table :)
  //     var dataToUse = {}

  //     for(var i = 0; i < dataFormatted.length; i++){
  //       // Grab the row
  //       var splitUpRow = dataFormatted[i].replace(/\s{2,}/g, ' ').split(" ")

  //       // Get the 'category' of data
  //       var dataCategory = splitUpRow[0].replaceAll("\"", "")
  //       if(dataCategory === ""){
  //         console.log("Empty string/garbage data, skipping..");
  //       } else {
  //         for(var j = 1; j < columnNameMapping.length; j++){
  //           var dataKey = `${dataCategory}_${columnNameMapping[j]}`
  //           var dataToAddCastToInt = parseInt(splitUpRow[j])

  //           if(columnNameMapping[j] in customStatisLogic == true){
  //             console.log(`Custom stats logic handler: ${columnNameMapping[j]} -- ${dataToAddCastToInt}`)
  //             dataToUse = customStatisLogic[columnNameMapping[j]](
  //               dataToAddCastToInt,
  //               dataToUse,
  //               dataCategory
  //             )
  //           } else {

  //             if(dataKey in dataToUse == false) {
  //               console.log("Add entry to dataToUse table..")
  //               dataToUse[dataKey] = {
  //                 "mean" : 0,
  //                 "peakVal": null,
  //                 "minVal" : null,
  //                 "totalEntries" : 0
  //               }
  //             }

  //             // Actual mean is calculated later. This is just to store the total.
  //             dataToUse[dataKey]["mean"] += dataToAddCastToInt
  //             dataToUse[dataKey]["totalEntries"] += 1

  //             if(dataToUse[dataKey]["peakVal"] == null ||
  //               dataToUse[dataKey]["peakVal"] < dataToAddCastToInt){
  //               dataToUse[dataKey]["peakVal"] = dataToAddCastToInt
  //             }

  //             if(dataToUse[dataKey]["minVal"] == null ||
  //               dataToUse[dataKey]["minVal"] > dataToAddCastToInt){
  //               dataToUse[dataKey]["minVal"] = dataToAddCastToInt
  //             }
  //           }

  //         }
  //       }
  //     }

  //     // Actually calculate the means
  //     for (const key of Object.keys(dataToUse)) {
  //       if("mean" in dataToUse[key]){
  //         // dataToUse[key]["originalMean"] = dataToUse[key]["mean"]
  //         dataToUse[key]["mean"] = (dataToUse[key]["mean"] / dataToUse[key]["totalEntries"])
  //       }
  //     }
  //     return dataToUse
  // }
}

/** @Deprecated 
  * Take data from 'calculateAutomatedStats' and format into a CSV. 
  * Afterwards push to client for download
  *
*/
// function createAutomatedStatsCSV(statsData, experimentName) {


//   var csv = [
//     "",
//     ""
//   ]

//   var statsCsvName = `${experimentName}_stats`

//   // Bad this is hardcoded but o well.. 
//   // CSVs[normalStatsKey] = "mean, minVal, peakVal, totalEntries\n"

//   for (const key of Object.keys(statsData)) {
//     // csv[0] += (Object.keys(statsData[key]).join(",") + "\n")
//     var keysToAdd = ""
//     var valsToAdd = ""
//     for(const dataKey of Object.keys(statsData[key])){
//       keysToAdd += `${key}_${dataKey},`
//       valsToAdd += `${statsData[key][dataKey]},`
//     }

//     csv[0] += keysToAdd
//     csv[1] += valsToAdd
//   }

//   console.log(csv)
  
//   var finalCsv = (csv[0] + "\n" + csv[1])

//   downloadBlob(
//     finalCsv, 
//     generateOutputFileName(statsCsvName), 
//     'text/csv;charset=utf-8;'
//   )  
// }

/*
 * Add collumn identifiers based on experiment name 
 */
function addCollumnsToOutputData(experimentName, data) {
  
  var experimentColumnMapping = getExperimentToColumnNamesMap(experimentName)

  var collumnsAsString = experimentColumnMapping.join(",")

  return `${collumnsAsString}\n${data}`

}

/**
  * Adds version to title of site 
**/
function addVersion(version) {
  document.getElementsByTagName("title")[0].innerText = `v${version}; CSUMB SSB Study`
}


/**
  * Simple helper method to determine if this is a demo site or not 
**/
function isDemo(){
  return isDemoSite
}
/**
  * Injects a custom welcome image :)
  *
  *
*/
function loadWelcomeImageBitMap(){
  var welcomeImageBitMap = "data:image/png;base64,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iGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiiGFAIyIiIooYBjQiIiKiKAHw/wDxTU3qJpTj8gAAAABJRU5ErkJggg=="

  var canvas = document.getElementById("exp");
  var ctx = canvas.getContext("2d");

  var image = new Image();
  image.onload = function() {
    ctx.drawImage(image, 100, 125);
  };
  image.src = welcomeImageBitMap;

}

function reactionTimeDemoReport(data, experimentName){
  var dataSerialized = serializeOutputDataToTable(data, experimentName)
  console.log(dataSerialized)
  var totalTrials = dataSerialized["ResponseTime"].length
  var totalTime = 0
  for(var i = 0; i < dataSerialized["ResponseTime"].length; i++){
    totalTime += parseFloat(dataSerialized["ResponseTime"][i])
  }

  var meanResponseTime = totalTime / totalTrials

  var endUserMessage = `Thank you! You had an average response time of ${meanResponseTime.toString()} milliseconds`
  alert(endUserMessage)
}

function demoReportingRoutine(experimentName){
  console.log("Demo reporting routine")
  if(experimentName == "SimpleReaction"){
    reactionTimeDemoReport(outputdata, experimentName)
  }
}

/**
  * Entry point for the custom data retrieval function. 
  * Basically it bootstraps on top of the existing 'showdata_html' event, 
  *   and will take the data and automatically convert it to a CSV and download it. 
*/
function initCustomDataLoader(experimentName){
    // Store the original method in a local var. 
    var originalShowDataHtml = showdata_html;

    // Stash for later in the callback..
    var EXPERIMENT_NAME = experimentName;

    // Bootstrap listener on top of the 'showdata_html' psytoolkit javascript method. 
    showdata_html = function() {
        if(!isDemo()){
          originalShowDataHtml();

          // Take output data and create the CSV for download 
          outputDataToCSV(
            addCollumnsToOutputData(EXPERIMENT_NAME, outputdata), 
            EXPERIMENT_NAME
          );

          // Stash the stats. Pass on to another function for creating the CSVs 
          var automatedStats = calculateAutomatedStats(
            EXPERIMENT_NAME,
            outputdata
          );
        } else {
          // DEMO CODE BLOCK 
          demoReportingRoutine(experimentName)
        }
    }
}

/**
  * This is effectively the 'main' entry point of the plugin. 
  * Only this function should be called in the psytoolkit scripts. 
  *
*/
function loadZehPlugin(experimentName) {
  console.log("INIT PSYTOOLKIT PLUGIN")

  // Adds  the version 
  addVersion(VERSION);

  // Initialize any required globals
  initGlobalVariableStash(experimentName)

  // Laod the custom welcome image 
  loadWelcomeImageBitMap();

  // Add our custom data loader callback 
  initCustomDataLoader(experimentName);
}