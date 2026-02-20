from graphics import Canvas

CANVAS_WIDTH = 450
CANVAS_HEIGHT = 300
CANVAS_POSITION_DEFAULT = 0

def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    canvas.create_rectangle(CANVAS_POSITION_DEFAULT, CANVAS_POSITION_DEFAULT, CANVAS_WIDTH, CANVAS_HEIGHT / 2, "red")
    canvas.mainloop()
    
if __name__ == '__main__':
    main()