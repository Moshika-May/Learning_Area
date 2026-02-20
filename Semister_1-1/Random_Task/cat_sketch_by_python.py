from graphics import Canvas

# 1. Target Resolution
WIDTH = 720
HEIGHT = 720

# 2. Base Design Grid (The mathematical proportions of the cat)
GRID_W = 400
GRID_H = 500

# 3. Dynamic Math: Scale and Centering Offsets
# Calculates uniform scale so the cat fits perfectly in the given resolution
SCALE = min(WIDTH / GRID_W, HEIGHT / GRID_H)

# Calculates exactly how much empty space to leave on the sides to center the image
OFFSET_X = (WIDTH - (GRID_W * SCALE)) / 2
OFFSET_Y = (HEIGHT - (GRID_H * SCALE)) / 2

# 4. Colors
COLOR_BLACK = "black"
COLOR_WHITE = "white"
COLOR_PINK = "#FF99B3"    
COLOR_DARK_PINK = "#FF4D79" 

# 5. Line Widths (Mathematically scaled to match the resolution)
W_THICK = 15 * SCALE
W_TAIL_PINK = 11 * SCALE
W_OUTLINE = 5 * SCALE
W_EYE = 6 * SCALE
W_PAW = 4 * SCALE
W_THIN = 3 * SCALE
W_TINY = 2 * SCALE

# 6. Angles (Degrees remain constant)
ARC_HALF = 180
ARC_START_BOTTOM = 180
ARC_START_RIGHT = 0
ARC_START_TOP = 90
ARC_TAIL_TIP = 50

