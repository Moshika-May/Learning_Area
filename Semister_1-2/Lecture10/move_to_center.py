from graphics import Canvas
import time

CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400
SQUARE_SIZE = 50
DELAY = 0.01

def main():
    # setup
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Move to Center')
    canvas.set_canvas_background_fill('white')
    rect = create_square(canvas)

    while not pass_center(canvas, rect):
        # update world
        canvas.move(rect, 1, 0)
        canvas.update()
        # pause
        time.sleep(DELAY)
    
    canvas.mainloop()


def pass_center(canvas, rect):
    # Get the current position of the square
    left_x, top_y, right_x, bottom_y = canvas.coords(rect)
    
    # Calculate the center of the square
    square_center_x = (left_x + right_x) / 2
    
    # Check if the center of the square has passed the center of the canvas
    return square_center_x >= CANVAS_WIDTH / 2


def create_square(canvas):
    center_y = CANVAS_HEIGHT / 2
    
    # Calculate the top left corner position
    left_x = 0
    top_y = center_y - (SQUARE_SIZE / 2)
    
    # Calculate the right and bottom of the square
    right_x = left_x + SQUARE_SIZE
    bottom_y = top_y + SQUARE_SIZE
    
    # Draw the square
    return canvas.create_rectangle(left_x, top_y, right_x, bottom_y, 'blue')

    
if __name__ == '__main__':
    main()