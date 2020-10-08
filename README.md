# NEAT-Stick-Hero
An AI that learns how to play Stick Hero! Using the NEAT python module.

## Files
### Images
Sprites for game animation
### requirements.txt
Use ```pip install -r requirements.txt``` to ensure all dependencies are installed.
### config.txt
NEAT configuration file that is used to pass configurations when generating genomes.
### game.py
Original game file. Use 'x' to grow stick and 'c' to stop growing.
### learn.py
Training file that uses code from game.py to and config.txt to generate populations of agents. Loops over each agent, simulates it performance, and assigns a score to the genome base on its performance. The NEAT module uses neuroevolution to improve the agents based on succesful agents from previous populations. Once training is complete, saves winner to "winner.pkl". 
### winRunner.py
Loads pickled winner and generates its agent which then plays the game!

