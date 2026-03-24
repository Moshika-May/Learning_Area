from graders.image_grader_utils import grade_image_transform


def _flip_horizontally(pixels):
    return [list(reversed(row)) for row in pixels]


def grade(student_file):
    return grade_image_transform(
        student_file,
        _flip_horizontally,
        "Great job! Your flip program correctly flips the image horizontally.",
        "flipped image",
    )
