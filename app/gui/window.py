from PyQt5.QtWidgets import QMainWindow, QStackedWidget

from app.gui.main import MainScreen
from app.gui.settings import SettingsScreen


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('State News Filter')
        self.setGeometry(400, 300, 1000, 600)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.main_screen = MainScreen(self.switch_to_settings)
        self.main_screen.get_raw_text()
        self.main_screen.filtering()
        self.stacked_widget.addWidget(self.main_screen)

        self.settings_screen = SettingsScreen(self.switch_to_main)
        self.stacked_widget.addWidget(self.settings_screen)

    def switch_to_settings(self):
        self.stacked_widget.setCurrentWidget(self.settings_screen)

    def switch_to_main(self):
        self.stacked_widget.setCurrentWidget(self.main_screen)