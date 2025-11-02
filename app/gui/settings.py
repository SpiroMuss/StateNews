from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QFrame, QScrollArea, QLabel
from functools import partial
from pprint import pprint as pp

from app.constants import constants


class SettingsScreen(QWidget):
    def __init__(self, switch_callback):
        super().__init__()

        main_layout = QVBoxLayout()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        settings_widget = QWidget()
        settings_layout = QHBoxLayout(settings_widget)

        self.staff_frame = None
        self.list_mark_frame = None
        self.activity_frame = None

        for category, const_frame in zip([constants.staff, constants.list_marks, constants.activity],
                                        [self.staff_frame, self.list_mark_frame, self.activity_frame]):
            frame = QFrame()
            frame.setObjectName("group_frame")
            layout = QVBoxLayout(frame)
            for constant in category:
                layout.addWidget(self.get_config_item(constant))
            add_item_button = QPushButton("Добавить")
            add_item_button.clicked.connect(partial(self.add_constant, category, layout))
            layout.addWidget(add_item_button)
            settings_layout.addWidget(frame)
            const_frame = frame

        pp(self.staff_frame)

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


    def get_config_item(self, item):
        frame = QFrame()
        frame.setObjectName("item_frame")

        layout = QHBoxLayout(frame)

        text = QTextEdit()
        text.setText(item)
        text.setReadOnly(True)
        layout.addWidget(text)

        edit_button = QPushButton("Изменить")
        edit_button.clicked.connect(partial(self.edit_constant, edit_button))
        layout.addWidget(edit_button)

        delete_button = QPushButton("Удалить")
        delete_button.clicked.connect(partial(self.delete_constant, delete_button))
        layout.addWidget(delete_button)

        return frame


    def edit_constant(self, button):
        frame = button.parent()
        children = frame.children()
        text = children[1]
        text.setReadOnly(False)
        for btn in children[2:]:
            btn.deleteLater()
        accept_button = QPushButton("Готово")
        accept_button.clicked.connect(lambda: 1)
        frame.addWidget(accept_button)
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(lambda: 2)
        frame.addWidget(cancel_button)


    def delete_constant(self, btn):
        frame = btn.parent()
        children = frame.children()
        text = children[1]
        if btn in self.constant_buttons.get("staff") and text.toPlainText() in constants.staff:
            constants.staff.remove(text.toPlainText())
            constants.commit()
        frame.deleteLater()


    def add_constant(self, constant_array, layout):
        frame = self.get_config_item("")
        layout.insertWidget(layout.count() - 1, frame)