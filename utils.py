from PIL import Image
import os
from rectpack import newPacker
from tqdm import tqdm
import math
accepted_extensions = (".jpg", ".jpeg", ".png")

def create_contact_sheet_no_crop(image_paths, output_file, img_size):
    images = []  # list to hold image objects
    sizes = []  # list to hold sizes of each image
    total_size = 0  # total size of all images
    if img_size == 0:
        img_size = len(image_paths)
    for filename in image_paths[0:img_size]:
        if filename.lower().endswith(accepted_extensions):
            img = Image.open(filename)
            images.append(img)
            sizes.append(img.size)
            total_size += img.size[0] * img.size[1]
            print("FINISHED1")

    # calculate the side of a square that can contain all images
    side = int(math.sqrt(total_size))
    # create a new packer
    packer = newPacker(rotation=False)

    # add the rectangles to packing queue
    for i, size in enumerate(sizes):
        packer.add_rect(*size, i) 
    print("FINISHED2")

    # add the bin (final image)
    packer.add_bin(side, side)

    # start packing
    print("Packing started, may take some time. Please wait...")
    packer.pack()

    # full bin packing
    all_rects = packer.rect_list()

    # create a blank canvas
    contact_sheet = Image.new('RGB', (side, side))
    print("FINISHED4")

    return contact_sheet,all_rects,images

