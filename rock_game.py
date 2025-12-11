"""Name: Michael Jarvis
Purpose: Develop a Python program that runs a rock bouncing game, using the graphics package.
    Practive decision statements
    Practice writing functions, including Boolean functions.
Authenticity: I created this program on my own at home. I got done with the basic requirements for the assignment and decided I wanted to add in 
a countdown timer and score counter just for fun. 
Last edited: 11/08/25
"""
from graphics import *
from random import randint
from math import sqrt
import time

def generate_rocks(num_rocks, win):
    #empty list to add generated rocks to
    rocks_list = []
    #loop for creating the specified number of rocks
    for i in range(num_rocks):
        #gather user click
        pt = win.getMouse()
        #set rock radius as 25
        radius = 25
        #create rock objects with user clicks as center
        rock = Circle(pt, radius)
        #rocks initally set to red
        rock.setFill('red')
        #draw rocks
        rock.draw(win)
        #add rock to list
        rocks_list.append(rock)
    return rocks_list

def build_hit_list(num_rocks):
    #empty list to add nums to
    hit_list = []
    #loop range for each rock made
    for i in range(num_rocks):
        #sets all initial values to 0
        hit_list.append(0)
    return hit_list

def random_color():
    #random color generator
    rand_color = color_rgb((randint(0,255)), (randint(0,255)), randint(0,255))
    return rand_color

def did_collide(ball: Circle, rock: Circle):
    #get cennter for ball and rock
    ball_center = ball.getCenter()
    rock_center = rock.getCenter()
    #compare the distance from the center of the rock to the center of the rock
    dist_x = rock_center.getX() - ball_center.getX()
    dist_y = rock_center.getY() - ball_center.getY()
    distance = sqrt((dist_x *dist_x) + (dist_y*dist_y))
    #50 is used because the rock and ball radii is defined by me as 25 so (25+25=50)
    #so if the distance between the center of the rock and ball is less than the sum of the radii, return true (did collide)
    if distance <= 50:
        return True
    else:
        return False
    
def hit_vertical(ball: Circle, win):
    # Get ball center y value
    center_y = ball.getCenter().getY()
    #ball radius is defined by me
    ball_radius = 25 
    # Check if the top edge of the ball hits the top wall (y <= 0)
    hits_top = (center_y - ball_radius) <= 0
    # Check if the bottom edge of the ball hits the bottom wall (y >= 500)
    hits_bottom = (center_y + ball_radius) >= 500
    if hits_bottom or hits_top:
        return True
    else:
        return False

#same code as hit_vertical just for x axis
def hit_horizontal(ball: Circle, win):
    center_x = ball.getCenter().getX()
    ball_radius = 25
    hits_left = (center_x - ball_radius) <= 0
    hits_right = (center_x + ball_radius) >= 500
    if hits_left or hits_right:
        return True
    else:
        return False

def play_game():
    #initialize the game with the number of rocks to be placed and graphic window
    num_rocks = 5
    height = 500
    width = 500
    win = GraphWin("Rock Game", width, height)
    #instructions to the user
    instructions = Text(Point(250,25), "Click to place 5 rocks ")
    instructions.draw(win)
    #initialize the ball starting position and color
    ball_start = Point(randint(30,width-30),randint(30, height-30))
    ball = Circle(ball_start, 25)
    ball.setFill(random_color())
    ball.draw(win)

    #generate rocks and hit list
    rocks_list = generate_rocks(num_rocks, win)
    hit_list = build_hit_list(num_rocks)
    #get rid of instrcutions after rocks are placed
    instructions.undraw()

    #random ball movement vectors for x and y directions
    dx = randint(-4,4)
    #if movement vector = 0 set it to 1 to keep the ball moving always
    if dx == 0:
        dx= 1

    dy = randint(-4,4)
    if dy == 0:
        dy = 1

    #initialize timer
    start_time = time.time()
    game_duration = 30
    timer_display = Text(Point(width/2,75), game_duration)
    timer_display.setSize(24)
    timer_display.draw(win)

    #while loop that runs the game until 30 seconds have elapsed
    while time.time() - start_time < game_duration:
        #countdown timer
        time_elapsed = time.time() - start_time
        time_remaining = game_duration - time_elapsed
        display_time = int(time_remaining)
        timer_display.setText(f"Time Remaining: {display_time}")
        #move the ball in random directions
        ball.move(dx,dy)
        #initialize score coutner
        score_counter = 0
        #condition statements for if the ball hits the walls
        if hit_vertical(ball, win):
            #reverses ball direction
            dy= -dy
            #sets ball to random color
            ball.setFill(random_color())

        if hit_horizontal(ball, win):
            dx = -dx
            ball.setFill(random_color())

        #loop for rock/ball hit register
        for i in range(num_rocks):
            #current rock is at index i
            rock = rocks_list[i]
            #if the ball hit a rock
            if did_collide(ball,rock):
                #reverses the ball direction when it hits a rock
                ball.move(-dx,-dy)
                #update the hit count 
                hit_list[i] += 1
                #set new random ball direction (same as above random direction code)
                dx = randint(-4,4)
                if dx == 0:
                    dx=1
                dy = randint(-4,4)
                if dy == 0:
                    dy = 1
                #starts moving the ball again in the new random direction
                ball.move(dx,dy)
                #change the rock color based on hit count
                hits = hit_list[i]
                if hits == 3:
                    rock.setFill('yellow')
                if hits >= 6:
                    rock.setFill('green')
                break
        #score counter
        for hits in hit_list:
            if hits >= 3 and hits <6:
                score_counter += 1
            if hits >= 6:
                score_counter += 3
        #delay to slow down movement of ball
        time.sleep(0.01)
    #game over text
    timer_display.setSize(18)
    timer_display.setText("TIME!\n Game over!\n Click to close the window") 
    
    #score criteria display
    score_display = Text(Point(100,50), "Scores:\n Green = 3\nYellow = 1\nRed = 0")
    score_display.draw(win)
    #display player score on the right
    your_score= Text(Point(400, 50), f"Your score: {score_counter}\nMax score: {num_rocks*3}")
    your_score.draw(win)

    #click to close
    win.getMouse()

if __name__ == "__main__":
    play_game()