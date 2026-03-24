"""
File: darken.py
----------------
This program accepts an image file and
darkens the image by decreasing its
RGB values by half.
"""

from simpleimage import SimpleImage

def darken(image):
	"""
	This function takes in an image and "darkens" it by halving
	the individual RGB components of each pixel in the image.

	Parameters:
		* image: SimpleImage representing the image to manipulate

	Return:
		None
	"""

	for pixel in image:
		pixel.red = pixel.red // 2
		pixel.green = pixel.green // 2
		pixel.blue = pixel.blue // 2

def main():
	image = SimpleImage("stanford.jpg")
	darken(image)
	image.show()

if __name__ == "__main__":
	main()