#import the libraries
import random
from enum import IntEnum

#defines the classes
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
