import cv2
import numpy as np
import os
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

def draw_bounding_boxes(filename, image_path, xml_path, mask_path):
    # Read image
    img = cv2.imread(image_path +"/"+ filename + ".jpg")
    print("image loaded")

    # Parse XML file
    tree = ET.parse(xml_path + "/"+ filename + ".xml")
    root = tree.getroot()
    print("xml loaded")

    # Loop through bounding boxes in XML and draw them on the image
    counter = 0
    for obj in root.findall('object'):
        counter +=1
        bbox = obj.find('bndbox')
        xmin = int(bbox.find('xmin').text)
        ymin = int(bbox.find('ymin').text)
        xmax = int(bbox.find('xmax').text)
        ymax = int(bbox.find('ymax').text)

        # Draw bounding box rectangle on the image
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        
        # Draw mask on image
        
        mask_filename = f"{filename}_{counter}_segmask.png"
        mask = cv2.imread(mask_path+"/"+mask_filename, 0) 
        print(mask)
        # Reshape the grayscale image to have 3 channels
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

        output_image = np.zeros_like(mask)
        output_image[:, :, 0] = mask[:,:,0] * 100


        img = cv2.addWeighted(img, 1, output_image, 0.5, 0)
        
        

    
    
    
    # Save the image with bounding boxes
    print("show image")
    plt.imshow(img)
    plt.axis('off')  # Turn off the axis labels
    plt.show()
    

mask_dest = '/home/fabian/github/data/cache/GTsegmask_VOC_2012_train_images'
xml_dest = '/home/fabian/github/data/VOCdevkit2012/VOC2012/Annotations'
imgs_dest = '/home/fabian/github/data/VOCdevkit2012/VOC2012/JPEGImages'

for filename in os.listdir(imgs_dest):
    if filename.endswith('.jpg'):
        filename = filename[:-4]
        print(filename)
        draw_bounding_boxes(filename, imgs_dest, xml_dest, mask_dest)