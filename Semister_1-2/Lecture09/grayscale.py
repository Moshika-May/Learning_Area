"""
File: grayscale.py
------------------
This program accepts an image file and
grayscales it by computing the luminosity
of each pixel.
"""

from simpleimage import SimpleImage

def compute_luminosity(red, green, blue):
	return (0.299 * red) + (0.587 * green) + (0.114 * blue)

def main():
	image = SimpleImage("stanford.jpg")
	for pixel in image:
		luminosity = compute_luminosity(pixel.red, pixel.green, pixel.blue)
		pixel.red = luminosity
		pixel.green = luminosity
		pixel.blue = luminosity

	image.show()

if __name__ == "__main__":
	main()