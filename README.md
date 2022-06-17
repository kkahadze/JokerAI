# JokerAI
This is an implementation of the Joker card game in Python. I created this in order to be able to play against a smart Joker AI that has the potential to beat
human players.
## What is Joker?
Joker is a card game commonly played in the country of Georgia and by some in Russia. It is not popular worldwide but has a lot of dedicated fans who even play
online on sites like [this](https://www.jok.ge). Joker is a card game played between four people in which each player must "call" how many hands they think they 
will take at the beginning of each set after a certain amount of cards are dealt to each user. After, each player must battle it out to see who can take the 
amount that they predicted they would. A more detailed description of the Joker card game can be found [here](https://www.pagat.com/exact/joker.html).
## Setup and Play
To begin playing Joker through your command line, this is all you need to do:
```
$ git clone https://github.com/kkahadze/JokerAI.git && cd JokerAI/src  
$ python3 joker.py game
```
## Running Simulations
If you would like to run simulations of Joker games in order to train your own Joker AI, you can run as many as you like and store them in a csv by running:
the following while inside the src directory
```
$ python3 joker.py simulation 100
```
Here, 100 simulations are run and stored in a csv titled joker_simulations.csv. 
If you would like to run the simulations with random calls you can run the following:
```
$ python3 joker.py simulation 100 NOMODEL
```
## Why Joker?
Aside from growing up and spending hours playing the card game in person my journey with the Joker game began when I implemented a version of the [Joker game in Rust](https://github.com/kkahadze/Joker-In-Rust). 
This version of the game needed 4 people to play and was limited by not being able to play against an AI. Once I understood the issues with my game. I decided to 
rewrite the game in Python, and use my knowledge of ML to create a ML model for predicting "calls" in the game. I trained the model by running a simulation of 
1,000 full joker games, consisting of 144,000 total hands and extracting relevant that the AI had before choosing their call.I trained this AI myself and pickled 
it to be loaded in at the beginning of the game. 
## Further Development
To make the AI even better, I plan to replace the hueristic that actually picks the cards to play for the AI, with a machine learned model to improve card choices.
## Dependencies
- Numpy
- Scikit-Learn
## License
[MIT](https://choosealicense.com/licenses/mit/)
