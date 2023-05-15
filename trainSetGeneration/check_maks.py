from PIL import Image, ImageDraw
import time



# Open the image for editing
image_own = Image.open('../data/cache/GTsegmask_VOC_2012_train_images/0_1_segmask.png')
image_org = Image.open('../data_iit/cache/GTsegmask_VOC_2012_train_images/0_1_segmask.png')
width = 480
height = 480


pixels_own = image_own.load()
pixels_org = image_org.load()

# create a dictionary to store the output images
output_images = {}

# loop through each pixel in the input image
for x in range(width):
    for y in range(height):
        # get the color value for the current pixel
        color = pixels_own[x, y]
        if(not color == 0):
            print(color)
          

print("sleep now")
time.sleep(10)
          

width = 1024
height = 1024

# loop through each pixel in the input image
for x in range(width):
    for y in range(height):
        # get the color value for the current pixel
        color = pixels_org[x, y]
        if(not color == 0 and not color == 5):
            print(color)