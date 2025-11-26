from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QFrame, QComboBox, QScrollArea, \
    QLabel
from datetime import datetime, timedelta
import requests
import json
import pyperclip
from functools import partial

from app.config import config, url, system


def delete_time(btn):
    btn.parent().deleteLater()

class TimeGroup(QFrame): # Временная группа активности GUI
    def __init__(self, time_group):
        super().__init__()
        self.setObjectName("Time_group_frame")
        self.layout = QVBoxLayout(self)

        self.activity = QComboBox()
        self.activity.addItems(config.get("ACTIVITIES"))
        if len(time_group) == 1:
            self.activity.setCurrentIndex(0)
        elif len(time_group) > 1:
            self.activity.setCurrentIndex(1)
        self.activity.setEditable(True)
        self.layout.addWidget(self.activity)

        for time in time_group: # Создание элемента времени
            time_frame = QFrame()
            layout = QHBoxLayout()

            time_label = QLabel(datetime.strftime(time, "%H:%M"))
            layout.addWidget(time_label)

            del_btn = QPushButton()
            del_btn.setText("Удалить")
            del_btn.clicked.connect(partial(delete_time, del_btn))
            layout.addWidget(del_btn)

            time_frame.setLayout(layout)
            self.layout.addWidget(time_frame)

    @property
    def times(self):
        t = []
        for time in self.children()[2:]:
            t.append(time)
        return sorted(t, key=lambda x: datetime.strptime(x.children()[1].text(), "%H:%M"))



