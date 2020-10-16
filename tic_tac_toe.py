from agent import QLearningAgent
from player import RandomPlayer
from board import Board
import random
import matplotlib.pyplot as plt
import pprint

def main():

    # Player 1 will be a Q Learning Agent
    player_1 = QLearningAgent("AI", "X")
    # Player 2 will use a Random Strategy
    player_2 = RandomPlayer("Random Player", "O")

    # Create a new Tic-Tac-Toe Board
    board = Board()

    ## Store metrics for monitoring agent win percentages
    q_agent_wins = 0
    random_player_wins = 0
    ties = 0
    q_agent_win_percentages = []
    random_player_win_percentages = []
    ties_percentage = []
    num_games_percentages= []

    # Set the number of games for the q agent to learn to 50000
    number_games = 50000

    # Loop through selected number of games for training
    for i in range(number_games):
        # Select starting player at random
        if random.choice([1,2]) == 1:
            player_1.set_turn(True)
        else:
            player_2.set_turn(True)

        # Continue game until a win or a tie
        while(not board.get_game_over()):

            # Player 1 Turn
            if player_1.get_turn():
                # Get available moves
                available_moves = board.get_available_moves()
                # Select a move based on q-values and epsilon
                move = player_1.select_move(available_moves,board.get_board_copy())
                # Add selected move to the board
                board.play_move(move, player_1.get_marker())
                # Check if game is over
                game_over = board.is_game_over()
                board.set_game_over(game_over)
                # Switch turns
                player_1.set_turn(False)
                player_2.set_turn(True)

            # Player 2 Turn
            else:
                # Get available moves
                available_moves = board.get_available_moves()
                # Select a move at random
                move = player_2.select_move(available_moves)
                # Play the move
                board.play_move(move, player_2.get_marker())
                # Check if game is over
                game_over = board.is_game_over()
                board.set_game_over(game_over)
                # Switch turns
                player_1.set_turn(True)
                player_2.set_turn(False)

        # Game is over, determine winner
        winning_marker = board.get_winning_marker()
        if player_1.get_marker() == winning_marker:
            # Reward player 1
            player_1.reward_player(1)
            q_agent_wins+=1
        elif player_2.get_marker() == winning_marker:
            # Punish player 1
            player_1.reward_player(-1)
            random_player_wins+=1
        else:
            # Set reward to middle draw
            player_1.reward_player(0.5)
            ties+=1

        if i % 1000 == 0 and i != 0:
            print("Finished Playing {} games...".format(i))

        # Store win percentages for every 100 games
        if i % 100 == 0 and i != 0:
            total_wins = q_agent_wins + random_player_wins + ties
            num_games_percentages.append(i)
            q_agent_win_percentages.append(q_agent_wins/total_wins)
            random_player_win_percentages.append(random_player_wins/total_wins)
            ties_percentage.append(ties/total_wins)

        # Reset the board, remove the current state history for the q-agent
        player_1.reset_history()
        board.reset_board()

    # Print the full q values for each state
    pp = pprint.PrettyPrinter(indent=4)
    print("\nAgent learned q-values:")
    pp.pprint(player_1.get_q_values())

    # Print win percentages
    total_wins = q_agent_wins + random_player_wins + ties
    print("\nTotal Games Played: {}".format(number_games))
    print("Total Agent Wins: {}, Win Percentage: {}".format(q_agent_wins,q_agent_wins/total_wins))
    print("Total Random Strategy Wins : {}, Win Percentage: {}".format(random_player_wins,random_player_wins/total_wins))
    print("Total Ties: {}, Tie Percentage: {}".format(ties,ties/total_wins))

    # Plot win percentages of Q Agent and Random Strategy Agent
    plt.plot(num_games_percentages, q_agent_win_percentages, '.', color='blue',label='Q Agent')
    plt.plot(num_games_percentages, random_player_win_percentages, '.', color='green', label='Random')
    plt.plot(num_games_percentages, ties_percentage, '.', color='yellow', label='Ties')
    plt.title('Q Agent vs Random Strategy Player')
    plt.xlabel("Number of Games")
    plt.ylabel("Win Percentage")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
