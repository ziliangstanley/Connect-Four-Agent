# Connect-Four-Agent
This repository contains the connect four agent that was created to compete in a contest against other agents. The contest was held by the NUS CS2109S AY24/25 Sem 1 teaching team.

## Overview
The contest allowed the use of any AI/ML techniques. However, the size of the submitted code should not exceed 1MB and every API call of the agent must take less than 1 second. This agent was created using classic AI techniques listed below.

### Key Components
  1. Minimax Algorithm
  2. Depth-limited Search
  3. Alpha-beta pruning

## Analysis
The agent uses adversarial search techniques such as the Minimax algorithm to determine the best action to play against other rational agents. The Minimax algorithm searches through the entire game state tree to then determine said best action on the assumption that the opponent makes the optimal move as well. We can work with this premise since it is likely that the other agents we compete against will also play optimally.

However, it will clearly be impossible to search through the entire game state tree with all possible moves made by both agents within a second. Hence, we implement depth-limited search to reduce the runtime for each move to be made. By cutting off the state tree at a height of 4, each of these end states are evaluated with a heuristic function which assigns them a score. This allows the Minimax algorithm to do its search on a much smaller state tree.

Lastly, to further reduce the runtime, we use alpha-beta pruning to stop the Minimax algorithm from evaluating a node in the state tree as it will not change the decision of the agent.

## Result
This agent placed at the 63rd percentile among 400+ submissions.

## Areas of Improvement
One area of improvement is to further develop the heuristic function used in the depth-limited search. Since the heuristic function estimates how "good" a state is, it is important for the heuristic function to be as accurate as possible when making this estimation.

Another area of improvement would be to precompute the best moves in the opening and ending parts of the game. Given that connect four is a solved game, we can directly load these moves into the agent so that there is no need to recompute these moves every game.

Lastly, we can implement a transposition table. A transposition table would contain all previously seen positions which removes the need to re-search the game tree below that position. Essentially, the usage of the transposition table is essentially memoization applied to the tree search.

## The Repository
This repository contains the files required to run the agent. Credits to the CS2109S teaching team for providing the files which creates the connect four environment. The code I had written for the agent can be found in contest.py under the AIAgent class.

To run this on your local machine, simply download all the files and run contest.py

By default, you will play against the agent, where you will go first and the agent goes second. 
To change the order of play, simply swap the HumanAgent and AIAgent on line 150 of contest.py
