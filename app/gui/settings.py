from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton


class SettingsScreen(QWidget):
    def __init__(self, switch_callback):
        super().__init__()

        main_layout = QVBoxLayout()

        button_layout = QHBoxLayout()

        self.main_button = QPushButton("Назад")
        self.main_button.clicked.connect(switch_callback)
        button_layout.addWidget(self.main_button)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
