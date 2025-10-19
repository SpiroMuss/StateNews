from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QFrame, QScrollArea
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

        self.constant_buttons = {
            "staff": [],
            "list_marks": [],
            "activity": []
        }

        staff_frame = QFrame()
        staff_frame.setObjectName("group_frame")
        staff_layout = QVBoxLayout(staff_frame)
        self.show_config_items(constants.staff, staff_layout, self.constant_buttons.get("staff"))
        settings_layout.addWidget(staff_frame)

        list_marks_frame = QFrame()
        list_marks_frame.setObjectName("group_frame")
        list_marks_layout = QVBoxLayout(list_marks_frame)
        self.show_config_items(constants.list_marks, list_marks_layout, self.constant_buttons.get("list_marks"))
        settings_layout.addWidget(list_marks_frame)

        activity_frame = QFrame()
        activity_frame.setObjectName("group_frame")
        activity_layout = QVBoxLayout(activity_frame)
        self.show_config_items(constants.activity, activity_layout, self.constant_buttons.get("activity"))
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


    def show_config_items(self, array, layout, button_list):
        for item in array:
            item_frame = QFrame()
            item_frame.setObjectName("item_frame")

            item_layout = QHBoxLayout(item_frame)

            text = QTextEdit()
            text.setText(item)
            text.setReadOnly(True)
            item_layout.addWidget(text)

            edit_button = QPushButton("Изменить")
            edit_button.clicked.connect(partial(self.edit_constant, edit_button))
            button_list.append(edit_button)
            item_layout.addWidget(edit_button)

            delete_button = QPushButton("Удалить")
            delete_button.clicked.connect(partial(self.delete_constant, delete_button))
            button_list.append(delete_button)
            item_layout.addWidget(delete_button)

            layout.addWidget(item_frame)


    def edit_constant(self, btn):
        pass



    def delete_constant(self, btn):
        frame = btn.parent()
        children = frame.children()
        text = children[1]
        if btn in self.constant_buttons.get("staff"):
            constants.staff.remove(text.toPlainText())
            constants.commit()
        # Сделать удаление из GUI