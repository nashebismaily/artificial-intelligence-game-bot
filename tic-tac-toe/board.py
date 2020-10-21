import copy

class Board:

    # state of the board
    game_over = False
    # contains 9 locations for tic-tac-toe
    board = None
    # Either X or O for the winner, or T for tie
    winning_marker = ''

    # Constructor
    def __init__(self):
        self.reset_board()

    # Reset the board after a game
    def reset_board(self):
        # Set board to new array with 9 values of '- ': [-,-,-,-,-,-,-,-,-]
        self.board = ['-'] * 9
        winning_marker = ''
        self.set_game_over(False)

    # Add a marker to the board based on the location provided
    def play_move(self, move, marker):
        self.board[move] = marker

    # Game is over, set flag
    def set_game_over(self,game_over):
        self.game_over = game_over

    # Return game status
    def get_game_over(self):
        return self.game_over

    # Return marker for winner: X or O, or T for tie
    def get_winning_marker(self):
        return self.winning_marker

    # Check each of the 9 possible locations for an empty spot denoted by '-'
    def get_available_moves(self):
        available_moves = []
        for i in range(len(self.board)):
            if (self.board[i]) == '-':
                available_moves.append(i)
        return available_moves

    # We don't want references in our board copy, so make a deep copy instead
    def get_board_copy(self):
        return copy.deepcopy(self.board)

    # Check if game is over
    def is_game_over(self):
        # Define all possible winning scenarios (3 of same marker)
        scenarios = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        for scenario in scenarios:
            # For each scenario, append the markers together, ex: xxo, xox, ooo, xxx, etc...
            values = [self.board[scenario[0]], self.board[scenario[1]], self.board[scenario[2]]]
            # Check if marker 0 is the winner
            if all(v == 'O' for v in values):
                self.winning_marker = 'O'
                return True
            # Check if marker X is the winner
            elif all(v == 'X' for v in values):
                self.winning_marker = 'X'
                return True
        # Check for a tie
        if '-' not in self.board:
            self.winning_marker = 'T'
            return True

        return False

    # Pretty print the board
    def print_board(self):
        print(self.board[0],self.board[1],self.board[2])
        print(self.board[3],self.board[4],self.board[5])
        print(self.board[6], self.board[7], self.board[8])




