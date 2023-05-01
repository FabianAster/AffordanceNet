import xml.etree.ElementTree as ET
from os import walk

object_dict = {0: "bowl", 1: "tvm", 2: "pan", 3: "hammer", 4: "knife", 5: "cup", 6: "drill", 7: "racket", 8: "spatula"}

def transform_to_xml(filename, src_dir, dest_dir):
    # Open the input file for reading

    with open(src_dir+"/"+filename, 'r') as f:
        # Create the root element of the XML tree
        root = ET.Element('annotation')
        folder = ET.SubElement(root, 'folder')
        folder.text = "IIT2017"
        filename_elem = ET.SubElement(root, 'filename')
        filename_elem.text = filename[:-4] + ".jpg"
        size = ET.SubElement(root, 'size')
        width = ET.SubElement(size, 'width')
        width.text = "480"
        height = ET.SubElement(size, 'height')
        height.text = "480"
        depth = ET.SubElement(size, 'depth')
        depth.text = "3"

        # Loop through each line in the input file
        for line in f:
            object = ET.SubElement(root, 'object')
            # Split the line into first name, last name, and age
            object_id, x, y, w, h = map(float, line.strip().split(' '))
            name = ET.SubElement(object, 'name')
            name.text = object_dict[object_id]

            pose = ET.SubElement(object, 'pose')
            pose.text = "Unspecified"

            truncated = ET.SubElement(object, 'truncated')
            truncated.text = "0"

            difficult = ET.SubElement(object, 'difficult')
            difficult.text = "0"

            # Calculate the pixel coordinates of the bounding box
            width, height = (480, 480)
            left = int((x - w / 2) * width)
            top = int((y - h / 2) * height)
            right = int((x + w / 2) * width)
            bottom = int((y + h / 2) * height)

            bndbox = ET.SubElement(object, 'bndbox')

            xmin = ET.SubElement(bndbox, 'xmin')
            xmin.text = str(min(left, right))

            ymin = ET.SubElement(bndbox, 'ymin')
            ymin.text = str(min(bottom, top))

            xmax = ET.SubElement(bndbox, 'xmax')
            xmax.text = str(max(right, left))

            ymax = ET.SubElement(bndbox, 'ymax')
            ymax.text = str(max(top, bottom))




    # Write the XML tree to a file
    tree = ET.ElementTree(root)
    ET.indent(tree, '  ')
    tree.write(dest_dir+"/"+filename[:-4]+".xml")
    
  
if __name__ == '__main__':
    src_dir = '/home/fabian/31_TrainingImages/training_set/labels'
    dest_dir = '/home/fabian/github/data/VOCdevkit2012/VOC2012/Annotations'


    filenames = next(walk(src_dir), (None, None, []))[2]  # [] if no file
    print(filenames)

    counter = 0
    for filename in filenames:
        transform_to_xml(filename, src_dir, dest_dir)