from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QFrame, QScrollArea

from constants import constants
from functions import show_config_items


class SettingsScreen(QWidget):
    def __init__(self, switch_callback):
        super().__init__()

        main_layout = QVBoxLayout()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        settings_widget = QWidget()
        settings_layout = QHBoxLayout(settings_widget)

        staff_frame = QFrame()
        staff_frame.setObjectName("group_frame")
        staff_layout = QVBoxLayout(staff_frame)
        show_config_items(constants.staff, staff_layout)
        settings_layout.addWidget(staff_frame)

        list_marks_frame = QFrame()
        list_marks_frame.setObjectName("group_frame")
        list_marks_layout = QVBoxLayout(list_marks_frame)
        show_config_items(constants.list_marks, list_marks_layout)
        settings_layout.addWidget(list_marks_frame)

        activity_frame = QFrame()
        activity_frame.setObjectName("group_frame")
        activity_layout = QVBoxLayout(activity_frame)
        show_config_items(constants.activity, activity_layout)
        settings_layout.addWidget(activity_frame)

        scroll_area.setWidget(settings_widget)
        main_layout.addWidget(scroll_area)

        button_layout = QHBoxLayout()

        self.main_button = QPushButton("Назад")
        self.main_button.clicked.connect(switch_callback)
        button_layout.addWidget(self.main_button)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.setStyleSheet('''
                    QFrame#item_frame {
                        border: 1px solid black;
                    }
                    QFrame#group_frame {
                        border: 2px solid black;
                    }
                ''')
