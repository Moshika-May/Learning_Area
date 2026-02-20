from graphics import Canvas
import random

CANVAS_WIDTH = 600      # Width of drawing canvas in pixels
CANVAS_HEIGHT = 300     # Height of drawing canvas in pixels

BRICK_WIDTH	= 30        # The width of each brick in pixels
BRICK_HEIGHT = 12       # The height of each brick in pixels
BRICKS_IN_BASE = 14     # The number of bricks in the base

def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    for row in range(BRICKS_IN_BASE):
        bricks_in_row = BRICKS_IN_BASE - row
        row_width = bricks_in_row * BRICK_WIDTH
        x_offset = (CANVAS_WIDTH - row_width) / 2
        bottom_y = CANVAS_HEIGHT - (row * BRICK_HEIGHT)
        top_y = bottom_y - BRICK_HEIGHT

        for col in range(bricks_in_row):
            start_x = x_offset + (col * BRICK_WIDTH)
            end_x = start_x + BRICK_WIDTH
            canvas.create_rectangle(start_x, top_y, end_x, bottom_y, "yellow", "black")
            
    canvas.mainloop()

if __name__ == '__main__':
    main()