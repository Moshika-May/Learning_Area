from graders.image_grader_utils import grade_image_transform


def _rotate_180(pixels):
    return [list(reversed(row)) for row in reversed(pixels)]


def grade(student_file):
    return grade_image_transform(
        student_file,
        _rotate_180,
        "Great job! Your rotate program correctly rotates the image by 180 degrees.",
        "rotated image",
    )
