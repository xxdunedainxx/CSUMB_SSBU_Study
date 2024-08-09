# Posner Cure Task PsyToolKit script
# Author: Zach McFadden, 7/3/2024
# Modification of the original posner cue tasks with additional bitmaps, and a training + test round 

options
  bitmapdir stimuli    # the folder that contains the stimuli bitmaps

bitmaps
  cuesignal 
  gosignal
  fixpoint1 # small
  fixpoint2 # medium
  fixpoint3 # large
  box
  instruction
  afterwords
  mistakefeedback
  GeneralPreTestMesssage
  GeneralTrialMessage

fonts
  arial 20

# the table section contains 4 rows, one for each of the four
# conditions the stuff in quatation marks is human readable
# information, the program doesn't really need it.

table cueingtable
  "cueleft  targetleft valid     cued 1"  -200 -200  1
  "cueleft  targetleft valid     cued 1"  -200 -200  1
  "cueleft  targetleft valid     cued 1"  -200 -200  1
  "cueright targetleft invalid uncued 0"   200 -200  1
  "cueright targetright valid     cued 1"  200  200  2
  "cueright targetright valid     cued 1"  200  200  2
  "cueright targetright valid     cued 1"  200  200  2
  "cueleft  targetright invalid uncued 0" -200  200  2

# the task describes exactly one trial. On each each trial, one of the
# rows of the cue table is chosen at random

task cueingtask
  table cueingtable
  keys a l
  delay 500 # time between trials
  show bitmap fixpoint1
  show bitmap box -200 0
  show bitmap box  200 0
  delay 75
  show bitmap fixpoint2
  delay 75
  show bitmap fixpoint3
  delay 75
  clear 4 5
  show bitmap fixpoint2
  delay 75
  clear 6
  show bitmap fixpoint1
  delay 200
  show bitmap cuesignal @2 0 # now show the cue
  delay 75
  clear -1
  delay 75
  show bitmap gosignal @3 0 # show target (go) 700 ms later
  readkey @4 1500
  clear -1
  if STATUS != CORRECT
    show bitmap mistakefeedback 0 200
    delay 2000
    clear -1
  fi
  save BLOCKNAME @1 RT STATUS # this saves the data to an output file



block cueingBlockTraining
  message instruction
	message GeneralTrialMessage
  tasklist
    cueingtask 100 # 100 or  25
  end
  bitmap afterwords
  wait_for_key
  feedback
    text align left
    set &RTvalid   mean c7 ; select c8 == 1 && c6 == 1
    set &RTinvalid mean c7 ; select c8 == 1 && c6 == 0
    text -300 0 "Response time (ms)"
    text -300 50 &RTvalid    ; prefix "Valid cue conditions: "   ; postfix " ms"
    text -300 100 &RTinvalid ; prefix "Invalid cue conditions: " ; postfix " ms"
    text -300 250 "Press space bar to continue"
  end

message GeneralPreTestMesssage

block cueingBlockTesting
  tasklist
    cueingtask 100 # 100 # do the task 100 times
  end
  bitmap afterwords
  wait_for_key
  feedback
    text align left
    set &RTvalid   mean c7 ; select c8 == 1 && c6 == 1
    set &RTinvalid mean c7 ; select c8 == 1 && c6 == 0
    text -300 0 "Response time (ms)"
    text -300 50 &RTvalid    ; prefix "Valid cue conditions: "   ; postfix " ms"
    text -300 100 &RTinvalid ; prefix "Invalid cue conditions: " ; postfix " ms"
    text -300 250 "Press space bar to continue"
  end