from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QLabel, QPushButton, QSlider, \
    QProgressBar, QComboBox, QSpinBox

import image_processing
import resolution_events
from scroll_label import ScrollLabel


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_paths = []
        self.images = []
        self.converted_images = []
        self.modus_radios = []
        self.progress = 0
        self.resolution = [40, 0, 0, 0]
        self.modus_index = 0
        self.input_widgets = []

        self.setMinimumSize(QSize(600, 250))
        self.setWindowTitle('Kirsch image filter')

        wid = QWidget(self)
        self.setCentralWidget(wid)
        grid = QGridLayout()
        wid.setLayout(grid)

        current_row = 0

        file_label = QLabel('Files')
        grid.addWidget(file_label, current_row, 2, Qt.AlignCenter)

        self.path_scroll_label = ScrollLabel()
        grid.addWidget(self.path_scroll_label, current_row, 3)

        self.file_select_button = QPushButton('Select Files')
        self.file_select_button.clicked.connect(self.select)
        self.input_widgets.append(self.file_select_button)
        grid.addWidget(self.file_select_button, current_row, 4, Qt.AlignCenter)

        current_row += 1

        self.resolution_dropdown = QComboBox()
        self.resolution_dropdown.addItem('Percent')
        self.resolution_dropdown.addItem('Pixel Count')
        self.resolution_dropdown.addItem('Width')
        self.resolution_dropdown.addItem('Height')
        self.resolution_dropdown.currentIndexChanged.connect(self.dropdown_select)
        self.resolution_dropdown.setEnabled(False)
        self.input_widgets.append(self.resolution_dropdown)
        grid.addWidget(self.resolution_dropdown, current_row, 2, Qt.AlignRight)

        self.resolution_slider = QSlider(Qt.Horizontal)
        self.resolution_slider.setMinimum(1)
        self.resolution_slider.setMaximum(100)
        self.resolution_slider.setValue(40)
        self.resolution_slider.valueChanged.connect(self.slider_changed)
        self.input_widgets.append(self.resolution_slider)
        grid.addWidget(self.resolution_slider, current_row, 3)

        self.resolution_spin_box = QSpinBox()
        self.resolution_spin_box.setMinimum(1)
        self.resolution_spin_box.setMaximum(100)
        self.resolution_spin_box.setSuffix('%')
        self.resolution_spin_box.setValue(40)
        self.resolution_spin_box.setSingleStep(10)
        self.resolution_spin_box.valueChanged.connect(self.spin_box_changed)
        self.input_widgets.append(self.resolution_spin_box)
        grid.addWidget(self.resolution_spin_box, current_row, 4)

        current_row += 1

        self.progress_bar = QProgressBar()
        grid.addWidget(self.progress_bar, current_row, 3)

        current_row += 1

        self.current_process_label = QLabel()
        grid.addWidget(self.current_process_label, current_row, 3, Qt.AlignCenter)

        current_row += 1

        self.convert_button = QPushButton('Convert')
        self.convert_button.clicked.connect(self.convert)
        self.convert_button.setEnabled(False)
        self.input_widgets.append(self.convert_button)
        grid.addWidget(self.convert_button, current_row, 2, Qt.AlignCenter)

        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.save)
        self.save_button.setEnabled(False)
        self.input_widgets.append(self.save_button)
        grid.addWidget(self.save_button, current_row, 3, Qt.AlignCenter)

        quit_button = QPushButton('Exit')
        quit_button.clicked.connect(self.quit)
        grid.addWidget(quit_button, current_row, 4, Qt.AlignCenter)

        for i in range(5):
            grid.setRowStretch(i, 1)
        grid.setRowStretch(0, 5)
        grid.setColumnStretch(3, 5)
        grid.setColumnStretch(4, 1)

    def quit(self):
        self.close()

    def add_progress(self, amount):
        self.progress += amount
        self.progress_bar.setValue(self.progress)

    def select(self):
        image_processing.select_files(self)

    def convert(self):
        image_processing.convert_image(self)

    def save(self):
        image_processing.save_converted_images(self)

    def dropdown_select(self, index: int):
        resolution_events.dropdown_select(self, index)

    def slider_changed(self, value: int):
        resolution_events.slider_changed(self, value)

    def spin_box_changed(self, value: int):
        resolution_events.spin_box_changed(self, value)
