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
