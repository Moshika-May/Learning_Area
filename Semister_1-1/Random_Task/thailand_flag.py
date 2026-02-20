from graphics import Canvas

MAIN_CANVAS_WIDTH = 1080
MAIN_CANVAS_HEIGHT = 720
CANVAS_HOME_POSITION = 0

# Thailand top red
THAILAND_FLAG_RED_TOP_X1 = CANVAS_HOME_POSITION
THAILAND_FLAG_RED_TOP_Y1 = CANVAS_HOME_POSITION
THAILAND_FLAG_RED_TOP_X2 = MAIN_CANVAS_WIDTH
THAILAND_FLAG_RED_TOP_Y2 = MAIN_CANVAS_HEIGHT / 6

# Thailand middle blue
THAILAND_FLAG_BLUE_MIDDLE_X1 = CANVAS_HOME_POSITION
THAILAND_FLAG_BLUE_MIDDLE_Y1 = (MAIN_CANVAS_HEIGHT / 2) - MAIN_CANVAS_HEIGHT / 6
THAILAND_FLAG_BLUE_MIDDLE_X2 = MAIN_CANVAS_WIDTH
THAILAND_FLAG_BLUE_MIDDLE_Y2 = (MAIN_CANVAS_HEIGHT / 2) + MAIN_CANVAS_HEIGHT / 6

# Thailand bottom red
THAILAND_FLAG_RED_BOTTOM_X1 = CANVAS_HOME_POSITION
THAILAND_FLAG_RED_BOTTOM_Y1 = MAIN_CANVAS_HEIGHT - (MAIN_CANVAS_HEIGHT / 6)
THAILAND_FLAG_RED_BOTTOM_X2 = MAIN_CANVAS_WIDTH
THAILAND_FLAG_RED_BOTTOM_Y2 = MAIN_CANVAS_HEIGHT

def main():
    main_canvas = Canvas(MAIN_CANVAS_WIDTH, MAIN_CANVAS_HEIGHT, "Thailand_Flag")
    main_canvas.create_rectangle(THAILAND_FLAG_RED_TOP_X1, 
                                 THAILAND_FLAG_RED_TOP_Y1, 
                                 THAILAND_FLAG_RED_TOP_X2, 
                                 THAILAND_FLAG_RED_TOP_Y2, 
                                 "red")
    main_canvas.create_rectangle(THAILAND_FLAG_BLUE_MIDDLE_X1, 
                                 THAILAND_FLAG_BLUE_MIDDLE_Y1, 
                                 THAILAND_FLAG_BLUE_MIDDLE_X2, 
                                 THAILAND_FLAG_BLUE_MIDDLE_Y2, 
                                 "#090088")
    main_canvas.create_rectangle(THAILAND_FLAG_RED_BOTTOM_X1, 
                                 THAILAND_FLAG_RED_BOTTOM_Y1, 
                                 THAILAND_FLAG_RED_BOTTOM_X2, 
                                 THAILAND_FLAG_RED_BOTTOM_Y2, 
                                 "red")
    main_canvas.mainloop()

main()