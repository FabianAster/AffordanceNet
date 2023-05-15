import xml.etree.ElementTree as ET
import shutil
from os import walk
import re

if __name__ == '__main__':
    src_dir = '/home/fabian/31_TrainingImages/training_set/imgs'
    dest_dir = '/home/fabian/31_TrainingImages/data/VOCdevkit2012/VOC2012/JPEGImages'
    filname_arr_with_masks = []


    filenames = next(walk(src_dir), (None, None, []))[2]  # [] if no file
    
    
    for filename in filenames:
        if "mask" in filename:
            filname_arr_with_masks.append(re.findall(r'\d+',filename)[0])
          
    print(filname_arr_with_masks)

    counter = 0
    for filename_no_end in filname_arr_with_masks:
        filename = filename_no_end + ".png"
        file_counter = int(filename[:-4])
        shutil.copyfile(src_dir+"/"+filename, dest_dir+"/"+filename)
        print("copied file " + filename)
        counter += 1