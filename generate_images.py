from PIL import Image, ImageFont
import os
import shutil
import numpy as np
import random

original_images_path = './original/'
noisy_images_path = './noisy/'
font_sizes = [16, 32, 64]
errors = [10, 30, 60]


def generate_original_images():
    # Make directories
    if not os.path.exists(original_images_path):
        os.makedirs(original_images_path)
    else:
        shutil.rmtree(original_images_path)
        os.makedirs(original_images_path)

    # Make images
    for font in font_sizes:
        image_path = original_images_path + str(font) + '/'
        if not os.path.exists(image_path):
            os.makedirs(image_path)
        arial_font = ImageFont.truetype("arial.ttf", font)
        for char in "ABCDEFGHIJ":
            im = Image.Image()._new(arial_font.getmask(char))
            im.save(image_path + char + '.bmp')


def generate_noisy_images():

    if not os.path.exists(noisy_images_path):
        os.makedirs(noisy_images_path)
    else:
        shutil.rmtree(noisy_images_path)
        os.makedirs(noisy_images_path)
    for error in errors:
        for font in font_sizes:
            image_path = noisy_images_path + str(error) + '/' + str(font) + '/'
            if not os.path.exists(image_path):
                os.makedirs(image_path)
            arial_font = ImageFont.truetype("arial.ttf", font)
            for char in "ABCDEFGHIJ":
                im = Image.Image()._new(arial_font.getmask(char))

                data = np.array(im)
                for i in data:
                    for j in range(len(i)):
                        r = random.randint(1, 10) / 10
                        if r <= error / 100:
                            i[j] = 0
                            rescaled = (255.0 / data.max() *
                                        (data - data.min())).astype(np.uint8)
                            im = Image.fromarray(rescaled)
                            im.save(image_path + char + '.bmp')


if __name__ == '__main__':
    generate_original_images()
    generate_noisy_images()

