from game_utils import initialize, step, get_valid_col_id, is_win, is_end, COLUMN_COUNT, ROW_COUNT
import numpy as np
import random
from simulator import GameController, HumanAgent
from connect_four import ConnectFour

class AIAgent(object):
    """
    A class representing an agent that plays Connect Four.
    """
    def __init__(self, player_id=1):
        """Initializes the agent with the specified player ID.

        Parameters:
        -----------
        player_id : int
            The ID of the player assigned to this agent (1 or 2).
        """
        self.player = player_id
        self.enemy = 2 if player_id == 1 else 1
        self.depth_limit = 4

    def minimax(self, state, depth, alpha, beta, current_player):
        if is_end(state):
            if is_win(state):
                if current_player == self.player:
                    return (-1000000, None)
                else:
                    return (1000000, None)
            else:
                return (0, None)
        elif depth == 0:
            return (self.evaluate_state(state), None)
        else:
            if current_player == self.player:
                value = float('-inf')
                possible_columns = get_valid_col_id(state)
                result_column = random.choice(possible_columns)
                for cols in possible_columns:
                    possible_state = step(state, cols, self.player, in_place=False)
                    possible_value = self.minimax(possible_state, depth - 1, alpha, beta, self.enemy)[0]
                    if possible_value > value:
                        value = possible_value
                        result_column = cols
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
                return (value, result_column)
            else:
                value = float('inf')
                possible_columns = get_valid_col_id(state)
                result_column = random.choice(possible_columns)
                for cols in possible_columns:
                    possible_state = step(state, cols, self.enemy, in_place=False)
                    possible_value = self.minimax(possible_state, depth - 1, alpha, beta, self.player)[0]
                    if possible_value < value:
                        value = possible_value
                        result_column = cols
                    beta = min(beta, possible_value)
                    if alpha >= beta:
                        break
                return (value, result_column)

        
    def evaluate_state(self, state):
        result = 0

        center_array = state[:, COLUMN_COUNT // 2]
        center_count = np.count_nonzero(center_array == self.player)
        result += center_count * 6

        for row in range(ROW_COUNT): 
            row_array = state[row, :] 
            for col in range(COLUMN_COUNT - 3): 
                window = row_array[col: col + 4] 
                result += self.evaluate_window(window, self.player) 
 
        for col in range(COLUMN_COUNT): 
            col_array = state[:, col] 
            for row in range(ROW_COUNT - 3): 
                window = col_array[row: row + 4] 
                result += self.evaluate_window(window, self.player) 
 
        for row in range(ROW_COUNT - 3): 
            for col in range(COLUMN_COUNT - 3): 
                window = [state[row+i][col+i] for i in range(4)] 
                result += self.evaluate_window(window, self.player) 
 
        for row in range(3, ROW_COUNT): 
            for col in range(COLUMN_COUNT - 3): 
                window = [state[row-i][col+i] for i in range(4)] 
                result += self.evaluate_window(window, self.player) 
 
        return result
        
    def evaluate_window(self, window, player_id): 
        result = 0 
        opponent_id = 2 if player_id == 1 else 1 
 
        if np.count_nonzero(window == player_id) == 4: 
            result += 100
        elif np.count_nonzero(window == player_id) == 3 and np.count_nonzero(window == 0) == 1: 
            result += 10
        elif np.count_nonzero(window == player_id) == 2 and np.count_nonzero(window == 0) == 2: 
            result += 5
 
        if np.count_nonzero(window == opponent_id) == 3 and np.count_nonzero(window == 0) == 1: 
            result -= 8

        return result
    
    def make_move(self, state):
        """
        Determines and returns the next move for the agent based on the current game state.

        Parameters:
        -----------
        state : np.ndarray
            A 2D numpy array representing the current, read-only state of the game board. 
            The board contains:
            - 0 for an empty cell,
            - 1 for Player 1's piece,
            - 2 for Player 2's piece.

        Returns:
        --------
        int
            The valid action, ie. a valid column index (col_id) where this agent chooses to drop its piece.
        """
        """ YOUR CODE HERE """
        return self.minimax(state, self.depth_limit, float('-inf'), float('inf'), self.player)[1]
        """ YOUR CODE END HERE """

def test_task_1_1():
    from utils import check_step, actions_to_board
    
    # Test case 1
    res1 = check_step(ConnectFour(), 1, AIAgent)
    assert(res1 == "Pass")
    
    # Test case 2
    res2 = check_step(actions_to_board([0, 0, 0, 0, 0, 0]), 1, AIAgent)
    assert(res2 == "Pass")
    
    # Test case 3
    res2 = check_step(actions_to_board([4, 3, 4, 5, 5, 1, 4, 4, 5, 5]), 1, AIAgent)
    assert(res2 == "Pass")

board = ConnectFour()
game = GameController(board=board, agents=[HumanAgent(1), AIAgent(2)])
#game = GameController(board=board, agents=[AIAgent(1), HumanAgent(2)])
game.run()
