"""
File: breakout.py
-----------------
This program implements the game Breakout!  The user controls a paddle
moving horizontally with the mouse, and the user must bounce the ball
to make it collide and remove bricks from the screen.  The user has
N_TURNS turns.  If the ball falls below the bottom of the screen, the user
loses a turn.  If the user removes all bricks before their turns
run out, they win!
"""

from graphics import Canvas
import random
import time

# Step 1: Set up the bricks

# Dimensions of the canvas
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 600

# Number of bricks in each row
N_BRICK_COLUMNS = 10

# Number of rows of bricks
N_BRICK_ROWS = 10

# Separation between neighboring bricks, in pixels
BRICK_SEP = 4

# Width of each brick, in pixels
BRICK_WIDTH = (CANVAS_WIDTH-BRICK_SEP * (N_BRICK_COLUMNS + 1)) // N_BRICK_COLUMNS

# Height of each brick, in pixels
BRICK_HEIGHT = 10

# Offset of the top brick row from the top of the canvas, in pixels
BRICK_Y_OFFSET = 70

# List of colors for the bricks
COLORS = ['red', 'orange', 'yellow', 'green', 'blue']

# Step 2: Create the bouncing ball

# Radius of the ball in pixels
BALL_RADIUS = 10

# The ball's vertical velocity
VELOCITY_Y = 6.0

# The ball's minimum and maximum horizontal velocity; the bounds of the
# initial random velocity that you should choose (randomly +/-).
VELOCITY_X_MIN = 2.0
VELOCITY_X_MAX = 6.0

# Animation delay or pause time between ball moves (in seconds)
DELAY = 1 / 120

# Stage 3: Create the Paddle

# Dimensions of the paddle
PADDLE_WIDTH = 70
PADDLE_HEIGHT = 15

# How far up the top of the paddle is from bottom of the canvas
PADDLE_Y_OFFSET = 50

# Stage 5: Finishing touches

# Number of turns
N_TURNS = 3


def create_bricks(canvas):
    bricks = []
    for row in range(N_BRICK_ROWS):
        for col in range(N_BRICK_COLUMNS):
            left_x = BRICK_SEP + col * (BRICK_WIDTH + BRICK_SEP)
            top_y = BRICK_Y_OFFSET + row * (BRICK_HEIGHT + BRICK_SEP)
            right_x = left_x + BRICK_WIDTH
            bottom_y = top_y + BRICK_HEIGHT
            
            color_index = (row // 2) % len(COLORS)
            color = COLORS[color_index]
            
            brick = canvas.create_rectangle(left_x, top_y, right_x, bottom_y, fill=color)
            bricks.append(brick)
    return bricks


def create_ball(canvas):
    left_x = CANVAS_WIDTH / 2 - BALL_RADIUS
    top_y = CANVAS_HEIGHT / 2 - BALL_RADIUS
    right_x = left_x + 2 * BALL_RADIUS
    bottom_y = top_y + 2 * BALL_RADIUS
    
    ball = canvas.create_oval(left_x, top_y, right_x, bottom_y, fill="black")
    return ball


def create_paddle(canvas):
    left_x = CANVAS_WIDTH / 2 - PADDLE_WIDTH / 2
    top_y = CANVAS_HEIGHT - PADDLE_Y_OFFSET - PADDLE_HEIGHT
    right_x = left_x + PADDLE_WIDTH
    bottom_y = top_y + PADDLE_HEIGHT
    
    paddle = canvas.create_rectangle(left_x, top_y, right_x, bottom_y, fill="black")
    return paddle


def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Breakout')
    canvas.set_canvas_background_fill("white")

    bricks = create_bricks(canvas)
    ball = create_ball(canvas)
    paddle = create_paddle(canvas)
    
    turns = N_TURNS
    
    while turns > 0 and len(bricks) > 0:
        click_text = canvas.create_text((CANVAS_WIDTH / 2) - 40, CANVAS_HEIGHT / 2 - 20, text="Click to start", font="Arial 24")
        turns_text = canvas.create_text((CANVAS_WIDTH / 2) - 40, CANVAS_HEIGHT / 2 + 10, text=f"Turns left: {turns}", font="Arial 24")
        
        canvas.wait_for_click()
        
        canvas.delete(click_text)
        canvas.delete(turns_text)
        
        vx = random.uniform(VELOCITY_X_MIN, VELOCITY_X_MAX)
        if random.random() < 0.5:
            vx = -vx
        vy = VELOCITY_Y
        
        turn_active = True
        while turn_active:
            mouse_x = canvas.get_mouse_x()
            paddle_x = mouse_x - PADDLE_WIDTH / 2
            
            paddle_x = max(0, min(paddle_x, CANVAS_WIDTH - PADDLE_WIDTH))
            canvas.move_to(paddle, paddle_x, CANVAS_HEIGHT - PADDLE_Y_OFFSET - PADDLE_HEIGHT)
            
            canvas.move(ball, vx, vy)
            
            ball_x = canvas.get_left_x(ball)
            ball_y = canvas.get_top_y(ball)
            
            if ball_x <= 0 or ball_x + 2 * BALL_RADIUS >= CANVAS_WIDTH:
                vx = -vx
                
            if ball_y <= 0:
                vy = -vy
                
            if ball_y + 2 * BALL_RADIUS >= CANVAS_HEIGHT:
                turns -= 1
                turn_active = False
                
                canvas.move_to(ball, CANVAS_WIDTH / 2 - BALL_RADIUS, CANVAS_HEIGHT / 2 - BALL_RADIUS)
                break
                
            colliders = canvas.find_overlapping(ball_x, ball_y, ball_x + 2 * BALL_RADIUS, ball_y + 2 * BALL_RADIUS)
            
            hit_object = None
            for c in colliders:
                if c != ball:
                    hit_object = c
                    break
                    
            if hit_object:
                if hit_object == paddle:
                    if vy > 0:
                        vy = -vy
                elif hit_object in bricks:
                    canvas.delete(hit_object)
                    bricks.remove(hit_object)
                    vy = -vy
                    
                    if len(bricks) == 0:
                        turn_active = False
                        break
                        
            canvas.update()
            time.sleep(DELAY)

    if turns == 0:
        canvas.create_text(CANVAS_WIDTH / 2 - 40, CANVAS_HEIGHT / 2, text="Game Over", font="Arial 24")
    elif len(bricks) == 0:
        canvas.create_text(CANVAS_WIDTH / 2 - 30, CANVAS_HEIGHT / 2, text="You Win!", font="Arial 24")

    canvas.mainloop()

if __name__ == '__main__':
    main()