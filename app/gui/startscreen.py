from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton

from functions import get_clipboard_data, time_sorting


class StartScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.setWindowTitle('State News')
        self.setGeometry(400, 300, 1000, 600)

        main_layout = QVBoxLayout()

        text_layout = QHBoxLayout()
        self.schedule_text = QTextEdit()

        self.timetable_layout = QVBoxLayout()


        text_layout.addWidget(self.schedule_text)
        text_layout.addLayout(self.timetable_layout)

        button_layout = QHBoxLayout()

        self.clear_button = QPushButton('Очистить')
        self.filter_button = QPushButton("Фильтровать")
        self.allocation_button = QPushButton("Распределение")
        self.timetable_button = QPushButton("Расписание")

        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.filter_button)
        button_layout.addWidget(self.allocation_button)
        button_layout.addWidget(self.timetable_button)

        main_layout.addLayout(text_layout)
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
        


