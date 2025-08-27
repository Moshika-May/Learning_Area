filenames = ["photo.jpg", "document.pdf", "image.png", "video.mp4", "graphic.gif"]
image_files = []

# Iterate over each file in the list of filenames
for file in filenames:
    # Check if the file ends with one of the specified image extensions
    if file.endswith(('.jpg', '.png', '.gif')):
        image_files.append(file)  

print("Image files:", image_files)  