# style = """
#             /* Основной фон */
#             QWidget {
#                 background-color: #f5f1e6;  /* Светлый бежевый */
#                 color: #3e2723;  /* Темно-коричневый для текста */
#                 font-family: 'Segoe UI', Arial, sans-serif;
#             }
#
#             /* Заголовки */
#             QLabel {
#                 color: #5d4037;  /* Коричневый */
#                 font-weight: bold;
#                 padding: 5px 0px;
#             }
#
#             /* Поля ввода (QLineEdit) */
#             QLineEdit {
#                 background-color: #faf8f3;  /* Очень светлый бежевый */
#                 border: 2px solid #6b8e71;  /* Зеленый акцент */
#                 border-radius: 6px;
#                 padding: 10px;
#                 font-size: 14px;
#                 color: #4e342e;  /* Темно-коричневый */
#                 selection-background-color: #a5d6a7;  /* Светло-зеленый для выделения */
#             }
#
#             QLineEdit:focus {
#                 border: 2px solid #4a7c59;  /* Более насыщенный зеленый */
#                 background-color: #ffffff;
#             }
#
#             QLineEdit::placeholder {
#                 color: #a1887f;  /* Светло-коричневый для placeholder */
#                 font-style: italic;
#             }
#
#             /* Многострочные текстовые поля (QTextEdit) */
#             QTextEdit {
#                 background-color: #faf8f3;
#                 border: 2px solid #6b8e71;  /* Зеленый акцент */
#                 border-radius: 6px;
#                 padding: 10px;
#                 font-size: 14px;
#                 color: #4e342e;
#                 selection-background-color: #a5d6a7;
#             }
#
#             QTextEdit:focus {
#                 border: 2px solid #4a7c59;
#                 background-color: #ffffff;
#             }
#
#             QTextEdit::placeholder {
#                 color: #a1887f;
#                 font-style: italic;
#             }
#
#             /* Кнопки */
#             QPushButton {
#                 background-color: #8d6e63;  /* Коричневый */
#                 color: white;
#                 border: none;
#                 border-radius: 6px;
#                 padding: 12px;
#                 font-size: 14px;
#                 font-weight: bold;
#                 margin-top: 10px;
#             }
#
#             QPushButton:hover {
#                 background-color: #6d4c41;  /* Темно-коричневый */
#             }
#
#             QPushButton:pressed {
#                 background-color: #4a3429;  /* Очень темный коричневый */
#                 padding-top: 13px;
#                 padding-bottom: 11px;
#             }
#
#             QPushButton:disabled {
#                 background-color: #bcaaa4;  /* Светло-коричневый */
#                 color: #757575;
#             }
#             """
import sys

from PyQt5.QtWidgets import (QMainWindow, QStackedWidget, QVBoxLayout,
                             QWidget, QPushButton, QLabel, QLineEdit, QApplication)


# Базовый класс для экранов
class BaseScreen(QWidget):
    def __init__(self):
        super().__init__()

    def get_data(self):
        """Метод для получения данных с экрана"""
        return {}

    def set_data(self, data):
        """Метод для установки данных на экран"""
        pass


# Главный экран
class MainScreen(BaseScreen):
    def __init__(self, switch_callback):
        super().__init__()
        self.switch_callback = switch_callback

        layout = QVBoxLayout()
        self.label = QLabel("Главный экран")
        self.settings_btn = QPushButton("Настройки")
        self.settings_btn.clicked.connect(switch_callback)

        layout.addWidget(self.label)
        layout.addWidget(self.settings_btn)
        self.setLayout(layout)

    def get_data(self):
        return {"message": "Данные с главного экрана"}


# Экран настроек
class SettingsScreen(BaseScreen):
    def __init__(self, switch_callback):
        super().__init__()
        self.switch_callback = switch_callback

        layout = QVBoxLayout()
        self.label = QLabel("Экран настроек")
        self.input_field = QLineEdit()
        self.back_btn = QPushButton("Назад")
        self.back_btn.clicked.connect(switch_callback)

        layout.addWidget(self.label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.back_btn)
        self.setLayout(layout)

    def get_data(self):
        return {"setting_value": self.input_field.text()}

    def set_data(self, data):
        if "setting_value" in data:
            self.input_field.setText(data["setting_value"])


# Основное окно
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Многоэкранное приложение")



        # Данные для передачи между экранами
        self.shared_data = {}

    def switch_to_settings(self):
        # Сохраняем данные с главного экрана
        self.shared_data.update(self.main_screen.get_data())
        # Переключаемся на экран настроек
        self.stacked_widget.setCurrentWidget(self.settings_screen)

    def switch_to_main(self):
        # Сохраняем данные с экрана настроек
        self.shared_data.update(self.settings_screen.get_data())
        # Обновляем данные на главном экране (если нужно)
        self.main_screen.set_data(self.shared_data)
        # Переключаемся на главный экран
        self.stacked_widget.setCurrentWidget(self.main_screen9)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()