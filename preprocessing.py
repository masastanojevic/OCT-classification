import os
from collections import defaultdict
from PIL import Image

FILTER_DATASET_PATH = 'C:\\Users\\mstanojevic\\filtered_dataset'
CROP_DATASET_PATH = 'C:\\Users\\mstanojevic\\cropped_dataset'

# creates image dictionary where keys are image contents and values are image names
def create_image_dict(path):
    img_dict = defaultdict(list)

    for img_name in os.listdir(path):
        img = Image.open(os.path.join(path, img_name))
        img_dict[tuple(img.getdata())].append(img_name)

    return img_dict

# returns count of duplicates in dictionary
def count_duplicates(img_dict):
    return sum([len(v[1:]) for v in img_dict.values()])

# if multiple images have the same content they are duplicates
# only the first image is kept, the rest are deleted
def remove_duplicates(folder_path, img_dict):
    for key, value in img_dict.items():
        for img_name in value[1:]:
            os.remove(os.path.join(folder_path, img_name))

# filters duplicates for each folder
def filter_duplicates(dataset_path):
    cnt = []

    for f in os.listdir(dataset_path):
        folder_path = os.path.join(dataset_path, f)
        img_dict = create_image_dict(folder_path)
        cnt.append(count_duplicates(img_dict))
        remove_duplicates(folder_path, img_dict)
        del img_dict

    print(cnt)
    print('There are ' + str(sum(cnt)) + ' duplicates')

# returns distribution of different image sizes in dataset
def image_sizes(dataset_path):
    sizes_dict = {}

    for f in os.listdir(dataset_path):
        folder_path = os.path.join(dataset_path, f)
        for img_name in os.listdir(folder_path):
            img = Image.open(os.path.join(folder_path, img_name))
            sizes_dict[img.size] = sizes_dict.get(img.size, 0) + 1

    return sizes_dict

# crops images to given size by taking the center part of the image
def crop_images(dataset_path, size):
    for f in os.listdir(dataset_path):
        folder_path = os.path.join(dataset_path, f)
        for img_name in os.listdir(folder_path):
            img_path = os.path.join(folder_path, img_name)
            img = Image.open(img_path)

            # find smaller dimension
            width, height = img.size
            dim = min(width, height)

            # find top left corner
            x = (width - dim) / 2
            y = (height - dim) / 2

            # crop, resize and save
            img = img.crop((x, y, x + dim, y + dim))
            img = img.resize((size, size))
            img.save(img_path)

