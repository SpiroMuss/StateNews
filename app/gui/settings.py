from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit

from constants import constants
from functions import show_config_items


class SettingsScreen(QWidget):
    def __init__(self, switch_callback):
        super().__init__()

        main_layout = QVBoxLayout()

        settings_layout = QHBoxLayout()

        staff_layout = QVBoxLayout()
        show_config_items(constants.staff, staff_layout)
        settings_layout.addLayout(staff_layout)

        list_marks_layout = QVBoxLayout()
        show_config_items(constants.list_marks, list_marks_layout)
        settings_layout.addLayout(list_marks_layout)

        activity_layout = QVBoxLayout()
        show_config_items(constants.activity, activity_layout)
        settings_layout.addLayout(activity_layout)

        main_layout.addLayout(settings_layout)

        button_layout = QHBoxLayout()

        self.main_button = QPushButton("Назад")
        self.main_button.clicked.connect(switch_callback)
        button_layout.addWidget(self.main_button)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