# 7. Coordinates (Projected mathematically: Offset + (Point * Scale))
COORD_TAIL = (
    OFFSET_X + 60 * SCALE, OFFSET_Y + 350 * SCALE, 
    OFFSET_X + 160 * SCALE, OFFSET_Y + 450 * SCALE
)
COORD_EAR_L_OUTER = (
    OFFSET_X + 80 * SCALE, OFFSET_Y + 200 * SCALE, 
    OFFSET_X + 110 * SCALE, OFFSET_Y + 110 * SCALE, 
    OFFSET_X + 160 * SCALE, OFFSET_Y + 170 * SCALE
)
COORD_EAR_L_INNER = (
    OFFSET_X + 95 * SCALE, OFFSET_Y + 180 * SCALE, 
    OFFSET_X + 110 * SCALE, OFFSET_Y + 135 * SCALE, 
    OFFSET_X + 145 * SCALE, OFFSET_Y + 170 * SCALE
)
COORD_EAR_R_OUTER = (
    OFFSET_X + 320 * SCALE, OFFSET_Y + 200 * SCALE, 
    OFFSET_X + 290 * SCALE, OFFSET_Y + 110 * SCALE, 
    OFFSET_X + 240 * SCALE, OFFSET_Y + 170 * SCALE
)
COORD_EAR_R_INNER = (
    OFFSET_X + 305 * SCALE, OFFSET_Y + 180 * SCALE, 
    OFFSET_X + 290 * SCALE, OFFSET_Y + 135 * SCALE, 
    OFFSET_X + 255 * SCALE, OFFSET_Y + 170 * SCALE
)
COORD_BODY = (
    OFFSET_X + 120 * SCALE, OFFSET_Y + 300 * SCALE, 
    OFFSET_X + 280 * SCALE, OFFSET_Y + 460 * SCALE
)
COORD_PAW_L = (
    OFFSET_X + 140 * SCALE, OFFSET_Y + 430 * SCALE, 
    OFFSET_X + 190 * SCALE, OFFSET_Y + 470 * SCALE
)
COORD_PAW_M = (
    OFFSET_X + 180 * SCALE, OFFSET_Y + 430 * SCALE, 
    OFFSET_X + 230 * SCALE, OFFSET_Y + 470 * SCALE
)
COORD_PAW_R = (
    OFFSET_X + 220 * SCALE, OFFSET_Y + 430 * SCALE, 
    OFFSET_X + 270 * SCALE, OFFSET_Y + 470 * SCALE
)
COORD_HEAD = (
    OFFSET_X + 60 * SCALE, OFFSET_Y + 160 * SCALE, 
    OFFSET_X + 340 * SCALE, OFFSET_Y + 360 * SCALE
)
COORD_CHEEK_L = (
    OFFSET_X + 100 * SCALE, OFFSET_Y + 280 * SCALE, 
    OFFSET_X + 140 * SCALE, OFFSET_Y + 310 * SCALE
)
COORD_CHEEK_R = (
    OFFSET_X + 260 * SCALE, OFFSET_Y + 280 * SCALE, 
    OFFSET_X + 300 * SCALE, OFFSET_Y + 310 * SCALE
)
COORD_EYE_L = (
    OFFSET_X + 110 * SCALE, OFFSET_Y + 230 * SCALE, 
    OFFSET_X + 170 * SCALE, OFFSET_Y + 270 * SCALE
)
COORD_EYE_R = (
    OFFSET_X + 230 * SCALE, OFFSET_Y + 230 * SCALE, 
    OFFSET_X + 290 * SCALE, OFFSET_Y + 270 * SCALE
)
COORD_NOSE = (
    OFFSET_X + 195 * SCALE, OFFSET_Y + 265 * SCALE, 
    OFFSET_X + 205 * SCALE, OFFSET_Y + 265 * SCALE, 
    OFFSET_X + 200 * SCALE, OFFSET_Y + 272 * SCALE
)
COORD_MOUTH_L = (
    OFFSET_X + 180 * SCALE, OFFSET_Y + 265 * SCALE, 
    OFFSET_X + 200 * SCALE, OFFSET_Y + 285 * SCALE
)
COORD_MOUTH_R = (
    OFFSET_X + 200 * SCALE, OFFSET_Y + 265 * SCALE, 
    OFFSET_X + 220 * SCALE, OFFSET_Y + 285 * SCALE
)
COORD_TONGUE = (
    OFFSET_X + 190 * SCALE, OFFSET_Y + 275 * SCALE, 
    OFFSET_X + 210 * SCALE, OFFSET_Y + 300 * SCALE
)
COORD_WHISK_L1 = (
    OFFSET_X + 70 * SCALE, OFFSET_Y + 260 * SCALE, 
    OFFSET_X + 30 * SCALE, OFFSET_Y + 270 * SCALE
)
COORD_WHISK_L2 = (
    OFFSET_X + 65 * SCALE, OFFSET_Y + 280 * SCALE, 
    OFFSET_X + 30 * SCALE, OFFSET_Y + 290 * SCALE
)
COORD_WHISK_R1 = (
    OFFSET_X + 330 * SCALE, OFFSET_Y + 260 * SCALE, 
    OFFSET_X + 370 * SCALE, OFFSET_Y + 270 * SCALE
)
COORD_WHISK_R2 = (
    OFFSET_X + 335 * SCALE, OFFSET_Y + 280 * SCALE, 
    OFFSET_X + 370 * SCALE, OFFSET_Y + 290 * SCALE
)
COORD_HEART = (
    OFFSET_X + 200 * SCALE, OFFSET_Y + 130 * SCALE, 
    OFFSET_X + 140 * SCALE, OFFSET_Y + 70 * SCALE, 
    OFFSET_X + 170 * SCALE, OFFSET_Y + 30 * SCALE, 
    OFFSET_X + 200 * SCALE, OFFSET_Y + 60 * SCALE, 
    OFFSET_X + 230 * SCALE, OFFSET_Y + 30 * SCALE, 
    OFFSET_X + 260 * SCALE, OFFSET_Y + 70 * SCALE, 
    OFFSET_X + 200 * SCALE, OFFSET_Y + 130 * SCALE
)

