from PIL import Image, ImageFont
import os
import shutil
import numpy as np
import random
import cv2

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

def add_noise(image, noise):
    output = np.zeros(image.shape, np.uint8)
    thres = 1 - noise
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < noise:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output

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
                im.save(image_path + char + '.bmp')
                builded_image = cv2.imread(image_path + char + '.bmp')
                noisy_image = add_noise(builded_image, error / 100)
                cv2.imwrite(image_path + char + '.bmp', noisy_image)


if __name__ == '__main__':
    generate_original_images()
    generate_noisy_images()

