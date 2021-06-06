import numpy as np
from PIL import Image
import os
import shutil

dim = 40
network_dim = dim ** 2
fonts = [16, 32, 64]
errors = [10, 30, 60]


class Hopfield:
    def __init__(self):
        self.weights = np.zeros((network_dim, network_dim))

    def update_weights(self, input_patterns):
        shape = len(input_patterns[0])
        for i in range(len(input_patterns)):
            input_patterns[i] = np.array([input_patterns[i]])
        for pattern in input_patterns:
            self.weights += pattern * pattern.T
        self.weights = self.weights - len(input_patterns) * np.identity(shape)

    def train(self):
        temp_pattern = []
        for font in fonts:
            path = './original/' + str(font) + '/'
            dir = os.listdir(path)

            for photo_path in dir:
                image_matrix, image_size = read_image(path + photo_path)
                image_matrix = image_matrix.flatten()
                image_matrix = image_matrix.tolist()
                temp_pattern.append(image_matrix)
        self.update_weights(temp_pattern)

    def recover(self, input_pattern):
        np_pattern = np.array(input_pattern)
        np_pattern = sign(np.dot(self.weights, np_pattern))
        return np.array(np_pattern, dtype='uint8')

    def feed(self):
        for error in errors:
            for font in fonts:
                path = './noisy/' + str(error) + '/' + str(font) + '/'
                result_path = 'recovered/' + str(error) + '/' + str(font) + '/'
                if not os.path.exists(result_path):
                    os.makedirs(result_path)
                else:
                    shutil.rmtree(result_path)
                    os.makedirs(result_path)
                dir = os.listdir(path)
                for photo_path in dir:
                    image_matrix, image_size = read_image(path + photo_path)
                    image_matrix = image_matrix.flatten()
                    image_matrix = image_matrix.tolist()
                    output = self.recover(image_matrix)
                    output = np.reshape(output, (dim, dim))
                    output = Image.fromarray(output, mode='L').resize(image_size)
                    output.save(result_path + photo_path)


def read_image(path):
    img = Image.open(path).convert(mode="L")
    size = img.size
    img = img.resize((dim, dim))
    imgArray = np.asarray(img, dtype=np.uint8)
    x = np.zeros(imgArray.shape, dtype=np.float)
    x[imgArray > 60] = 1
    x[x == 0] = -1
    return x, size


def sign(np_pattern):
    for i in range(len(np_pattern)):
        if np_pattern[i] < 0:
            np_pattern[i] = 0
        else:
            np_pattern[i] = 255
    return np_pattern


if __name__ == '__main__':
    hopfield = Hopfield()
    hopfield.train()

    hopfield.feed()
