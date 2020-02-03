![Supported Python Versions](https://img.shields.io/badge/Python->=3.6-blue.svg?logo=python&logoColor=white)

# ReversIA - An AI for Reversi/Othello game using AlphaBeta algorithm or UCT Search algorithm

**Colin Decourt & Mehamli Théo** 


> This repository contain an AI for Reversi/Othello game using tree search algorithm such as Alpha Beta or Monte Carlo Tree Search algorithms. This was done as part of the courses "Research Algorithm" and "Knowledge Representation" given by Laurent Simon at Bordeaux INP - ENSEIRB MATMECA.

## Description 

The repository is composed of different important files. 

### Board and core functions

The `Reversi.py` file contains core functions to play and develop the AI. 

### Players

The **players** folder contains three different AIs to run a local game.


##### myPlayerBasic

`myPlayerBasic.py`contains behavior functions for playing a party with random moves, without any strategie.


##### myPlayerAlphaBeta

`myPlayerAlphaBeta.py`contrains beavior functions for playing a party with an *negAlphaBeta with memory* algorithm and a MTDF algorithm. These algorithms are inspired from these links : ![French Othello Federation - Principles and strategies](http://www.ffothello.org/othello/principes-strategiques) / ![Heuristic functions for Reversi/Othello](https://kartikkukreja.wordpress.com/2013/03/30/heuristic-function-for-reversiothello/)

We used five different heuristic to find the optimal moves to win : 
  1. Pieces differences heuristic : the player tries to maximize his number of tiles. 
  2. Corner closeness heuristic : the player tries to avoid the tiles close to the corner. Indeed these tiles are sensitive to a capture if the opponent player in the corner. 
  3. Corner occupancy heuristic : the player will try to place tile on the corner to capture tile on diagonals. 
  4. Mobility heuristic
  5. Coin parity heuristic

Each heuristics are weigthed to influence the AI to play more some moves. More detail are provide (in french...) in `myPlayerAlphaBeta.py`code. 

> Weaknesses and improvements : From now, it is only possible to play with AlphaBeta with a 10x10 board. Further versions could contain more **WEIGHT_BOARD** matrices. Moreover heuristics are weighted in the same way during all the game. For example corner closeness and occupancy heursitics could be use more at the end of the party. 

##### myPlayerUCTSearch

`myPlayerUCTSearch.py`contains behavior functions for playing a party using an UCT Search algorithm (Monte Carlo Tree Search based algorithm). We chose to implement this algorihtm because it is known as the best tree search algorithm for playing game such as Reversi or Go. 
UCT search algorithm code can be found in the `UCTSearch.py`file in the *utils* folder. This code was inspired from the page 6 to 10 of ![this](https://ieeexplore.ieee.org/document/6145622) paper. In this file the following functions can be find : 
  1. *Node* class : this class is use to create a new node in the tree and contain informations about parent node, children nodes, the number of time the node has been visited, the current state board and the total simulation reward for this node. 
  2. *Tree policy* function : get a tree policy for a given node. While the node is non terminal and the node is expandable, we expand the tree search. Else we return the best child node. 
  3. *Best child* function : return the best node child.
  4. *Default policy* function : return the best reward for a given state.
  5. *Backup* function : perform the backpropagation. 
  6. *uct_search* function : main loop for finding the best move in the tree. We chose to allow a computational budget of 100 for finding the best child.

## Usage

Download the code, open a terminal and run :

`python localGame.py` 

This will run a local game between to AI. By default the code launch a party between UCT Search and AlphaBeta. UCT Search play first. 

To run custom game : 

`python localGame.py --blackTile nameOfyourAI --whiteTile nameOfyourAI`

Choose an AI among the following list : 
  * UCTSearch
  * random
  * AlphaBeta

Exemple : 

`python localGame.py --blackTile UCTSearch --whiteTile random`

Black tiles always begin but this can be change in `localGame.py` file. 

## Performances

### Alpha Beta with memory algorithm vs Random moves

Number of victory : Alpha Beta always won versus an Random moves AI. 

![](https://github.com/colindecourt/ReversIA/blob/master/images/random_vs_alpha.png)

Total time per party : AlphaBeta (in orange) is very long to play depending on the party (time in seconds). 

![](https://github.com/colindecourt/ReversIA/blob/master/images/time_random_alphaBeta.png)

### Monte Carlo Tree Search algorithm (UCT Search) vs Random moves

Number of victory : UCT Search always won versus an Random moves AI. 

![](https://github.com/colindecourt/ReversIA/blob/master/images/random_vs_uct.png)

Total time per party : Because of a constant allocation of computational ressources, UCT Search algorithm (in orange) play with a constant time. 

![](https://github.com/colindecourt/ReversIA/blob/master/images/time_random_uct.png)

### Monte Carlo Tree Search algorithm (UCT Search) vs Alpha Beta with memory algorithm

#### UCT First

Number of victory : 

![](https://github.com/colindecourt/ReversIA/blob/master/images/alpha_beta_vs_uct_first.png)

Total time per party : As said previously, UCT Search plays with a constant time contrary to AlphaBeta method. 

![](https://github.com/colindecourt/ReversIA/blob/master/images/time_alphabeta_uct_first.png)

#### AlphaBeta First

We noticed that when UCT Search AI plays first, it always won. However, when it plays as the second player the victory is not recurrent. 

Number of victory : Here AlphaBeta won 3 times playing first. 

![](https://github.com/colindecourt/ReversIA/blob/master/images/won_alphabeta_first_uct.png)

Total time per party : 

![](https://github.com/colindecourt/ReversIA/blob/master/images/time_alpha_beta_first_uct.png)
