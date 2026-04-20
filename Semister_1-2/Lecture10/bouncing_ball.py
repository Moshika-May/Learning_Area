from graphics import Canvas
import time

CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400
SQUARE_SIZE = 50
DELAY = 0.001

def main():
    # setup
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Bouncing Ball')
    canvas.set_canvas_background_fill('white')
    ball = create_ball(canvas)

    # initial velocity
    velocity_x = 2
    velocity_y = 2

    while True:
        # update world
        draw_shawdow(canvas, ball)
        canvas.move(ball, velocity_x, velocity_y)
        canvas.update()

        # check for collision with walls and reverse direction if necessary
        if hit_vertical_wall(canvas, ball):
            velocity_x = -velocity_x
        
        if hit_horizontal_wall(canvas, ball):
            velocity_y = -velocity_y

        # pause
        time.sleep(DELAY)
  

def hit_vertical_wall(canvas, ball):
    left_x, top_y, right_x, bottom_y = canvas.coords(ball)
    
    # Check for collision with left or right walls
    return left_x <= 0 or right_x >= CANVAS_WIDTH


def hit_horizontal_wall(canvas, ball):
    left_x, top_y, right_x, bottom_y = canvas.coords(ball)
    
    # Check for collision with top or bottom walls
    return top_y <= 0 or bottom_y >= CANVAS_HEIGHT


def create_ball(canvas):
    # Calculate the top left corner position
    left_x = 0
    top_y = 0
    
    # Calculate the right and bottom of the ball
    right_x = left_x + SQUARE_SIZE
    bottom_y = top_y + SQUARE_SIZE
    
    # Draw the ball (as a circle)
    return canvas.create_oval(left_x, top_y, right_x, bottom_y, 'red')


def draw_shawdow(canvas, ball):
    left_x, top_y, right_x, bottom_y = canvas.coords(ball)
    shadow_left_x = left_x
    shadow_top_y = top_y
    shadow_right_x = right_x
    shadow_bottom_y = bottom_y
    
    # Draw the shadow (as a gray oval)
    shawdow = canvas.create_oval(shadow_left_x, shadow_top_y, shadow_right_x, shadow_bottom_y, fill='gray')
    canvas.lower_to_back(shawdow)

if __name__ == '__main__':
    main()