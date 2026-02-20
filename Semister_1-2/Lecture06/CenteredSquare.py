from graphics import Canvas

CANVAS_WIDTH = 400
CANVAS_HEIGHT = 300
SQUARE_SIZE = 100

# Get the middle of the canvas
CANVAS_MIDDLE_X = CANVAS_WIDTH / 2
CANVAS_MIDDLE_Y = CANVAS_HEIGHT / 2

def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    
    # Calculate the top left corner position
    left_x = CANVAS_MIDDLE_X - (SQUARE_SIZE / 2)
    top_y = CANVAS_MIDDLE_Y - (SQUARE_SIZE / 2)
    
    # Calculate the right and bottom of the square
    right_x = CANVAS_MIDDLE_X + (SQUARE_SIZE / 2)
    bottom_y = CANVAS_MIDDLE_Y + (SQUARE_SIZE / 2)

    canvas.create_rectangle(left_x, top_y, right_x, bottom_y, 'blue')
    canvas.mainloop()

if __name__ == '__main__':
    main()