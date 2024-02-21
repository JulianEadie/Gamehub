#import the libraries
import os
import time
import random
import threading
from msvcrt import getch

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
