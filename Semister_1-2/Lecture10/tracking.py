from graphics import Canvas
import time

CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400
SQUARE_SIZE = 50
DELAY = 0.001

# this program will track the position of the mouse and draw a square that follows the mouse around the canvas
def main():
    # setup
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Tracking')
    canvas.set_canvas_background_fill('white')
    square = create_square(canvas)

    while True:
        # update world
        mouse_x, mouse_y = canvas.get_mouse_x(), canvas.get_mouse_y()
        left_x = mouse_x - (SQUARE_SIZE / 2)
        top_y = mouse_y - (SQUARE_SIZE / 2)
        right_x = left_x + SQUARE_SIZE
        bottom_y = top_y + SQUARE_SIZE
        canvas.coords(square, left_x, top_y, right_x, bottom_y)
        canvas.update()

        # pause
        time.sleep(DELAY)

def create_square(canvas):
    # Calculate the top left corner position
    left_x = 0
    top_y = 0
    
    # Calculate the right and bottom of the square
    right_x = left_x + SQUARE_SIZE
    bottom_y = top_y + SQUARE_SIZE
    
    # Draw the square
    return canvas.create_rectangle(left_x, top_y, right_x, bottom_y, 'blue')

if __name__ == '__main__':
    main()