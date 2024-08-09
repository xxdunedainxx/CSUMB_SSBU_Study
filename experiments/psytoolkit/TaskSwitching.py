# A slightly modified version of the alternate runs task switching
# paradigm: Rogers and Monsell, Journal of Experimental Psychology:
# General, 124, 207-231 (2003).
# Modification by: Zach McFadden, 7/3/2024

# grid position 1 is top left, and then clockwise
# task 1 is in top quadrants
# task 2 in bottom quadrants

#### this code does not use a table, but the conditions are calculated
#### with helper variables. The code looks a bit more complicated, but
#### the reason is that neither letters nor numbers should repeat
#### themselves in consecutive trials. This seems the most efficient
#### way of coding it.

options
  bitmapdir stimuli

##
# G K M R  A E I U
# 3 5 7 9  2 4 6 8
# L L L L  R R R R

bitmaps
  ############### stimuli used in tasks
  pg
  pk
  pm
  pr
  pa
  pe
  pi
  pu
  p3
  p5
  p7
  p9
  p2
  p4
  p6
  p8
  ## other stimuli
  grid
  task1
  task2
  ready
  instructions1
  instructions2
  instructions3
  instructions4
  instructions5
  readyletters
  readynumbers
  readylettersnumbers
  thankyou  
  GeneralPreTestMesssage
  GeneralTrialMessage

fonts
  arial 18

######################################################################
# TASK SWITCHING BASED ON ROGERS/MONSELL 1995

# letters 1-8 and numbers 1-8.
# G K M R  A E I U     bitmaps 1-8
# 3 5 7 9  2 4 6 8     bitmaps 9-16 (i.e. 1-8 +8)
# L L L L  R R R R     response

task lettersnumbers
  keys b n
  ## instead of table, determine stimulus/response here #########
  set $letter random 1 8 # select a random letter
  set $number random 1 8 # select a random number
  # keep selecting until letter and number are different from previous trial
  while $letter == &previousletter or $number == &previousnumber
    set $letter random 1 8
    set $number random 1 8
  while-end
  set &previousletter $letter # keep for the next trial
  set &previousnumber $number # keep for the next trial
  set $numberbitmap expression $number + 8 # number bitmaps run from 9-16
  # associate responses for both possible tasks #################
  set $lettertaskresponse 1   # left button
  if $letter > 4
    set $lettertaskresponse 2 # right button
  fi
  set $numbertaskresponse 1   # left button
  if $number > 4
    set $numbertaskresponse 2 # right button
  fi
  ###############################################################
  show bitmap grid
  delay 150 # ITI (RS = 150)
  # which quadrant is being used? this goes clockwise
  # top left is 1, up to four
  set &pos increase 1
  if &pos > 4
    set &pos 1
  fi
  ########## you can also do just one task then you use only 2 quadrants
  if &justtask == 1
    if &pos > 2
      set &pos increase -2
    fi
  fi
  if &justtask == 2
    if &pos < 3
      set &pos increase 2
    fi
  fi
  # determine position 1 and 2 of stimuli (letter is left or number)
  if &pos == 1           # letter task
    set $xpos1 -50
    set $xpos2 -25
    set $ypos  -33
    set $key $lettertaskresponse
    set $tasktype 1
  fi
  if &pos == 2           # letter task
    set $xpos1 25
    set $xpos2 50
    set $ypos  -33
    set $key $lettertaskresponse
    set $tasktype 1
  fi
  if &pos == 3           # number task
    set $xpos1 25
    set $xpos2 50
    set $ypos  33
    set $key $numbertaskresponse
    set $tasktype 2
  fi
  if &pos == 4           # number task
    set $xpos1 -50
    set $xpos2 -25
    set $ypos  33
    set $key $numbertaskresponse
    set $tasktype 2
  fi
  # set up screen
  show bitmap $letter $xpos1 $ypos
  show bitmap $numberbitmap $xpos2 $ypos
  readkey $key 5000
  if STATUS != CORRECT
    if $tasktype == 1
      show bitmap task1 210 -50
    fi
    if $tasktype == 2
      show bitmap task2 210 40
    fi
    delay 3000
    clear -1
  fi
  clear 2 3
  # code if this trial was a task switch or task repeat trial
  if &previoustask == $tasktype
    set &taskswitch 0
  fi
  if &previoustask != $tasktype
    set &taskswitch 1
  fi
  set &previoustask $tasktype
  # save data
  save BLOCKNAME &pos $tasktype $letter $number &justtask &taskswitch STATUS RT TT

