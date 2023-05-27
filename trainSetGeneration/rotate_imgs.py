import cv2
import os
import xml.etree.ElementTree as ET
import numpy as np
import math

def rotate_bounding_boxes(scaling_factor, counter, xml_path_src, xml_path_dest, angle, img_width, img_height):
    tree = ET.parse(xml_path_src)
    root = tree.getroot()

    # TODO: add counter into xml file
    root.find("filename").text = str(counter) + ".jgp"
    
    # Loop through all bounding boxes and rotate the coordinates
    for obj in root.findall('object'):
        bbox = obj.find('bndbox')
        xmin = int(bbox.find('xmin').text) * scaling_factor
        ymin = int(bbox.find('ymin').text) * scaling_factor
        xmax = int(bbox.find('xmax').text) * scaling_factor
        ymax = int(bbox.find('ymax').text) * scaling_factor

        rotated_xmin, rotated_xmax, rotated_ymin, rotated_ymax = rotate_bounding_box(xmin, xmax, ymin, ymax, img_width, img_height, angle)

        if (rotated_xmax < rotated_xmin):
          print("min greater than max")
          return -1

        if (rotated_ymax < rotated_ymin):
          print("min greater than max")
          return -1

        if (rotated_xmax < 0):
          print("negative_value")
          return -1

        if (rotated_xmin < 0):
          print("negative_value")
          return -1

        if (rotated_ymax < 0):
          print("negative_value")
          return -1

        if (rotated_ymin < 0):
          print("negative_value")
          return -1

        if (rotated_xmax > 479 * scaling_factor):
          print("value too large")
          return -1

        if (rotated_xmin > 479 * scaling_factor):
          print("value too large")
          return -1

        if (rotated_ymax > 479 * scaling_factor):
          print("value too large")
          return -1

        if (rotated_ymin > 479 * scaling_factor):
          print("value too large")
          return -1

        # Update bounding box coordinates in XML
        bbox.find('xmin').text = str(int(round(rotated_xmin)))
        bbox.find('ymin').text = str(int(round(rotated_ymin)))
        bbox.find('xmax').text = str(int(round(rotated_xmax)))
        bbox.find('ymax').text = str(int(round(rotated_ymax)))
        
    # Write the modified XML file
    tree.write(xml_path_dest)

def scale_up_image(input_img, scale_factor = 3):
    width = input_img.shape[1]
    height = input_img.shape[0]
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    
    # Upscale the image using cv2.resize with the nearest neighbor interpolation
    return cv2.resize(input_img, (new_width, new_height), interpolation=cv2.INTER_NEAREST)

def rotate_image(scaling_factor, img_path_src, img_path_dest, angle):
    img = cv2.imread(img_path_src)
    img = scale_up_image(img, scale_factor=scaling_factor)
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_img = cv2.warpAffine(img, M, (w, h))
    cv2.imwrite(img_path_dest, rotated_img)

def rotate_bounding_box(x_min, x_max, y_min, y_max, image_width, image_height, angle):
    # Calculate the center of the bounding box
    center_x = (image_width) / 2
    center_y = (image_height) / 2
    # calculate offset to move venter of image to top left corner

    # move all coordinates
    # rotate
    angle_rad = math.radians(-angle)
    
    # Convert the angle to radians
    x_min -= center_x
    x_max -= center_x
    y_min -= center_y
    y_max -= center_y


    cord_1 = [x_min, y_min]
    cord_2 = [x_min, y_max]
    cord_3 = [x_max, y_min]
    cord_4 = [x_max, y_max]

    rotation_matrix = np.array([[math.cos(angle_rad), -math.sin(angle_rad)],
                                [math.sin(angle_rad), math.cos(angle_rad)]])
    
    cord_1 = np.dot(rotation_matrix, np.array(cord_1))
    cord_2 = np.dot(rotation_matrix, np.array(cord_2))
    cord_3 = np.dot(rotation_matrix, np.array(cord_3))
    cord_4 = np.dot(rotation_matrix, np.array(cord_4))
    
    y_max = max(cord_1[1], cord_2[1], cord_3[1], cord_4[1])
    y_min = min(cord_1[1], cord_2[1], cord_3[1], cord_4[1])
    x_max = max(cord_1[0], cord_2[0], cord_3[0], cord_4[0])
    x_min = min(cord_1[0], cord_2[0], cord_3[0], cord_4[0])

    x_min += center_x
    x_max += center_x
    y_min += center_y
    y_max += center_y

    # Return the rotated bounding box coordinates
    return x_min, x_max, y_min, y_max