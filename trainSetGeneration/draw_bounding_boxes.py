import cv2
import xml.etree.ElementTree as ET

def draw_bounding_boxes(image_path, xml_path, output_path):
    # Read image
    img = cv2.imread(image_path)

    # Parse XML file
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Loop through bounding boxes in XML and draw them on the image
    for obj in root.findall('object'):
        bbox = obj.find('bndbox')
        xmin = int(bbox.find('xmin').text)
        ymin = int(bbox.find('ymin').text)
        xmax = int(bbox.find('xmax').text)
        ymax = int(bbox.find('ymax').text)

        # Draw bounding box rectangle on the image
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

    # Save the image with bounding boxes
    cv2.imwrite(output_path, img)

draw_bounding_boxes("/home/fabian/31_TrainingImages/training_set/imgs_generated/1083.jpg", "/home/fabian/31_TrainingImages/training_set/xml_generated/1083.xml", "./test1.png")