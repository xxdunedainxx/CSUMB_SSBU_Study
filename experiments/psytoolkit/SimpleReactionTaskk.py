# Simple Reaction Time PsyToolKit script
# Author: Zach McFadden, 7/3/2024
# Modification of the origina psytoolkit script, which ONLY includes the Simple Reaction Time task 
# 10 training & 20 testing rounds should be ran. 

options
  bitmapdir stimuli
  set &dummy 0
  set &maxResponseTime 3000
  set &minInterval 1000
  set &maxInterval 3000  

fonts
  arial 18
  
bitmaps
  instruction_simple_task
  instruction_choice_task1
  instruction_choice_task2
  instruction_choice_task3
  readytraining
  readyreal
  thankyou
  title
  too_slow
  wrong_key
  reminder
  box_empty
  box_cross

task dl_task_simple
  keys space
  set $num_choices 1
  show background 0 0 100
  show bitmap box_empty
  set $randomdelay random &minInterval &maxInterval
  delay $randomdelay
  show bitmap box_cross
  readkey 1 &maxResponseTime
  clear 3
  save BLOCKNAME &training $num_choices $randomdelay &dummy RT STATUS

######################################################################
## blocks start here

block dlsimple_training
  set &training 1
  message title
  message instruction_simple_task
  message readytraining
  tasklist
  	# ROUNDS ARE DETERMINED BY THE FIRST ARG BELOW
  	# CHANGE VALUE FOR ARGUMENT TO 'dl_task_simple' to alter the number of rounds 
    dl_task_simple 10
  end
  delay 1000

block dlsimple_real
	set &TESTING_ROUNDS 1 
  set &training 0
  message readyreal
  tasklist
  	# ROUNDS ARE DETERMINED BY THE FIRST ARG BELOW
  	# CHANGE VALUE FOR ARGUMENT TO 'dl_task_simple' to alter the number of rounds 
    dl_task_simple 20
  end
  delay 1000

message thankyou
