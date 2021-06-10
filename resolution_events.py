import math


def dropdown_select(self, index: int):
    maximum_slider_values = [100,
                             10 * min([int(math.log(image.p_width * image.p_height / 36)) for image in self.images]),
                             min([image.p_width // 6 for image in self.images]),
                             min([image.p_height // 6 for image in self.images])]
    maximum_spin_box_values = [100, min([image.p_width * image.p_height // 36 for image in self.images]),
                               min([image.p_width // 6 for image in self.images]),
                               min([image.p_height // 6 for image in self.images])]
    self.resolution_slider.setMaximum(maximum_slider_values[index])
    self.resolution_spin_box.setMaximum(maximum_spin_box_values[index])
    self.resolution_spin_box.setSuffix('%' if index == 0 else '')
    self.resolution_spin_box.valueChanged.disconnect()
    self.resolution_spin_box.setValue(int(math.e ** (self.resolution_slider.value() / 10)) if index == 1
                                      else self.resolution_slider.value())
    self.resolution_spin_box.valueChanged.connect(self.spin_box_changed)
    self.resolution = [0, 0, 0, 0]
    self.resolution[index] = self.resolution_slider.value() if self.resolution_dropdown.currentIndex() != 1 \
        else int(math.e ** (self.resolution_slider.value() / 10))


def slider_changed(self, value):
    value = value if self.resolution_dropdown.currentIndex() != 1 else int(math.e ** (value / 10))
    self.resolution = [0, 0, 0, 0]
    self.resolution[self.resolution_dropdown.currentIndex()] = value
    self.resolution_spin_box.valueChanged.disconnect()
    self.resolution_spin_box.setValue(value)
    self.resolution_spin_box.valueChanged.connect(self.spin_box_changed)


def spin_box_changed(self, value):
    self.resolution = [0, 0, 0, 0]
    self.resolution[self.resolution_dropdown.currentIndex()] = value
    self.resolution_slider.valueChanged.disconnect()
    self.resolution_slider.setValue(value if self.resolution_dropdown.currentIndex() != 1
                                    else int(100 * math.log(value)))
    self.resolution_slider.valueChanged.connect(self.slider_changed)
