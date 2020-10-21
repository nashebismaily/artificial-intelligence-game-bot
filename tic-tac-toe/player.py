import random

class RandomPlayer:

    #Player Name
    name = None
    # Tic Tac Toe Marker
    marker = None
    # Players turn
    turn = False

    def __init__(self, name, marker ):
        self.name = name
        self.marker = marker

    # Select a move at random from available moves and return
    def select_move(self, available_moves):
        return available_moves[random.randrange(0, len(available_moves))]

    # Set player name
    def set_name(self, name):
        self.name = name

    # Set player marker
    def set_marker(self, marker):
        self.marker = marker

    # Set players turn
    def set_turn(self, turn):
        self.turn = turn

    # Get players name
    def get_name(self):
        return self.name

    # Get players marker
    def get_marker(self):
        return self.marker

    # Get players turn
    def get_turn(self):
        return self.turn