def main():
    canvas = Canvas(WIDTH, HEIGHT, "caty")

    # 1. Tail
    canvas.create_arc(*COORD_TAIL, start=ARC_START_TOP, extent=ARC_HALF, style="arc", outline=COLOR_BLACK, width=W_THICK)
    canvas.create_arc(*COORD_TAIL, start=ARC_START_BOTTOM, extent=ARC_TAIL_TIP, style="arc", outline=COLOR_PINK, width=W_TAIL_PINK)

    # 2. Ears
    canvas.create_polygon(*COORD_EAR_L_OUTER, fill=COLOR_WHITE, outline=COLOR_BLACK, width=W_OUTLINE)
    canvas.create_polygon(*COORD_EAR_L_INNER, fill=COLOR_PINK, outline=COLOR_BLACK, width=W_THIN)
    canvas.create_polygon(*COORD_EAR_R_OUTER, fill=COLOR_WHITE, outline=COLOR_BLACK, width=W_OUTLINE)
    canvas.create_polygon(*COORD_EAR_R_INNER, fill=COLOR_PINK, outline=COLOR_BLACK, width=W_THIN)

    # 3. Body
    canvas.create_oval(*COORD_BODY, fill=COLOR_WHITE, outline=COLOR_BLACK, width=W_OUTLINE)

    # 4. Paws
    canvas.create_arc(*COORD_PAW_L, start=ARC_START_RIGHT, extent=ARC_HALF, fill=COLOR_WHITE, outline=COLOR_BLACK, width=W_PAW)
    canvas.create_arc(*COORD_PAW_M, start=ARC_START_RIGHT, extent=ARC_HALF, fill=COLOR_WHITE, outline=COLOR_BLACK, width=W_PAW)
    canvas.create_arc(*COORD_PAW_R, start=ARC_START_RIGHT, extent=ARC_HALF, fill=COLOR_WHITE, outline=COLOR_BLACK, width=W_PAW)

    # 5. Head
    canvas.create_oval(*COORD_HEAD, fill=COLOR_WHITE, outline=COLOR_BLACK, width=W_OUTLINE)

    # 6. Face Details
    canvas.create_oval(*COORD_CHEEK_L, fill=COLOR_PINK, outline=COLOR_PINK)
    canvas.create_oval(*COORD_CHEEK_R, fill=COLOR_PINK, outline=COLOR_PINK)
    canvas.create_arc(*COORD_EYE_L, start=ARC_START_RIGHT, extent=ARC_HALF, style="arc", outline=COLOR_BLACK, width=W_EYE)
    canvas.create_arc(*COORD_EYE_R, start=ARC_START_RIGHT, extent=ARC_HALF, style="arc", outline=COLOR_BLACK, width=W_EYE)
    canvas.create_polygon(*COORD_NOSE, fill=COLOR_WHITE, outline=COLOR_BLACK, width=W_TINY)
    canvas.create_arc(*COORD_MOUTH_L, start=ARC_START_BOTTOM, extent=ARC_HALF, style="arc", outline=COLOR_BLACK, width=W_THIN)
    canvas.create_arc(*COORD_MOUTH_R, start=ARC_START_BOTTOM, extent=ARC_HALF, style="arc", outline=COLOR_BLACK, width=W_THIN)
    canvas.create_arc(*COORD_TONGUE, start=ARC_START_BOTTOM, extent=ARC_HALF, fill=COLOR_PINK, outline=COLOR_BLACK, width=W_THIN)

    # 7. Whiskers
    canvas.create_line(*COORD_WHISK_L1, width=W_THIN)
    canvas.create_line(*COORD_WHISK_L2, width=W_THIN)
    canvas.create_line(*COORD_WHISK_R1, width=W_THIN)
    canvas.create_line(*COORD_WHISK_R2, width=W_THIN)

    # 8. Floating Heart
    canvas.create_polygon(*COORD_HEART, fill=COLOR_DARK_PINK, outline=COLOR_BLACK, width=W_PAW, smooth=True)

    canvas.mainloop()

main()