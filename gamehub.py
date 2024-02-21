from enum import Enum
import os
import time
import random
import threading
from msvcrt import getch
import tkinter as tk
from itertools import cycle
from tkinter import font
from typing import NamedTuple

def start_flappy_bird():
  def clear_screen(
    os.system('cls' if os.name == 'nt' else 'clear')
)

def flappy_bird():
    bird = '^'
    gravity = 1
    jump_strength = 2
    pipe_char = '|'
    pipe_gap = 5
    pipe_speed = 0.1
    bird_speed = 0.1

    bird_pos = 10
    bird_velocity = 0
    score = 0
    game_over = False

    def draw_game():
        clear_screen()
        print("Flappy Bird - Score: {}".format(score))
        print(" " * (bird_pos - 1) + bird)
        print("=" * 20)

    def move_bird():
        nonlocal bird_pos, bird_velocity
        bird_velocity += gravity
        bird_pos += bird_velocity

    def generate_pipe():
        pipe_height = random.randint(1, 10)
        return pipe_height

    def check_collision(pipe_height):
        if bird_pos <= 0 or bird_pos >= 20 or (bird_pos <= pipe_height or bird_pos >= pipe_height + pipe_gap):
            return True
        return False

    def game_loop():
        nonlocal score, game_over

        while not game_over:
            pipe_height = generate_pipe()
            pipe_position = 20

            while pipe_position > -1:
                draw_game()
                print(" " * pipe_position + pipe_char * pipe_height + " " * pipe_gap + pipe_char * (20 - pipe_height - pipe_gap))
                
                if pipe_position == bird_pos and check_collision(pipe_height):
                    game_over = True
                    break

                time.sleep(pipe_speed)
                pipe_position -= 1

            score += 1

    game_thread = threading.Thread(target=game_loop)

    try:
        game_thread.start()

        while not game_over:
            key = ord(getch())
            if key == 32:  # Spacebar
                bird_velocity = -jump_strength
                move_bird()
            else:
                move_bird()

            time.sleep(bird_speed)

    except KeyboardInterrupt:
        game_over = True

    game_thread.join()

if __name__ == "__main__":
    flappy_bird()

def start_tic_tac_toe():
  class Player(NamedTuple):
    label: str
    color: str

class Move(NamedTuple):
    row: int
    col: int
    label: str = ""

#defines the board size
BOARD_SIZE = 3
#defines the players x and o and their colours
DEFAULT_PLAYERS = (
    Player(label="X", color="blue"),
    Player(label="O", color="green"),
)

#defines the game
class TicTacToeGame:
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        self._players = cycle(players)
        self.board_size = board_size
        self.current_player = next(self._players)
        self.winner_combo = []
        self._current_moves = []
        self._has_winner = False
        self._winning_combos = []
        self._setup_board()
#makes the board set up itself in the terminal
    def _setup_board(self):
        self._current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self._winning_combos = self._get_winning_combos()
#defines the winning condition
    def _get_winning_combos(self):
        rows = [
            [(move.row, move.col) for move in row]
            for row in self._current_moves
        ]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]

    def toggle_player(self):
        """Return a toggled player."""
        self.current_player = next(self._players)
#makes sure the move is available/valid
    def is_valid_move(self, move):
        """Return True if move is valid, and False otherwise."""
        row, col = move.row, move.col
        move_was_not_played = self._current_moves[row][col].label == ""
        no_winner = not self._has_winner
        return no_winner and move_was_not_played
#this will check if the move wins the game
    def process_move(self, move):
        """Process the current move and check if it's a win."""
        row, col = move.row, move.col
        self._current_moves[row][col] = move
        for combo in self._winning_combos:
            results = set(self._current_moves[n][m].label for n, m in combo)
            is_win = (len(results) == 1) and ("" not in results)
            if is_win:
                self._has_winner = True
                self.winner_combo = combo
                break
#checks if there is a winner and if so it prints who is the winner
    def has_winner(self):
        """Return True if the game has a winner, and False otherwise."""
        return self._has_winner
#check if there is a tie
    def is_tied(self):
        """Return True if the game is tied, and False otherwise."""
        no_winner = not self._has_winner
        played_moves = (
            move.label for row in self._current_moves for move in row
        )
        return no_winner and all(played_moves)
