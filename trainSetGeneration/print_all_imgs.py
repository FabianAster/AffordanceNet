import xml.etree.ElementTree as ET
import shutil
from os import walk
import re

if __name__ == '__main__':
    src_dir = '/home/fabian/github/data/VOCdevkit2012/VOC2012/JPEGImages'
    filname_arr_with_masks = []


    filenames = next(walk(src_dir), (None, None, []))[2]  # [] if no file
    print(filenames)
    
    
    for filename in filenames:
        print(filename[:-4])