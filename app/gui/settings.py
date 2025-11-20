from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QFrame, QScrollArea, QLabel
from functools import partial

from app.config import config


class ConfigItem(QFrame): # Элемент конфигурации
    def __init__(self, item = ""):
        super().__init__()
        self.setObjectName("Config item frame")
        self.layout = QHBoxLayout(self)
        self.item = item
        self.active = True

        self.text = QTextEdit(item)
        self.layout.addWidget(self.text)

        self.edit_btn = QPushButton("Изменить")
        self.edit_btn.clicked.connect(self.editable)
        self.layout.addWidget(self.edit_btn)

        self.delete_btn = QPushButton("Удалить")
        self.delete_btn.clicked.connect(self.delete)
        self.layout.addWidget(self.delete_btn)

        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.clicked.connect(self.cancel)
        self.layout.addWidget(self.cancel_btn)

        self.accept_btn = QPushButton("Подтвердить")
        self.accept_btn.clicked.connect(self.accept)
        self.layout.addWidget(self.accept_btn)

    def editable(self):
        self.text.setReadOnly(False)
        self.edit_btn.hide()
        self.delete_btn.hide()
        self.cancel_btn.show()
        self.accept_btn.show()

    def static(self):
        self.text.setReadOnly(True)
        self.edit_btn.show()
        self.delete_btn.show()
        self.cancel_btn.hide()
        self.accept_btn.hide()

    def cancel(self):
        self.text.setText(self.item)
        self.static()

    def accept(self):
        self.item = self.text.toPlainText()
        self.static()

    def delete(self):
        self.active = False
        self.hide()
        self.deleteLater()


def add_config_item(category, layout): # Добавить новый элемент конфигурации
    ci = ConfigItem()
    ci.editable()
    layout.insertWidget(layout.count() - 1, ci)
    category.append(ci)


class SettingsScreen(QWidget): # Экран настройки приложения
    def __init__(self, switch_callback):
        super().__init__()

        main_layout = QVBoxLayout()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        settings_widget = QWidget()
        settings_layout = QHBoxLayout(settings_widget)

        self.staff = []
        self.list_marks = []
        self.activities = []

        for category, cat in zip(config.keys(),
                                 [self.staff, self.activities, self.list_marks]): # Заполнение полей данными из конфига
            frame = QFrame()
            frame.setObjectName("group_frame")
            layout = QVBoxLayout(frame)
            for item in config.get(category):
                ci = ConfigItem(item)
                ci.static()
                layout.addWidget(ci)
                cat.append(ci)
            add_item_btn = QPushButton("Добавить")
            add_item_btn.clicked.connect(partial(add_config_item, cat, layout))
            layout.addWidget(add_item_btn)
            settings_layout.addWidget(frame)

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

    def save_config(self):
        staff = [item.item for item in self.staff if item.item != '' and item.active]
        activities = [item.item for item in self.activities if item.item != '' and item.active]
        list_marks = [item.item for item in self.list_marks if item.item != '' and item.active]

        config.update({
            "STAFF": staff,
            "ACTIVITIES": activities,
            "LIST MARKS": list_marks
        })
