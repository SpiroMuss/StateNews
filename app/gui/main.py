from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QFrame, QComboBox
from datetime import datetime

from functions import get_clipboard_data, time_sorting
from app.config import system, config


class MainScreen(QWidget): # Главный экрын приложения
    def __init__(self, switch_callback): # Инициализация основного окна
        super().__init__()

        main_layout = QVBoxLayout()

        text_layout = QHBoxLayout()

        self.schedule_text = QTextEdit()
        text_layout.addWidget(self.schedule_text)

        self.timetable_frame = QFrame()
        self.timetable_layout = QVBoxLayout()
        self.timetable_frame.setLayout(self.timetable_layout)
        text_layout.addWidget(self.timetable_frame)

        main_layout.addLayout(text_layout)

        button_layout = QHBoxLayout()

        self.settings_button = QPushButton("Настройки")
        self.settings_button.clicked.connect(switch_callback)
        button_layout.addWidget(self.settings_button)

        self.clear_button = QPushButton('Очистить')
        self.clear_button.clicked.connect(self.clear_schedule)
        button_layout.addWidget(self.clear_button)

        self.filter_button = QPushButton("Фильтровать")
        self.filter_button.clicked.connect(self.filter_schedule)
        button_layout.addWidget(self.filter_button)

        self.allocation_button = QPushButton("Распределение")
        self.allocation_button.clicked.connect(self.copy_allocation)
        button_layout.addWidget(self.allocation_button)

        self.timetable_button = QPushButton("Расписание")
        button_layout.addWidget(self.timetable_button)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def clear_schedule(self): # Очистка главного экрана от текста
        self.schedule_text.setText('')
        for frame in self.timetable_frame.children()[1:]:
            frame.deleteLater()

    def filter_schedule(self): # Фильтрация расписания согласно конфигу, создание визуальных групп
        for frame in self.timetable_frame.children()[1:]:
            frame.deleteLater()
        time_groups = time_sorting(self.schedule_text.toPlainText())
        if time_groups is None:
            print("Не удалось получить временные группы.")
            return

        for time_group in time_groups:
            frame = QFrame()
            frame.setObjectName("time_group_frame")

            group_layout = QVBoxLayout()

            name = QComboBox()
            name.addItems(config.get('ACTIVITIES'))
            if len(time_group) > 1:
                name.setCurrentIndex(0)
            elif len(time_group) == 1:
                name.setCurrentIndex(1)
            name.setEditable(True)
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

    def copy_allocation(self):
        print(self.timetable_frame.children())

    def get_raw_text(self):
        data = get_clipboard_data()
        if data is not None:
            self.schedule_text.setText(data)
            self.filter_schedule()
