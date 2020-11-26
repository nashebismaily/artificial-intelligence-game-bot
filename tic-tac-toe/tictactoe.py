import tkinter as tk
from agent import QLearningAgent
from player import RandomPlayer
from board import Board
import random
import math
from tkinter import *
from tkinter import  simpledialog

def train(ai, board,response):

    # Player 1 will be a Q Learning Agent
    player_1 = ai
    # Player 2 will use a Random Strategy
    player_2 = RandomPlayer("Random Player", "X")

    ## Store metrics for monitoring agent win percentages
    q_agent_wins = 0
    random_player_wins = 0
    ties = 0
    q_agent_win_percentages = []
    random_player_win_percentages = []
    ties_percentage = []
    num_games_percentages= []

    try:
        number_games = int(response)
    except ValueError as verr:
        number_games = 5000
    except Exception as ex:
        number_games = 5000

    print("Training Artificial Intelligence")

    # Loop through selected number of games for training
    for i in range(number_games):
        # Select starting player at random
        if random.choice([1,2]) == 1:
            player_1.set_turn(True)
        else:
            player_2.set_turn(True)

        player_2.set_turn(True)
        # Continue game until a win or a tie
        while(not board.get_game_over()):

            # Player 1 Turn
            if player_1.get_turn():
                # Get available moves
                available_moves = board.get_available_moves()
                # Select a move based on q-values and epsilon
                move, value = player_1.select_move(available_moves,board.get_board_copy())
                # Add selected move to the board
                board.play_move(move, "O")
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
                board.play_move(move, "X")
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

        if (i % 1000 == 0 and i != 0):
            print("AI Finished Playing {} games...".format(i))
        elif i == number_games-1:
            print("AI Finished Playing {} games...".format(response))

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

    print("Training Complete!")

def available_spots():
    h=[]
    for i in range(3):
        for j in range(3):
            if board[i][j]['text'] == '':
                h.append((i,j))
    return h

def check_win():
    for i in range(3):
        if board[i][0]['text'] == board[i][1]['text'] == board[i][2]['text'] != '':
            board[i][0].config(fg='red')
            board[i][1].config(fg='red')
            board[i][2].config(fg='red')
            return 1
    for j in range(3):
        if board[0][j]['text'] == board[1][j]['text'] == board[2][j]['text'] != '':
            board[0][j].config(fg='red')
            board[1][j].config(fg='red')
            board[2][j].config(fg='red')
            return 1
    if board[0][0]['text'] == board[1][1]['text'] == board[2][2]['text'] != '':
        board[0][0].config(fg='red')
        board[1][1].config(fg='red')
        board[2][2].config(fg='red')
        return 1
    elif board[0][2]['text'] == board[1][1]['text'] == board[2][0]['text'] != '':
        board[0][2].config(fg='red')
        board[1][1].config(fg='red')
        board[2][0].config(fg='red')
        return 1
    elif available_spots() == []:
        return 0
    else:
        return -1

player = 'X'
def main_gameflow1(r,c):
    global player
    if board[r][c]['text'] == '' and check_win() == -1:
        # Human move
        board[r][c].config(text='X')
        ai_board.play_move(3 * r + c, "X")
        if check_win() == -1:
            player = 'O'
        elif check_win() == 1:
            label_1.config(text=("Human Wins!"))
            ai.reward_player(-1)
            return
        elif check_win() == 0:
            label_1.config(text="Draw!")
            ai.reward_player(0.5)
            return

        # AI Move
        ai_move,q_value = aiplay(3 * r + c)
        c = ai_move % 3
        r = math.floor(ai_move / 3)
        board[r][c].config(text='O')
        ai_board.play_move(ai_move, "O")
        if check_win() == -1:
            player = 'X'
        elif check_win() == 1:
            ai_board.set_game_over(True)
            label_1.config(text=("AI Wins!"))
            ai.reward_player(1)
        elif check_win() == 0:
            ai_board.set_game_over(True)
            label_1.config(text="Draw!")
            ai.reward_player(0.5)

def aiplay(position):
    available_moves = ai_board.get_available_moves()
    move, q_value = ai.select_move(available_moves, ai_board.get_board_copy())
    return move, q_value

def refresh():
    for i in range(3):
        for j in range(3):
            board[i][j]['text']=''
            board[i][j].config(fg='black')
    label_1.config(text=(""))

    ai.reset_history()
    ai_board.reset_board()

def train_ai_window():
    ai.reset_history()
    ai.reset_q_values()
    refresh()
    response = simpledialog.askstring("Input", "How many games would you like the AI to train on?")
    train(ai,ai_board,response)
    print(ai.get_q_values())

def pre_trained_ai():
    ai.reset_history()
    refresh()
    ai.set_q_values(q_file)
    print(ai.get_q_values())

def show_ai_brain():
    window_2 = Toplevel(window_1)
    window_2.title("AI Brain")
    S = tk.Scrollbar(window_2)
    T = tk.Text(window_2, height=50, width=50)
    S.pack(side=tk.RIGHT, fill=tk.Y)
    T.pack(side=tk.LEFT, fill=tk.Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    quote = str(ai.get_q_values())
    T.insert(tk.END, quote)

# Create AI Agent
ai = QLearningAgent("AI", "O")
ai_board = Board()

# Set AI Exploration to 0.1
ai.set_epsilon(0.1)
q_file= 'pre_trained_ttt_agent.json'

# Create Game Board
board=[[0,0,0],[0,0,0],[0,0,0]]

# Create UI
window_1=tk.Tk()
window_1.title('Tic Tac Toe')
for i in range(3):
    for j in range(3):
        board[i][j]=tk.Button(text='',font=('normal',60,'normal'),width=5,height=3,command=lambda r=i,c=j: main_gameflow1(r,c))
        board[i][j].grid(row=i,column=j)
label_1=tk.Label(text="",font=('normal',22,'bold'))
label_1.grid(row=3,column=1)
button_1=tk.Button(text='Restart',font=('Courier',18,'normal'),fg='red',command=refresh)
button_1.grid(row=4,column=1)
button_1=tk.Button(text='Retrain AI',font=('Courier',18,'normal'),fg='blue',command=train_ai_window)
button_1.grid(row=6,column=1)
button_1=tk.Button(text='Use Pre-trained AI',font=('Courier',18,'normal'),fg='green',command=pre_trained_ai)
button_1.grid(row=7,column=1)
button_1=tk.Button(text='Show AI Brain',font=('Courier',18,'normal'),fg='orange',command=show_ai_brain)
button_1.grid(row=8,column=1)

# Train AI
train_ai_window()

# Begin Game
window_1.mainloop()