#this resets the game to allow the player to play again
    def reset_game(self):
        """Reset the game state to play again."""
        for row, row_content in enumerate(self._current_moves):
            for col, _ in enumerate(row_content):
                row_content[col] = Move(row, col)
        self._has_winner = False
        self.winner_combo = []

class TicTacToeBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self._cells = {}
        self._game = game
        self._create_menu()
        self._create_board_display()
        self._create_board_grid()

    def _create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(label="Play Again", command=self.reset_board)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Ready?",
            font=font.Font(size=28, weight="bold"),
        )
        self.display.pack()

    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(self._game.board_size):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(self._game.board_size):
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="lightblue",
                )
                self._cells[button] = (row, col)
                button.bind("<ButtonPress-1>", self.play)
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    def play(self, event):
        """Handle a player's move."""
        clicked_btn = event.widget
        row, col = self._cells[clicked_btn]
        move = Move(row, col, self._game.current_player.label)
        if self._game.is_valid_move(move):
            self._update_button(clicked_btn)
            self._game.process_move(move)
            if self._game.is_tied():
                self._update_display(msg="Tied game!", color="red")
            elif self._game.has_winner():
                self._highlight_cells()
                msg = f'Player "{self._game.current_player.label}" won!'
                color = self._game.current_player.color
                self._update_display(msg, color)
            else:
                self._game.toggle_player()
                msg = f"{self._game.current_player.label}'s turn"
                self._update_display(msg)

    def _update_button(self, clicked_btn):
        clicked_btn.config(text=self._game.current_player.label)
        clicked_btn.config(fg=self._game.current_player.color)

    def _update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color

    def _highlight_cells(self):
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground="red")

    def reset_board(self):
        """Reset the game's board to play again."""
        self._game.reset_game()
        self._update_display(msg="Ready?")
        for button in self._cells.keys():
            button.config(highlightbackground="lightblue")
            button.config(text="")
            button.config(fg="black")

def main():
    """Create the game's board and run its main loop."""
    game = TicTacToeGame()
    board = TicTacToeBoard(game)
    board.mainloop()

if __name__ == "__main__":
    main()

def start_rock_paper_scissors():
  class Action(IntEnum):
    Rock = 0
    Paper = 1 
    Scissors = 2 

while True:
#users choice
    def get_user_selection():
        choices = [f"{action.name}[{action.value}]" for action in Action]
        choices_str = ", ".join(choices)
        selection = int(input(f"Enter a choice ({choices_str}): "))
        action = Action(selection)
        return action

#computers choice
possible_actions = ["rock", "paper", "scissors"]
computer_action = random.choice(possible_actions)

#prints the choices made
print(f"\nYou chose {user_action}, the computer chose {computer_action}.\n")

#This determines the winner
if user_action == computer_action:
    print(f"Both players selected {user_action}. It's a tie!")
elif user_action == "rock":
    if computer_action == "scissors:":
        print("Rock Smashes Scissors, You Win!")
    else:
        print("Paper covers rock, You Lose!")
elif user_action == "paper":
    if computer_action == "rock":
        print("Paper Covers Rock, You Win!")
    else:
        print("Scissors cuts pape, You Lose.")
elif user_action == "scissors":
    if computer_action == "paper":
        print("Scissors Cuts Paper, You Win!")
    else:
        print("Rock smashes scissors, You Lose.")

#This is to play again
play_again = input("Play Again? (y/n): ")
if play_again.lower() != "y":
    break
  

class Game(Enum):
    FLAPPY_BIRD = 1
    TIC_TAC_TOE = 2
    ROCK_PAPER_SCISSORS = 3
def choose_game():
    print("Choose a game to play:")
    for game in Game:
        print(f"{game.value}. {game.name.replace('_', ' ').title()}")
    choice = int(input("Enter the number of your choice: "))
    return Game(choice)
def run_game(selected_game):
    if selected_game == Game.FLAPPY_BIRD:
        start_flappy_bird()
    elif selected_game == Game.TIC_TAC_TOE:
        start_tic_tac_toe()
    elif selected_game == Game.ROCK_PAPER_SCISSORS:
        start_rock_paper_scissors()
    else:
        print("Invalid choice. Please choose a valid game.")
selected_game = choose_game()
run_game(selected_game)

if choose_game == 1:
  start_flappy_bird()

else:
  print("Game Not Found")

if choose_game == 2:
  start_tic_tac_toe()

else:
  print("Game Not Found")

if choose_game == 3:
  start_rock_paper_scissors()

else:
  print("Game Not Found")
