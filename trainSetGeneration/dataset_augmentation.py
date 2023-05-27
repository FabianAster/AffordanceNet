import os
from mirror_imgs import *
from rotate_imgs import *
import xml.etree.ElementTree as ET

def apply_transformations(scaling_factor, counter, dir_img_src, dir_img_dest, dir_xml_src, dir_xml_dest, dir_mask_src, dir_mask_dest, angle, img_width, img_height):
    for filename in os.listdir(dir_img_src):
        if filename.endswith('.png'):
            counter += 1
            image_path_src = os.path.join(dir_img_src, filename)
            image_path_dest = os.path.join(dir_img_dest, str(counter)+".jpg")

            xml_path_src = os.path.join(dir_xml_src, filename.replace('.png', '.xml'))
            xml_path_dest = os.path.join(dir_xml_dest, str(counter)+".xml")
            
            # Extract the number of objects from XML
            num_objects = get_num_objects(xml_path_src)

            # Apply rotation transformation
            if(rotate_bounding_boxes(scaling_factor, counter, xml_path_src, xml_path_dest, angle, img_width, img_height) != -1):
              rotate_image(scaling_factor, image_path_src, image_path_dest, angle)
              rotate_masks(scaling_factor, dir_mask_src, dir_mask_dest, counter, filename, angle, num_objects)
              counter+=1

              image_path_dest = os.path.join(dir_img_dest, str(counter)+".jpg")
              image_path_src = os.path.join(dir_img_dest, str(counter-1)+".jpg")
              xml_path_src = os.path.join(dir_xml_dest, str(counter-1)+".xml")
              xml_path_dest = os.path.join(dir_xml_dest, str(counter)+".xml")
              
              # Apply mirror transformation
              mirror_image(scaling_factor, image_path_src, image_path_dest)
              mirror_xml(scaling_factor, counter, xml_path_src, xml_path_dest, image_width)
              mirror_masks(scaling_factor, dir_mask_dest, dir_mask_dest, counter, filename, num_objects)
            else:
              print("skipped")

            
    return counter

# Function to extract the number of objects from XML
def get_num_objects(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    return len(root.findall('object'))

# Function to mirror the masks
def mirror_masks(scaling_factor, src_dir, dest_dir, counter, filename, num_objects):
    for i in range(1, num_objects + 1):
        mask_filename = f"{counter-1}_{i}_segmask.png"
        mask_filename_dest = f"{counter}_{i}_segmask.png"
        mask_path_src = os.path.join(src_dir, mask_filename)
        mask_path_dest = os.path.join(dest_dir, mask_filename_dest)
        
        # Apply mirror transformation to mask
        mirror_image(scaling_factor, mask_path_src, mask_path_dest)

# Function to rotate the masks
def rotate_masks(scaling_factor, src_dir, dest_dir, counter, filename, angle, num_objects):
    base_name = os.path.splitext(filename)[0]
    for i in range(1, num_objects + 1):
        mask_filename = f"{base_name}_{i}_segmask.png"
        mask_filename_dest = f"{counter}_{i}_segmask.png"
        mask_src_dir = os.path.join(src_dir, mask_filename)
        mask_dest_dir = os.path.join(dest_dir, mask_filename_dest)
        
        # Apply rotation transformation to mask
        rotate_image(scaling_factor, mask_src_dir, mask_dest_dir, angle)

# Example usage
imgs_src = '/home/fabian/31_TrainingImages/training_set/imgs_clean'
imgs_dest = '/home/fabian/31_TrainingImages/training_set/imgs_generated'

xml_src = '/home/fabian/31_TrainingImages/training_set/xml'
xml_dest = '/home/fabian/31_TrainingImages/training_set/xml_generated'

mask_src = '/home/fabian/31_TrainingImages/training_set/masks'
mask_dest = '/home/fabian/31_TrainingImages/training_set/masks_generated'

image_width = 480
image_height = 480


counter = 0

for angle in range(0, 360, 10):
    print(str(angle) + " done")
    counter = apply_transformations(1, counter, imgs_src, imgs_dest, xml_src, xml_dest, mask_src, mask_dest, angle, image_height, image_width)
    counter+=1