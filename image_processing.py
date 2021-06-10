import os

from PIL import Image, UnidentifiedImageError
from PyQt5.QtWidgets import QFileDialog

from image import Picture


def select_files(self):
    self.file_paths, _ = QFileDialog.getOpenFileNames(self, 'Select Image', filter='Image Files (*.png *.jpg)')
    if not len(self.file_paths):
        return
    for widget in self.input_widgets:
        widget.setEnabled(False)
    label_text = ''
    self.progress_bar.setMaximum(len(self.file_paths))
    self.progress = 0
    self.images = []
    self.converted_images = []
    for file_path in self.file_paths:
        self.current_process_label.setText(os.path.basename(file_path))
        try:
            pillow_image = Image.open(file_path)
            image = Picture(pillow_image, file_path)
            self.images.append(image)
            label_text = label_text + str(file_path) + '\n'
            self.path_scroll_label.setText(label_text)
        except UnidentifiedImageError:
            pass
        self.add_progress(1)
    self.current_process_label.setText('everything loaded ✔️')
    for widget in [self.file_select_button,
                   self.resolution_dropdown, self.resolution_slider, self.resolution_spin_box,
                   self.convert_button]:
        widget.setEnabled(True)


def convert_image(self):
    for widget in self.input_widgets:
        widget.setEnabled(False)
    self.converted_images = []
    self.progress_bar.setMaximum(25 * len(self.images))
    self.progress = 0
    for image in self.images:
        self.current_process_label.setText(os.path.basename(image.path))
        image.resize(self.resolution)
        self.add_progress(1)
        image.create_reshaped_arr()
        self.add_progress(1)
        image.convert_to_i1_i2_i3_colors()
        self.add_progress(1)
        for i in range(len(Picture.masks)):
            image.calculate_averages(i)
            self.add_progress(3)
        image.calculate_optimal_orientations()
        self.add_progress(1)
        image.recreate_individual_pixels()
        self.add_progress(1)
        image.convert_to_rgb_colors()
        self.add_progress(1)
        converted_image = image.recreate()
        self.converted_images.append(converted_image)
        self.add_progress(1)
    self.current_process_label.setText('everything converted ✔️')
    for widget in [self.file_select_button,
                   self.resolution_dropdown, self.resolution_slider, self.resolution_spin_box,
                   self.convert_button, self.save_button]:
        widget.setEnabled(True)


def save_converted_images(self):
    for widget in self.input_widgets:
        widget.setEnabled(False)
    self.progress_bar.setMaximum(len(self.file_paths))
    self.progress = 0
    directory = QFileDialog.getExistingDirectory()
    for i in range(len(self.file_paths)):
        old_file_path = self.file_paths[i]
        file_name = os.path.basename(old_file_path)
        file_name, _ = os.path.splitext(file_name)
        self.current_process_label.setText(file_name)
        out_path = directory + '/' + file_name + ".png"
        converted_image = self.converted_images[i]
        try:
            converted_image.save(out_path)
            self.add_progress(1)
        except PermissionError:
            self.progress_bar.setValue(len(self.file_paths))
            self.current_process_label.setText('saving cancelled')
            for widget in [self.resolution_dropdown, self.resolution_slider, self.resolution_spin_box,
                           self.convert_button, self.save_button]:
                widget.setEnabled(True)
            return
        for widget in [self.file_select_button,
                       self.resolution_dropdown, self.resolution_slider, self.resolution_spin_box,
                       self.convert_button, self.save_button]:
            widget.setEnabled(True)
        self.current_process_label.setText('everything saved ✔️')
