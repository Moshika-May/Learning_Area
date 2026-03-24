"""
File: rotate.py
---------------
This program loads stanford.jpg and
creates a copy rotated by 180 degrees
using SimpleImage.
"""

from simpleimage import SimpleImage


def rotate_180(image):
	"""
	Returns a new SimpleImage that is rotated
	180 degrees from the given image.
	"""
	rotated = SimpleImage.blank(image.width, image.height)

	# TODO: Write this function!
	return rotated


def main():
	image = SimpleImage("stanford.jpg")
	rotated = rotate_180(image)
	rotated.show()


if __name__ == "__main__":
	main()