class MainScreen(QWidget): # Главный экран приложения
    def __init__(self, switch_callback): # Инициализация основного окна
        super().__init__()

        main_layout = QVBoxLayout()

        text_layout = QHBoxLayout()

        self.schedule_text = QTextEdit()
        text_layout.addWidget(self.schedule_text)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        self.timetable_widget = QWidget()
        self.timetable_layout = QVBoxLayout()
        self.timetable_widget.setLayout(self.timetable_layout)
        self.time_groups = []
        self.up_btns = []
        self.down_btns = []
        scroll_area.setWidget(self.timetable_widget)
        text_layout.addWidget(scroll_area)

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

        self.copy_allocation_button = QPushButton("Скопировать распределение")
        self.copy_allocation_button.clicked.connect(self.copy_allocation)
        button_layout.addWidget(self.copy_allocation_button)

        self.send_allocation_button = QPushButton("Выслать распределение")
        self.send_allocation_button.clicked.connect(self.send_allocation)
        button_layout.addWidget(self.send_allocation_button)

        self.timetable_button = QPushButton("Скопировать расписание")
        self.timetable_button.clicked.connect(self.copy_timetable)
        button_layout.addWidget(self.timetable_button)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)


    def clear_schedule(self): # Очистка главного экрана от текста
        self.schedule_text.setText('')
        for i in range(len(self.time_groups)):
            group = self.time_groups.pop()
            group.setParent(None)
            group.deleteLater()

    def get_clipboard_text(self): # Получение текста из буфера обмена
        if system == 'Windows':
            data = pyperclip.paste()
        else:
            data = None

        if data is not None and not "":
            self.schedule_text.setText(data)
            self.filter_schedule()

    def filter_schedule(self): # Фильтрация расписания согласно конфигу, создание визуальных групп
        for i in range(len(self.time_groups)):
            group = self.time_groups.pop()
            group.setParent(None)
            group.deleteLater()

        # Поиск времени по сотрудникам
        timetable = []
        for line in self.schedule_text.toPlainText().split('\n'):
            for employee in config.get('STAFF'):
                if line.rfind(employee) != -1:
                    timetable.append(datetime.strptime(line[0:11], "%d.%m %H:%M"))

        # Разделение на группы
        try:
            time_groups = [[timetable[0]]]
        except IndexError:
            time_groups = None
        group = 0
        for i, j in zip(timetable[0:-1], timetable[1:]):
            if (j - i).total_seconds() == 1200:
                time_groups[group].append(j)
            elif (j - i).total_seconds() > 1200:
                time_groups.append([j])
                group += 1
            else:
                print("Непредвиденная ошибка в паре: ", i, j)


        if time_groups is None: # Проверка наличия групп
            print("Не удалось получить временные группы.")
            return

        for time_group in time_groups: # Создание, вывод групп в GUI
            frame = TimeGroup(time_group)
            self.time_groups.append(frame)
            self.timetable_layout.addWidget(frame)

        self.place_btns()

        self.setStyleSheet('''
            QFrame#Time_group_frame {
                border: 1px solid black;
            }
        ''')


    def up_time(self, group_num):
        times = self.time_groups[group_num].times
        time = times[0]
        if len(times) == 1:
            time.setParent(self.time_groups[group_num - 1])
            self.time_groups[group_num - 1].layout.addWidget(time)
            time_group = self.time_groups.pop(group_num)
            time_group.deleteLater()

        else:
            if group_num == 0:
                new_group = TimeGroup([])
                new_group.setParent(self.timetable_widget)
                self.timetable_layout.insertWidget(0, new_group)
                time.setParent(new_group)
                new_group.layout.addWidget(time)
                self.time_groups.insert(0, new_group)

            else:
                time.setParent(self.time_groups[group_num - 1])
                self.time_groups[group_num - 1].layout.addWidget(time)

        self.place_btns()

    def down_time(self, group_num):
        times = self.time_groups[group_num].times
        time = times[-1]
        if len(times) == 1:
            time.setParent(self.time_groups[group_num + 1])
            self.time_groups[group_num + 1].layout.insertWidget(1, time)
            time_group = self.time_groups.pop(group_num)
            time_group.deleteLater()

        else:
            if group_num == len(self.time_groups) - 1:
                new_group = TimeGroup([])
                new_group.setParent(self.timetable_widget)
                self.timetable_layout.addWidget(new_group)
                time.setParent(new_group)
                new_group.layout.insertWidget(1, time)
                self.time_groups.append(new_group)

            else:
                time.setParent(self.time_groups[group_num + 1])
                self.time_groups[group_num + 1].layout.insertWidget(1, time)

        self.place_btns()

    def create_up_btn(self, time, group_num):
        up_btn = QPushButton()
        up_btn.setText("Поднять")
        up_btn.clicked.connect(partial(self.up_time, group_num))
        time.layout().addWidget(up_btn)
        self.up_btns.append(up_btn)

    def create_down_btn(self, time, group_num):
        down_btn = QPushButton()
        down_btn.setText("Опустить")
        down_btn.clicked.connect(partial(self.down_time, group_num))
        time.layout().addWidget(down_btn)
        self.down_btns.append(down_btn)

    def place_btns(self):
        for enum, group_frame in enumerate(self.time_groups):
            times = group_frame.times
            for time in times:
                if len(time.children()) > 3:
                    for item in time.children()[3:]:
                        item.setParent(None)
                        item.deleteLater()

            if len(times) == 1:
                if enum == 0:
                    self.create_down_btn(times[-1], enum)

                elif enum == len(self.time_groups) - 1:
                    self.create_up_btn(times[0], enum)

                else:
                    self.create_up_btn(times[0], enum)
                    self.create_down_btn(times[-1], enum)

            elif len(times) > 1:
                self.create_up_btn(times[0], enum)
                self.create_down_btn(times[-1], enum)


    def get_allocation(self): # Сборщик групп в одно сообщение для распределения
        date = self.schedule_text.toPlainText()[:self.schedule_text.toPlainText().find(' ')]
        title = f'# Список задач на {date}.{(datetime.now() + timedelta(days=1)).year}\n'

        tasks = []
        for group in self.time_groups:
            activity = group.children()[1].currentText()
            times = []
            for time in group.times:
                times.append(time.children()[1].text())

            tasks.append(f'> {activity}\n> ' + ' - '.join(times))

        return title, tasks

    def send_allocation(self): # Отправление распределения на Webhook
        title, tasks = self.get_allocation()
        if not tasks:
            return

        headers = {
            "Content-Type": "application/json",
        }

        data = {
            'content': title
        }
        requests.post(url=url, headers=headers, data=json.dumps(data))

        for task in tasks:
            data = {
                'content': task
            }
            requests.post(url=url, headers=headers, data=json.dumps(data))

    def copy_allocation(self): # Копирование распределения в буфер обмена
        title, tasks = self.get_allocation()
        if system == 'Windows':
            pyperclip.copy(title + '\n'.join(tasks))


    def copy_timetable(self):
        date = self.schedule_text.toPlainText()[:self.schedule_text.toPlainText().find(' ')]
        title = f'## Гос. волны Аппарата Правительства на {date}.{(datetime.now() + timedelta(days=1)).year}\n'

        tasks = []
        for group in self.time_groups:
            activity = group.children()[1].currentText()
            times = []
            for time in group.times:
                times.append(time.children()[1].text())

            tasks.append(f'{activity} | ' + ' - '.join(times))

        pyperclip.copy(title + '```' + '\n'.join(tasks) + '```')
