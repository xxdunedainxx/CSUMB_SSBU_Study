# CSU Monterey Bay - Super Smah Bros Ultimate Cognitive Research

Repo for the experiment code regarding a super smash bros ultimate cognitive research study being done at [CSU Monterey Bay](https://csumb.edu/)), where we are attempting to observe various cognitive capabilities in relationship to various players of super smash brothers. 

Experiments are built on top of the [psytoolkit](https://www.psytoolkit.org/). 

## Navigation of the repository

Experiment code can be found under `experiments`, of which there are two different directories to be mindful of:

1. `experiments/compiled`: Contains runnable versions of the experiments, which are effectively MASSIVE html files containing all of the experiment logic (in vanilla JavaScript) & the needed HTML to render the experiment UI. For more info on the compiled experiments, see [here](experiments/compiled/README.md)

2. `experiments/psytoolkit`: Contains the psytoolkit scripts which are eventually transpiled into the massive HTML files explained above. For more information on the scripts, see [here](experiments/psytoolkit/README.md)