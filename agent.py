import random
import copy

class QLearningAgent():

    #Player Name
    name = None
    # Tic Tac Toe Marker
    marker = None
    # Percent Exploration for Agent
    epsilon = 0
    # Learning rate
    aplha = 0
    # Discount factor
    gamma = 0
    # Players turn
    turn = False
    # Stores all the states and associated q values
    q_values = {}
    # Stores the history of all moves in the current board
    history = []

    # Constructor
    def __init__(self, name, marker, epsilon=0.2, alpha=0.9, gamma=0.95, default_q=0):
        self.name = name
        self.marker = marker
        self.epsilon = float(epsilon)
        self.alpha = float(alpha)
        self.gamma = float(gamma)

    # Set the players name
    def set_name(self, name):
        self.name = name

    # Set the players marker
    def set_marker(self, marker):
        self.marker = marker

    # Set the exploration rate
    def set_epsilon(self, epsilon):
        self.epsilon = float(epsilon)

    # Set the learning rate
    def set_alpha(self, alpha):
        self.alpha= float(alpha)

    # Set the discount factor
    def set_gamma(self, gamma):
        self.gamma= float(gamma)

    # Set the agents turn
    def set_turn(self, turn):
        self.turn = turn

    # Select a move based on q learning
    def select_move(self, available_moves, board):
        # Agent decides to explore
        probability = random.uniform(0, 1)
        if probability <= self.epsilon:
            best_move = available_moves[random.randrange(0, len(available_moves))]
        # Agent decides to exploit
        else:
            # Set upper bound for value comparison
            max_value = float("-inf")
            # Start by selecting first available move as best move
            best_move = available_moves[0]
            # Loop through all available moves
            for available_move in available_moves:
                # Make a deep copy of the board, with actual values instead of references
                board_copy = copy.deepcopy(board)
                # In the copy of the board, have the agent play the move at the current available location
                board_copy[available_move] = self.get_marker()
                # Get the hash of the board, ex: hash(xxo-----x)
                existing_board = self.q_values.get(self.compute_hash(board_copy))

                # Check if the q value exists for this board
                if existing_board:
                    value = existing_board
                # Set q value to 0
                else:
                    value = 0

                # Best move becomes location associated with largest q value
                if value > max_value:
                    max_value = value
                    best_move = available_move

            # Make a copy of the current board (without future steps)
            board_copy = copy.deepcopy(board)
            # Add a player marker for the selected move
            board_copy[best_move] = self.get_marker()
            self.history.append(self.compute_hash(board_copy))

        return best_move

    # Combines the board into a string
    def compute_hash(self, board):
        return ''.join(board)

    # Reset the agents current board history
    def reset_history(self):
        self.history = []

    # Reward the agent
    def reward_player(self, reward):
        # Loop through the current board history backwards (last entry is winning/loosing move)
        for state in reversed(self.history):
            # Set q value to 0 if state doesn't already exist
            if self.q_values.get(state) is None:
                self.q_values[state] = 0
            # Calculate q
            self.q_values[state] += self.alpha * (self.gamma * reward - self.q_values[state])
            # update current reward, next one should be lower as it's not the final move
            reward = self.q_values[state]

    # get the agent's name
    def get_name(self):
        return self.name

    # get the agent's marker
    def get_marker(self):
        return  self.marker

    # get the exploration rate
    def get_epsilon(self):
        return  self.epsilon

    # get the learning rate
    def get_alpha(self):
        return  self.alpha

    # get the discount rate
    def get_gamma(self):
        return  self.gamma

    # get the players turn
    def get_turn(self):
        return  self.turn

    # get the q-values for all the states
    def get_q_values(self):
        return  self.q_values
