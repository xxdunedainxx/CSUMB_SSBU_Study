# CSUMB SSBU - Compiled Experiments

This section contains the 'compiled' experiments based on the psytoolkit scripts used for the project. I say 'compiled' in quotes, because realistically these are technically [transpiled](https://en.wikipedia.org/wiki/Source-to-source_compiler), as the code is converted from psytoolkit's DSL, to HTML files. 

This section is an overview of (hopefully) anything you would need to know about the experiments

## Important note regarding experiment modification 

These experiments have been slightly modified, after psytoolkit transpilation. This is due to the fact that there were some features not available in the pre-provided experiment, of which we built some basic mods for. For more information, see [here](mods/README.md). 

## OS & Browser support 

See below for tested and verified browsers/OS's that have been tested with the current experiments. 

| OS   | Browser    | Supported       |
| ---    | ---   | ---     |
| Windows 10 | Chrome | YES |
| Windows 11 | Chrome | YES |
| MacOS - Sonoma 14.5 | Chrome | YES |

## Running the experiments 

It is highly recommended to run the experiments with an OS and browser that has been tested, as suggested above. We suggest using [chrome](https://www.google.com/chrome/dr/download/), however other browsers are likely to work, but not **guaranteed**. Additionally, other Operating Systems **should work**, but again it is highly suggested to run this on systems we have already tested and verified :) 

If chrome is already your [default browser](https://support.google.com/chrome/answer/95417?hl=en&co=GENIE.Platform%3DDesktop), then you can simply 'double click' the file to open the experiment. Otherwise, you will have to 'right click', and open the experiment file in chrome. 

## Experiments List 

* [Go No Go](GoNoGo.html) - Test inhibitory control in participants, see more [here](https://en.wikipedia.org/wiki/Inhibitory_control)
* [Posner Cue Task](Posner.html)- See [here](https://en.wikipedia.org/wiki/Posner_cueing_task)
* [Simple reaction task](SimpleReactionOnly.html) - Test participant reaction time 
* [Task Switching](TaskSwitching.html) - Task switching, or set-shifting, is an executive function that involves the ability to unconsciously shift attention between one task and another. See more information [here](https://en.wikipedia.org/wiki/Task_switching_(psychology))


## Data output

Once the experiment is complete, our mod will run a set of JavaScript functions which will automagically export the results to a CSV file, and download it to your file system. 

Below is a simple, high level overview of what the data output CSV columns mean. 

### GoNoGo output

* 1 - Name of task: go or nogo / training or trial
* 2 - The response speed (in nogo trials, this is 2000, the timeout)
* 3 - The error status (0 is correct, 1 is error)

### TaskSwitching output

* 1 - letter | numbers | mixed and TestOrTrial
* 2 - position of stimulus 1,2,3,4 (top left, top right, bottom right, bottom left
* 3 - tasktype (1 or 2)
* 4 - the letter stimulus
* 5 - the number stimulus
* 6 - type of block (1=just task 1; 2=just task 2; 0=both tasks mixed)
* 7 - 1=task switch , 0=task repeat
* 8 - status (1=correct, 2=error, 3=too slow)
* 9 - response time (ms)
* 10 - total time (response time + button release time)

### Simple Reaction output

Ref: https://www.psytoolkit.org/experiment-library/deary_liewald.html

* 1 - Test or trials 
* 2 - training (1=training, 0=real data collection)
* 3 - number of choices (1 in simple block, 4 in choice block)
* 4 - time between response and next trial (between 1 and 3 seconds)
* 5 - the x-coordinate of the target stimulus
* 6 - the response time (ms)
* 7 - status (1=correct, 2=error, 3=too slow)

### Posner Cue output

Ref: https://www.psytoolkit.org/experiment-library/cueing.html

* 1 - Test or training data
* 2 - cue position (cueleft, cueright)
* 3 - target position (targetleft, targetright)
* 4 - cue validity (cued, uncued)
* 5 - cued or uncued 
* 6 - cue validity as number (1=cued, 0=uncued)
* 7 - Response time (ms)
* 8 - Status (1=correct, 2=wrong, 3=timeout)