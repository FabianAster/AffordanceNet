from PIL import Image, ImageDraw

# Open the image for editing
image = Image.open('0.png')
draw = ImageDraw.Draw(image)

# Open the bounding boxes file for reading
with open('0.txt', 'r') as f:
    # Loop through each line in the file
    for line in f:
        # Split the line into class and bounding box coordinates
        class_id, x, y, w, h = map(float, line.strip().split())

        # Calculate the pixel coordinates of the bounding box
        width, height = image.size
        left = int((x - w / 2) * width)
        top = int((y - h / 2) * height)
        right = int((x + w / 2) * width)
        bottom = int((y + h / 2) * height)

        # Draw the bounding box on the image
        draw.rectangle((left, top, right, bottom), outline='red', width=2)

# Save the edited image
image.save('output.png')