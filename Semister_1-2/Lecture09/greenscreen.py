"""
File: greenscreen.py
--------------------
This program places an image behind
a green-screen image using SimpleImage.
"""

from simpleimage import SimpleImage


BACKGROUND_FILE = "stanford.jpg"
FOREGROUND_FILE = "greenscreen.jpg"
INTENSITY_THRESHOLD = 1.5


def greenscreen(foreground_fn, background_fn):
    foreground = SimpleImage(foreground_fn)
    background = SimpleImage(background_fn, foreground.width, foreground.height)
    for pixel in foreground:
        average = (pixel.red + pixel.green + pixel.blue) // 3
        # See if this pixel is "sufficiently" green
        if pixel.green >= average * INTENSITY_THRESHOLD:
            x = pixel.x
            y = pixel.y
            foreground.set_pixel(x, y, background.get_pixel(x, y))
    return foreground
    

def main():
	image = greenscreen(FOREGROUND_FILE, BACKGROUND_FILE)
	image.show()


if __name__ == "__main__":
	main()
