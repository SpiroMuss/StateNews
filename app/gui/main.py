from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QFrame, QComboBox
from datetime import datetime

from functions import get_clipboard_data, time_sorting
from app.config import system, config


class MainScreen(QWidget):
    def __init__(self, switch_callback):
        super().__init__()

        main_layout = QVBoxLayout()

        text_layout = QHBoxLayout()

        self.schedule_text = QTextEdit()
        text_layout.addWidget(self.schedule_text)

        self.timetable_layout = QVBoxLayout()
        text_layout.addLayout(self.timetable_layout)

        main_layout.addLayout(text_layout)

        button_layout = QHBoxLayout()

        self.settings_button = QPushButton("Настройки")
        self.settings_button.clicked.connect(switch_callback)

        self.clear_button = QPushButton('Очистить')
        self.filter_button = QPushButton("Фильтровать")
        self.allocation_button = QPushButton("Распределение")
        self.timetable_button = QPushButton("Расписание")

        button_layout.addWidget(self.settings_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.filter_button)
        button_layout.addWidget(self.allocation_button)
        button_layout.addWidget(self.timetable_button)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)


    def get_raw_text(self):
        data = get_clipboard_data()
        if data is not None:
            self.schedule_text.setText(data)


    def filtering(self):
        time_groups = time_sorting(self.schedule_text.toPlainText())
        if time_groups is None:
            print("Не удалось получить временные группы.")
            return

        for num, time_group in enumerate(time_groups):
            frame = QFrame()
            frame.setObjectName("group_frame")

            group_layout = QVBoxLayout()

            name = QComboBox()
            name.addItems(item.item for item in config.get('ACTIVITY'))
            if len(time_group) > 1:
                name.setCurrentIndex(0)
            elif len(time_group) == 1:
                name.setCurrentIndex(1)
            group_layout.addWidget(name)

            for time in time_group:
                line = QTextEdit()
                line.setText(datetime.strftime(time, "%H:%M"))
                line.setReadOnly(True)
                group_layout.addWidget(line)

            frame.setLayout(group_layout)
            self.timetable_layout.addWidget(frame)

        self.setStyleSheet('''
            QFrame#group_frame {
                border: 1px solid black;
            }
        ''')
