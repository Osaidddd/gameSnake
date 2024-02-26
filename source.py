from sense_hat import SenseHat
from time import sleep
from random import randint

sense = SenseHat()

#setting up colors
snake_color = (0, 255, 0)  #green
food_color = (255, 0, 0)   #red
background_color = (0, 0, 0)  #black

#setting up variables
snake = [(3, 3)]  #snake starts in the middle
direction = "right"
food = (randint(0, 7), randint(0, 7))  #food starts at a random location
score = 0

#draw the snake and food on the Sense HAT
def draw_snake_and_food():
    sense.clear(background_color)
    for segment in snake:
        sense.set_pixel(segment[0], segment[1], snake_color)
    sense.set_pixel(food[0], food[1], food_color)

#move the snake
def move_snake():
    global direction
    head = snake[0]
    if direction == "right":
        new_head = (head[0] + 1, head[1])
    elif direction == "left":
        new_head = (head[0] - 1, head[1])
    elif direction == "up":
        new_head = (head[0], head[1] - 1)
    elif direction == "down":
        new_head = (head[0], head[1] + 1)

    #check for collision with walls
    if new_head[0] < 0 or new_head[0] >= 8 or new_head[1] < 0 or new_head[1] >= 8:
        game_over()
        return

    #check for collision with itself
    if new_head in snake:
        game_over()
        return

    #check for collision with food
    global food, score
    if new_head == food:
        score += 1
        snake.append(snake[-1])  #grow the snake
        food = (randint(0, 7), randint(0, 7))  #move food to a new location
    else:
        snake.pop()  #remove the tail segment

    #move the snake
    snake.insert(0, new_head)

#end the game
def game_over():
    sense.show_message("Game Over!".format(score), text_colour=(255, 0, 0))
    sense.show_message("Score: {}".format(score), text_colour=(255, 255, 255))
    quit()

#handle joystick events
def handle_joystick_event(event):
    global direction
    if event.action == "pressed":
        if event.direction == "up" and direction != "down":
            direction = "up"
        elif event.direction == "down" and direction != "up":
            direction = "down"
        elif event.direction == "left" and direction != "right":
            direction = "left"
        elif event.direction == "right" and direction != "left":
            direction = "right"

#main game loop
sense.stick.direction_any = handle_joystick_event
while True:
    draw_snake_and_food()
    move_snake()
    sleep(0.5)  #snake speed here