######################################################################
#			   BLOCKS START HERE                         #
######################################################################

message GeneralTrialMessage

block lettersTraining
  pager instructions1 instructions2 instructions3 instructions4 instructions5
  message readyletters
  set &previoustask -1
  set &taskswitch 0 # 1 if a trial is a task switch trial
  set &justtask 1 # this makes that only the letter task is being selected
  tasklist
    lettersnumbers 60 
  end

block numbersTraining
  set &justtask 2 # this makes that only the number task is being selected
  message readynumbers
  tasklist
    lettersnumbers 60
  end

block mixedTraining
  set &justtask 0 # this makes that both tasks are in alternative run sequence
  message readylettersnumbers
  tasklist
    lettersnumbers 60 # Per IRB, 120 in total for trial and test 
  end
  feedback
    text align left
    set &RTpure      mean c9 ; select c8 == 1 && c6 != 0 && c7 == 0
    set &RTmixRepeat mean c9 ; select c8 == 1 && c6 == 0 && c7 == 0
    set &RTmixSwitch mean c9 ; select c8 == 1 && c6 == 0 && c7 == 1
    set &RTMixCost    expression &RTmixRepeat - &RTpure
    set &RTSwitchCost expression &RTmixSwitch - &RTmixRepeat
    text -200 -150 "Response times (RT in ms):"
    text -200 -50  &RTpure       ; prefix "RTs in single-task blocks: " ; postfix " ms"
    text -200   0  &RTmixRepeat  ; prefix "RTs in mixed block, task-repeat trials: " ; postfix "ms"
    text -200  50  &RTmixSwitch  ; prefix "RTs in mixed block, task-switch trials: " ; postfix "ms"
    text -200 100  &RTSwitchCost ; prefix "Task switch cost in RTs: " ; postfix "ms"
    text -200 150  "Press space bar to continue"
  end

message GeneralPreTestMesssage

block lettersTesting
  message readyletters
  set &previoustask -1
  set &taskswitch 0 # 1 if a trial is a task switch trial
  set &justtask 1 # this makes that only the letter task is being selected
  tasklist
    lettersnumbers 60 
  end

block numbersTesting
  set &justtask 2 # this makes that only the number task is being selected
  message readynumbers
  tasklist
    lettersnumbers 60
  end

block mixedTesting
  set &justtask 0 # this makes that both tasks are in alternative run sequence
  message readylettersnumbers
  tasklist
    lettersnumbers 60 # Per IRB, 120 in total for trial and test 
  end
  feedback
    text align left
    set &RTpure      mean c9 ; select c8 == 1 && c6 != 0 && c7 == 0
    set &RTmixRepeat mean c9 ; select c8 == 1 && c6 == 0 && c7 == 0
    set &RTmixSwitch mean c9 ; select c8 == 1 && c6 == 0 && c7 == 1
    set &RTMixCost    expression &RTmixRepeat - &RTpure
    set &RTSwitchCost expression &RTmixSwitch - &RTmixRepeat
    text -200 -150 "Response times (RT in ms):"
    text -200 -50  &RTpure       ; prefix "RTs in single-task blocks: " ; postfix " ms"
    text -200   0  &RTmixRepeat  ; prefix "RTs in mixed block, task-repeat trials: " ; postfix "ms"
    text -200  50  &RTmixSwitch  ; prefix "RTs in mixed block, task-switch trials: " ; postfix "ms"
    text -200 100  &RTSwitchCost ; prefix "Task switch cost in RTs: " ; postfix "ms"
    text -200 150  "Press space bar to continue"
  end
