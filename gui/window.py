from PyQt5.QtWidgets import QMainWindow, QStackedWidget

from gui.main import MainScreen
from gui.settings import SettingsScreen


class MainWindow(QMainWindow): # Окно приложения
    def __init__(self):
        super().__init__()
        self.setWindowTitle('State News Filter')
        self.setGeometry(400, 300, 1000, 600)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.main_screen = MainScreen(self.switch_to_settings)
        self.main_screen.get_clipboard_text()
        self.stacked_widget.addWidget(self.main_screen)

        self.settings_screen = SettingsScreen(self.switch_to_main)
        self.stacked_widget.addWidget(self.settings_screen)

    def switch_to_settings(self):
        self.stacked_widget.setCurrentWidget(self.settings_screen)

    def switch_to_main(self):
        self.settings_screen.save_config()
        self.stacked_widget.setCurrentWidget(self.main_screen)

    def closeEvent(self, event):
        self.settings_screen.save_config()