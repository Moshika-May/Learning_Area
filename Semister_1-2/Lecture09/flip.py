"""
File: flip.py
-------------
This program loads stanford.jpg and
creates a horizontally flipped copy
using SimpleImage.
"""

from simpleimage import SimpleImage


def flip_horizontal(image):
	"""
	Returns a new SimpleImage that is a horizontal
	mirror of the given image.
	"""
	flipped = SimpleImage.blank(image.width, image.height)

	# TODO: Write this function!
	
	return flipped


def main():
	image = SimpleImage("stanford.jpg")
	flipped = flip_horizontal(image)
	flipped.show()


if __name__ == "__main__":
	main()
