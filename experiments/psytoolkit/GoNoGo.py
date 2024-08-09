# Go-No-Go
# Author: Zach McFadden, 7/3/2024
# Modification of the original Go-No-Go tasks with additional bitmaps, and a training + test round 


bitmaps
  instructions
  gosignal
  nogosignal
  errortype1
  errortype2
  GeneralPreTestMesssage
  GeneralTrialMessage

task go
  keys space
  set $errorstatus 0
  set %saveName TASKNAME  BLOCKNAME
  show bitmap gosignal
  readkey 1 2000 # wait 2 seconds for key to be pressed
  clear 1
  if STATUS == TIMEOUT
    set $errorstatus 1
    show bitmap errortype2
    delay 2000
    clear 2
  fi    
  delay 500 # intertrial interval
  save %saveName RT $errorstatus 

task nogo
  keys space
  set $errorstatus 0
  set %saveName TASKNAME BLOCKNAME
  show bitmap nogosignal
  readkey 1 2000
  clear 1
  if STATUS != TIMEOUT  ## there should be a TIME OUT, so if not, we have a mistake
    set $errorstatus 1
    show bitmap errortype1
    delay 2000
    clear 2
  fi    
  delay 500 # intertrial interval
  save %saveName RT $errorstatus 

# -------------------------------------

message instructions

message GeneralTrialMessage

block GoNoGoTraining
  tasklist
    go 20
    nogo 5
  end

message GeneralPreTestMesssage

block GoNoGoTesting
  tasklist
    go 20
    nogo 5
  end
