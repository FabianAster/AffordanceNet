import xml.etree.ElementTree as ET 
import cv2

def mirror_xml(source_path, destination_path, img_width):
    # Parse XML file
    tree = ET.parse(source_path)
    root = tree.getroot()

    # Mirror bounding boxes in XML
    for obj in root.findall('object'):
        bbox = obj.find('bndbox')
        xmin = int(bbox.find('xmin').text)
        xmax = int(bbox.find('xmax').text)

        # Mirror bounding box coordinates
        mirrored_xmin = img_width - xmax
        mirrored_xmax = img_width - xmin

        # Update bounding box coordinates in XML
        bbox.find('xmin').text = str(mirrored_xmin)
        bbox.find('xmax').text = str(mirrored_xmax)

    # Save the modified XML to the destination path
    tree.write(destination_path)


def mirror_image(source_path, destination_path):
    # Read image
    img = cv2.imread(source_path)

    # Mirror image
    mirrored_img = cv2.flip(img, 1)

    # Save the mirrored image to the destination path
    cv2.imwrite(destination_path, mirrored_img)