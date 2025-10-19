from datetime import datetime
from PyQt5.QtWidgets import QTextEdit, QHBoxLayout, QPushButton, QFrame
from functools import partial

from constants import constants


def get_clipboard_data():
    data = None
    # if constants.system == 'WINDOWS':
    #     try:
    #         import win32clipboard
    #         win32clipboard.OpenClipboard()
    #         data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
    #         win32clipboard.CloseClipboard()
    #     except Exception as err:
    #         pass
    with open("schedule.txt", "r", encoding="utf-8") as file:
        data = file.read()
    return data


def time_sorting(schedule):
    timetable = []

    # Поиск времени
    for line in schedule.split('\n'):
        for employee in constants.staff:
            if line.rfind(employee) != -1:
                timetable.append(datetime.strptime(line[0:11], "%d.%m %H:%M"))

    # Разделение на группы
    try:
        time_groups = [[timetable[0]]]
    except IndexError:
        return None
    group = 0
    for i, j in zip(timetable[0:-1], timetable[1:]):
        if (j - i).total_seconds() == 1200:
            time_groups[group].append(j)
        elif (j - i).total_seconds() > 1200:
            time_groups.append([j])
            group += 1
        else:
            print("Неотсортированная пара: ", i, j)

    return time_groups


def clear_widget(widget):
    pass


def show_config_items(array, layout):
    for item in array:
        item_frame = QFrame()
        item_frame.setObjectName("item_frame")
        item_layout = QHBoxLayout(item_frame)

        text = QTextEdit()
        text.setText(item)
        text.setReadOnly(True)
        item_layout.addWidget(text)

        edit_button = QPushButton("Изменить")
        edit_button.clicked.connect(lambda: 1)
        item_layout.addWidget(edit_button)

        delete_button = QPushButton("Удалить")
        delete_button.clicked.connect(partial(delete_constant, delete_button.parent()))
        item_layout.addWidget(delete_button)

        layout.addWidget(item_frame)



def edit_constant():
    pass


def delete_constant(frame):
    children = frame.children()
    
