import os

import numpy as np
from PIL import Image

errors = [10, 30, 60]
fonts = [16, 32, 64]
accuracies = {
    '10_16': [],
    '10_32': [],
    '10_64': [],

    '30_16': [],
    '30_32': [],
    '30_64': [],

    '60_16': [],
    '60_32': [],
    '60_64': []
}

accuracy = {
    '10_16': 0,
    '10_32': 0,
    '10_64': 0,

    '30_16': 0,
    '30_32': 0,
    '30_64': 0,

    '60_16': 0,
    '60_32': 0,
    '60_64': 0
}


def read_image_path(path):
    img = Image.open(path).convert(mode="L")
    imgArray = np.asarray(img, dtype=np.uint8).flatten()
    x = np.zeros(imgArray.shape, dtype=np.float)
    x[imgArray > 60] = 1
    x[x == 0] = 0
    return x

def calculate_accuracies():
    for keyaccs, accs in accuracies.items():
        accuracy[keyaccs] = round(np.average(accs), 2)


if __name__ == '__main__':
    original_images_path = './original/'
    recovered_images_path = './recovered/'
    for font in fonts:
        image_path = original_images_path + str(font) + '/'

        images = os.listdir(image_path)
        for image in images:
            original_image = image_path + image
            open_image = read_image_path(original_image)
            for error in errors:
                recovered_image = recovered_images_path + str(error) + '/' + str(font) + '/' + image
                open_recovered_image = read_image_path(recovered_image)
                acc = 100 * (1 - np.average(np.abs(open_image - open_recovered_image)))
                accuracies[str(error) + '_' + str(font)].append(acc)

    calculate_accuracies()
    print(accuracy)

