import os.path
from math import sqrt

import numpy as np
from PIL import Image


class Picture:
    masks = np.array([(0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0,
                       1, 1, 1, 1, 1, 1,
                       1, 1, 1, 1, 1, 1,
                       1, 1, 1, 1, 1, 1),
                      (0, 0, 0, 1, 1, 1,
                       0, 0, 0, 1, 1, 1,
                       0, 0, 0, 1, 1, 1,
                       0, 0, 0, 1, 1, 1,
                       0, 0, 0, 1, 1, 1,
                       0, 0, 0, 1, 1, 1),
                      (0, 0, 0, 0, 1, 1,
                       0, 0, 0, 0, 1, 1,
                       0, 0, 0, 1, 1, 1,
                       0, 0, 0, 1, 1, 1,
                       0, 0, 1, 1, 1, 1,
                       0, 0, 1, 1, 1, 1),
                      (1, 1, 0, 0, 0, 0,
                       1, 1, 0, 0, 0, 0,
                       1, 1, 1, 0, 0, 0,
                       1, 1, 1, 0, 0, 0,
                       1, 1, 1, 1, 0, 0,
                       1, 1, 1, 1, 0, 0),
                      (0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 1, 1,
                       0, 0, 1, 1, 1, 1,
                       1, 1, 1, 1, 1, 1,
                       1, 1, 1, 1, 1, 1),
                      (0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0,
                       1, 1, 0, 0, 0, 0,
                       1, 1, 1, 1, 0, 0,
                       1, 1, 1, 1, 1, 1,
                       1, 1, 1, 1, 1, 1)
                      ], int)

    def __init__(self, pict, path):
        self._picture = pict.copy()
        self._picture = self._picture.convert('RGB')
        self._resized_picture = self._picture.copy()
        self.p_width = self._picture.size[0]
        self.p_height = self._picture.size[1]
        self.p_arr = None
        self.new_size = self._picture.size
        self.prop = self.p_height / self.p_width
        self._width = 0
        self._height = 0
        self._average_pairs = None
        self._optimal_indices = None
        self._optimal_average_pairs = None
        self.path = path
        self.name, _ = os.path.splitext(os.path.basename(path))

    def resize(self, resolution: list):
        if resolution[0]:
            self._width = int(self.p_width * resolution[0] / 600)
            self._height = int(self.p_height * resolution[0] / 600)
        elif resolution[1]:
            self._width = int(sqrt(resolution[1] / self.prop))
            self._height = int(sqrt(resolution[1] * self.prop))
        elif resolution[2]:
            self._width = int(resolution[2])
            self._height = int(resolution[2] * self.prop)
        else:
            self._height = int(resolution[3])
            self._width = int(resolution[3] / self.prop)
        self.new_size = np.array((self._width, self._height))
        self._resized_picture = self._picture.resize([val * 6 for val in self.new_size], resample=4)

    def create_reshaped_arr(self):
        self.p_arr = np.copy(np.asarray(self._resized_picture))
        self.p_arr = self.p_arr.reshape((int(self._height), 6, self._width, 6, 3))
        self.p_arr = self.p_arr.transpose((0, 2, 1, 3, 4))
        self.p_arr = self.p_arr.reshape((self.new_size.prod(), 36, 3))

    def convert_to_i1_i2_i3_colors(self):
        convert_matrix = np.array([[4, 6, -3],
                                   [4, 0, 6],
                                   [4, -6, -3]])
        self.p_arr = np.dot(self.p_arr, convert_matrix)
        self._average_pairs = np.zeros((self.new_size.prod(), len(Picture.masks), 2, 3))

    def calculate_averages(self, mask_index):
        self._average_pairs[:, mask_index, 0, :] = np.average(self.p_arr, 1, Picture.masks[mask_index])
        self._average_pairs[:, mask_index, 1, :] = np.average(self.p_arr, 1, 1 - Picture.masks[mask_index])

    def calculate_optimal_orientations(self):
        differences = np.abs(self._average_pairs[:, :, 0] - self._average_pairs[:, :, 1])
        differences_indexed = np.dot(differences ** 2, np.array((4, 1, 1), int))
        self._optimal_indices = np.argmax(differences_indexed, 1)
        self._optimal_average_pairs = np.take_along_axis(self._average_pairs,
                                                         self._optimal_indices[..., np.newaxis, np.newaxis, np.newaxis],
                                                         1)

    def get_compressed_array(self):
        image_arr = self._optimal_average_pairs + np.array([0, 6 * 128, 6 * 128])
        image_arr = image_arr.squeeze(1)
        image_arr = image_arr / np.array([12, 24, 24])
        image_arr[:, 0, 1] = image_arr[:, 0, 1] + (128 * (self._optimal_indices % 16) // 8)
        image_arr[:, 0, 2] = image_arr[:, 0, 2] + (128 * (self._optimal_indices % 8) // 4)
        image_arr[:, 1, 1] = image_arr[:, 1, 1] + (128 * (self._optimal_indices % 4) // 2)
        image_arr[:, 1, 2] = image_arr[:, 1, 2] + (128 * (self._optimal_indices % 2) // 1)
        return image_arr.astype('uint8')

    def recreate_individual_pixels(self):
        mask = np.take_along_axis(Picture.masks[np.newaxis, :, :], self._optimal_indices[:, np.newaxis, np.newaxis], 1)
        self.p_arr = np.take_along_axis(self._optimal_average_pairs, 1 - mask[..., np.newaxis], 2)

    def convert_to_rgb_colors(self):
        convert_matrix = np.array([[1 / 12, 1 / 12, 1 / 12],
                                   [1 / 12, 0, -1 / 12],
                                   [-1 / 18, 1 / 9, -1 / 18]])
        self.p_arr = np.dot(self.p_arr, convert_matrix)

    def recreate(self):
        self.p_arr = self.p_arr.reshape((self._height, self._width, 6, 6, 3))
        self.p_arr = self.p_arr.transpose((0, 2, 1, 3, 4))
        self.p_arr = self.p_arr.reshape(self._height * 6, self._width * 6, 3)
        converted_image = Image.fromarray(self.p_arr.astype(np.uint8))
        return converted_image
