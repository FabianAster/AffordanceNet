import cv2
import numpy as np

def scale_up_image(input_img, scale_factor):
    width = input_img.shape[1]
    height = input_img.shape[0]
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    
    # Upscale the image using cv2.resize with the nearest neighbor interpolation
    return cv2.resize(input_img, (new_width, new_height), interpolation=cv2.INTER_NEAREST)
    

# Usage example
input_path = "./0plot.png"
output_path = "scaled_up_image.jpg"
scale_factor = 3  # Change this value to scale the image up by a different factor

scale_up_image(input_path, output_path, scale_factor)