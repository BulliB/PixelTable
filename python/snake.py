#!/usr/bin/python3

import time
import config
from switchcase import switch
from command import *
from pixels import *
from readback import *
from random import randint

# Constants
NO = 0
YES = 1

# Control
RIGHT = 0
LEFT = 1
UP = 2
DOWN = 3
NONE = 4

# Colors
snake_color = "FFFFFF"
apple_color = "FFFFFF"
snake_color_r = 0xFF
snake_color_g = 0xFF
snake_color_b = 0xFF
apple_color_r = 0xFF
apple_color_g = 0xFF
apple_color_b = 0xFF

# STATE-Machine
STOPPED = 0
RUNNING = 1
OVER = 2
STATE = STOPPED
speed_delay = 0.5



# Snake Boddy, Start Coordinates
x = [5,6,7]
y = [4,4,4]

apple = [13,4]

DIRECTION = NONE

#-----------------------------------------------------------------------------
# Create new Apple on Field
#-----------------------------------------------------------------------------
def newApple():
    global apple
    isTaken = NO

    while True:
        # Calc new Coordinates
        apple[0] = randint(0,config.LED_COLUMN_COUNT-1)
        apple[1] = randint(0,(config.LED_COUNT/config.LED_COLUMN_COUNT)-1)

        # Check if new Position is on snake
        for i in range(0,len(x)):
            if ((x[i] == apple[0]) and (y[i] == apple[1])):
                isTaken = YES

        # Repeate or Breakout
        if isTaken == NO:
            break
        else:
            isTaken = NO


# Move Snake in current direction
def move():
    global x
    global y
    global STATE
    global DIRECTION

    x_new = x[len(x)-1]
    y_new = y[len(y)-1]

    # Get new Coordinates
    for case in switch(DIRECTION):
        if case(RIGHT):
            x_new = x[len(x)-1]+1
            break
        if case(DOWN):
            y_new = y[len(y)-1]+1
            break
        if case(LEFT):
            x_new = x[len(x)-1]-1
            break
        if case(UP):
            y_new = y[len(y)-1]-1
            break

    # Game Over Check - Self Eaten
    for i in range(0,len(x)-1):
        if x[i] == x_new:
            if y[i] == y_new:
                STATE = OVER

    # Game Over Check - Boundry
    if (x_new >= config.LED_COLUMN_COUNT or x_new < 0):
        STATE = OVER
    if (y_new >= config.LED_COUNT/config.LED_COLUMN_COUNT or y_new < 0):
        STATE = OVER

    # Check if Apple got Eaten
    if (apple[0] == x_new) and (apple[1] == y_new):
        x.append(x_new)
        y.append(y_new)
        newApple()
    else:
        for i in range(len(x)-1):
            x[i] = x[i+1]
            y[i] = y[i+1]
        x[len(x)-1] = x_new
        y[len(y)-1] = y_new


def isKeyPress(command):
    if command[0] == "keyPressed":
        return True
    else:
        print("not A KeyPress")
        return False


def readInputs():
    global DIRECTION
    global STATE

    while int(CommandsAvailable()) > 1:
        delLastCommand()
    command = getCommand()
    if isKeyPress(command):
        if command[1] == "UP":
            DIRECTION = UP
        if command[1] == "DOWN":
            DIRECTION = DOWN
        if command[1] == "RIGHT":
            DIRECTION = RIGHT
        if command[1] == "LEFT":
            DIRECTION = LEFT
        print(DIRECTION)
    else:
        STATE = OVER

# Move snake boddy to buffer
def drawSnakeToBuffer(strip):
    for i in range(len(x)):
        index = getPixelIndex(y[i],x[i])
        strip.setPixelColor(index,Color(snake_color_r,snake_color_g,snake_color_b))

# Move Apple to buffer
def drawAppleToBuffer(strip):
    index = getPixelIndex(apple[1],apple[0])
    strip.setPixelColor(index,Color(apple_color_r,apple_color_g,apple_color_b))


def draw(strip):
    clearPixelBuffer(strip)
    drawSnakeToBuffer(strip)
    drawAppleToBuffer(strip)
    strip.show()


def importColors(colors):
    global snake_color_r
    global snake_color_g
    global snake_color_b
    global apple_color_r
    global apple_color_g
    global apple_color_b

    snake_color = colors[1]
    apple_color = colors[2]

    snake_color_r = int(snake_color[0]+snake_color[1],randint(0,255))
    snake_color_g = int(snake_color[2]+snake_color[3],randint(0,255))
    snake_color_b = int(snake_color[4]+snake_color[5],randint(0,255))

    apple_color_r = int(apple_color[0]+apple_color[1],randint(0,255))
    apple_color_g = int(apple_color[2]+apple_color[3],randint(0,255))
    apple_color_b = int(apple_color[4]+apple_color[5],randint(0,255))


# Main function
def snake(strip,parameters):
    global STATE

    # Import the Color scheme
    importColors(parameters)

    # Single draw on Start
    draw(strip)

    # Wait for keyPress
    command = getCommand()
    while command[0] == "startSnake":
        if int(CommandsAvailable()) > 1:
            delLastCommand()
        command = getCommand()
        if (command[0] != "startSnake" and command[0] != "keyPressed"):
            STATE = OVER
            print("Game Over at Start")

    # Main Game Loop
    while STATE != OVER:
        readInputs()
        move()
        draw(strip)
        time.sleep(speed_delay)
    print("Snake: Over")
