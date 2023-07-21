from Login import Ui_Frame

import json
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QStackedWidget, QWidget, QToolBar, QToolButton, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy, QAction, QCalendarWidget, QListWidget, QLineEdit, QTextEdit, QDialog, QDialogButtonBox, QTableWidget, QTableWidgetItem, QCheckBox, QFrame
from PyQt5.QtCore import Qt, QSize, QSettings
from PyQt5.QtGui import QIcon, QPixmap


class TaskWidget2(QWidget):
    def __init__(self, task):
        super().__init__()

        # Создаем элементы для отображения задачи
        title_label = QLabel(task["Title"])
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        description_label = QLabel(task["Description"])
        description_label.setStyleSheet("font-size: 14px;")

        start_date_label = QLabel("Start: " + task["Start"])
        start_date_label.setStyleSheet("font-size: 12px;")

        end_date_label = QLabel("End: " + task["End"])
        end_date_label.setStyleSheet("font-size: 12px;")

        completed_checkbox = QCheckBox("Completed")
        completed_checkbox.setChecked(task["Completed"])
        completed_checkbox.setEnabled(False)
        completed_checkbox.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")

        # Создаем компоновщики для элементов задачи
        title_layout = QHBoxLayout()
        title_layout.addWidget(title_label)

        date_layout = QHBoxLayout()
        date_layout.addWidget(start_date_label)
        date_layout.addWidget(end_date_label)
        date_layout.addStretch()

        description_layout = QHBoxLayout()
        description_layout.addWidget(description_label)

        checkbox_layout = QHBoxLayout()
        checkbox_layout.addWidget(completed_checkbox)
        checkbox_layout.addStretch()

        # Создаем компоновщик для всего виджета
        task_layout = QVBoxLayout()
        task_layout.addLayout(title_layout)
        task_layout.addLayout(date_layout)
        task_layout.addLayout(description_layout)
        task_layout.addLayout(checkbox_layout)
        task_layout.setContentsMargins(10, 10, 10, 10)

        # Создаем рамку для виджета
        task_frame = QFrame()
        task_frame.setFrameShape(QFrame.StyledPanel)
        task_frame.setFrameShadow(QFrame.Raised)
        task_frame.setLayout(task_layout)

        # Устанавливаем компоновщик для рамки
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(task_frame)


class ErrorDialog(QDialog):
    def __init__(self, error_message):
        super().__init__()

        # Создаем метку с сообщением об ошибке
        label = QLabel(error_message)

        # Создаем кнопку "ОК"
        button = QPushButton("OK")
        button.clicked.connect(self.accept)

        # Размещаем элементы на форме
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button)

        self.setLayout(layout)


class DateDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Создаем календарь для выбора даты
        self.calendar = QCalendarWidget()

        # Создаем кнопки "ОК" и "Отмена"
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # Размещаем элементы на форме
        layout = QVBoxLayout()
        layout.addWidget(self.calendar)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def selected_date(self):
        # Возвращает выбранную дату в формате QDate
        return self.calendar.selectedDate()


class TaskWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Название задачи
        label_title = QLabel("Название задачи")
        self.edit_title = QLineEdit()

        # Описание задачи
        label_description = QLabel("Описание задачи")
        self.edit_description = QTextEdit()

        # Дата начала задачи
        label_start_date = QLabel("Дата начала")
        self.edit_start_date = QLineEdit()
        self.edit_start_date.setReadOnly(True)  # Делаем поле только для чтения

        button_start_date = QPushButton("Выбрать")
        button_start_date.clicked.connect(self.select_start_date)

        layout_start_date = QHBoxLayout()
        layout_start_date.addWidget(self.edit_start_date)
        layout_start_date.addWidget(button_start_date)

        # Дата окончания задачи
        label_end_date = QLabel("Дата окончания")
        self.edit_end_date = QLineEdit()
        self.edit_end_date.setReadOnly(True)  # Делаем поле только для чтения

        button_end_date = QPushButton("Выбрать")
        button_end_date.clicked.connect(self.select_end_date)

        layout_end_date = QHBoxLayout()
        layout_end_date.addWidget(self.edit_end_date)
        layout_end_date.addWidget(button_end_date)

        # Кнопка "Добавить задачу"
        button_add_task = QPushButton("Добавить задачу")
        button_add_task.clicked.connect(self.add_task)

        # Размещаем элементы на форме
        layout = QVBoxLayout()
        layout.addWidget(label_title)
        layout.addWidget(self.edit_title)
        layout.addWidget(label_description)
        layout.addWidget(self.edit_description)
        layout.addWidget(label_start_date)
        layout.addLayout(layout_start_date)
        layout.addWidget(label_end_date)
        layout.addLayout(layout_end_date)
        layout.addWidget(button_add_task)

        self.setLayout(layout)

    def select_start_date(self):
        # Открываем окно с выбором даты начала задачи
        dialog = DateDialog()
        if dialog.exec_() == QDialog.Accepted:
            date = dialog.selected_date().toString(Qt.ISODate)
            self.edit_start_date.setText(date)

    def select_end_date(self):
        # Открываем окно с выбором даты окончания задачи
        dialog = DateDialog()
        if dialog.exec_() == QDialog.Accepted:
            date = dialog.selected_date().toString(Qt.ISODate)
            self.edit_end_date.setText(date)

    def add_task(self):
        # Обработчик нажатия на кнопку "Добавить задачу"
        title = self.edit_title.text()
        description = self.edit_description.toPlainText()
        start_date = self.edit_start_date.text()
        end_date = self.edit_end_date.text()

        if (title == '' or description == '' or start_date == '' or end_date == ''):
            error_dialog = ErrorDialog("Необходимо заполнить ВСЕ поля")
            error_dialog.exec_()
            return

        task = {"Title": title,
                "Description": description,
                "Start": start_date,
                "End": end_date,
                "Completed": False}

        with open("tasks.json", "r") as f:
            tasks = json.load(f)
        tasks.append(task)
        with open("tasks.json", "w") as f:
            json.dump(tasks, f)

        # Очищаем поля формы
        self.edit_title.clear()
        self.edit_description.clear()
        self.edit_start_date.clear()
        self.edit_end_date.clear()

        error_dialog = ErrorDialog("Задача была успешно добавлена")
        error_dialog.exec_()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Задаем параметры основному окну
        self.window_icon = QIcon("window.png")
        self.setWindowIcon(self.window_icon)
        self.setWindowTitle("Планировщик задач")

        # Создаем QStackedWidget
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        # Подгружаем настройки
        self.settings = QSettings("Туманян Марк", "Task-planner", self)

        # Создаем виджеты, которые будут отображаться в QStackedWidget
        self.profileWidget = QWidget(self.stacked_widget)
        self.calendarWidget = QWidget(self.stacked_widget)
        self.notificationsWidget = QWidget(self.stacked_widget)
        self.reminderWidget = QWidget(self.stacked_widget)
        self.chatWidget = QWidget(self.stacked_widget)
        self.taskAddWidget = QWidget(self.stacked_widget)
        self.optionsWidget = QWidget(self.stacked_widget)

        # Добавление элементов в виджет профиля
        self.profileBox = QHBoxLayout(self.profileWidget)

        # Фото профиля
        self.picProfileLabel = QLabel()
        self.picProfileLabel.setStyleSheet(
            "padding: 5px; border: 2px solid black; background-color: rgb(207, 207, 207);")
        self.picProfileLabel.setPixmap(QPixmap("new-user.png"))
        self.picProfileLabel.setScaledContents(True)
        self.picProfileLabel.setFixedWidth(320)
        self.profileBox.addWidget(self.picProfileLabel)
        self.profileWidget.setLayout(self.profileBox)

        # ФИО и прочие данные
        self.profileLabelLayout = QVBoxLayout()
        self.profileLabelLayout.setAlignment(Qt.AlignTop)

        self.profileLabelFName = QLabel(
            'Фамилия: ' + self.settings.value("FName", "Иванов"))
        self.profileLabelFName.setStyleSheet(
            "font: 18pt/12pt sans-serif; padding-left: 10px;")
        self.profileLabelSName = QLabel(
            'Имя: ' + self.settings.value("SName", "Иван"))
        self.profileLabelSName.setStyleSheet(
            "font: 18pt/12pt sans-serif; padding-left: 10px;")
        self.profileLabelLName = QLabel(
            'Отчество: ' + self.settings.value("LName", "Иванович"))
        self.profileLabelLName.setStyleSheet(
            "font: 18pt/12pt sans-serif; padding-left: 10px;")
        self.profileLabelJob = QLabel(
            'Профессия: ' + self.settings.value("Job", "Фронтенд разработчик"))
        self.profileLabelJob.setStyleSheet(
            "font: 18pt/12pt sans-serif; padding-left: 10px;")

        self.profileLabelLayout.addWidget(self.profileLabelFName)
        self.profileLabelLayout.addWidget(self.profileLabelSName)
        self.profileLabelLayout.addWidget(self.profileLabelLName)
        self.profileLabelLayout.addWidget(self.profileLabelJob)

        self.profileBox.addLayout(self.profileLabelLayout)

        # Добавление элементов в виджет календаря
        self.calendarBox = QHBoxLayout(self.calendarWidget)
        self.calendarCalendar = QCalendarWidget()

        # Потом добавить обновление виджета при изменении даты
        self.calendarCalendar.selectionChanged.connect(self.set_task_table)

        self.calendarList = QTableWidget()
        self.calendarList.setColumnCount(2)
        self.calendarList.setHorizontalHeaderLabels(["Название", "Статус"])
        self.set_task_table()

        self.calendarBox.addWidget(self.calendarCalendar)
        self.calendarBox.addWidget(self.calendarList)

        # Страница добавления задачи
        self.taskAddBox = QHBoxLayout(self.taskAddWidget)
        self.taskAddWidget = TaskWidget()
        self.taskAddBox.addWidget(self.taskAddWidget)

        # Страница уведомлений
        self.reminderBox = QVBoxLayout(self.reminderWidget)
        # Загружаем список задач из файла
        with open("tasks.json", "r") as f:
            self.tasks = json.load(f)
        # Создаем виджеты для каждой задачи и добавляем их в список задач
        for task in self.tasks:
            task_widget = TaskWidget2(task)
            self.reminderBox.addWidget(task_widget)

        # Добавляем виджеты в QStackedWidget
        self.stacked_widget.addWidget(self.profileWidget)
        self.stacked_widget.addWidget(self.calendarWidget)
        self.stacked_widget.addWidget(self.notificationsWidget)
        self.stacked_widget.addWidget(self.reminderWidget)
        self.stacked_widget.addWidget(self.chatWidget)
        self.stacked_widget.addWidget(self.taskAddWidget)
        self.stacked_widget.addWidget(self.optionsWidget)

        # Перетаскиваемый тулбар
        self.tabsToolBar = QToolBar("toolbar", self)

        # Пустое пространство между кнопками на тулбаре
        self.spacer = QLabel(self.tabsToolBar)
        self.spacer.setSizePolicy(QSizePolicy.Policy(3), QSizePolicy.Policy(3))

        # Кнопки на тулбаре
        self.profileButton = QToolButton(self.tabsToolBar)
        self.calendarButton = QToolButton(self.tabsToolBar)
        self.notificationsButton = QToolButton(self.tabsToolBar)
        self.reminderButton = QToolButton(self.tabsToolBar)
        self.chatButton = QToolButton(self.tabsToolBar)
        self.taskAddButton = QToolButton(self.tabsToolBar)
        self.optionsButton = QToolButton(self.tabsToolBar)
        self.exitButton = QToolButton(self.tabsToolBar)

        # Привязка действий к кнопкам
        self.profileButton.clicked.connect(self.show_profile)
        self.calendarButton.clicked.connect(self.show_calendar)
        self.notificationsButton.clicked.connect(self.show_notifications)
        self.reminderButton.clicked.connect(self.show_reminder)
        self.chatButton.clicked.connect(self.show_chat)
        self.taskAddButton.clicked.connect(self.show_taskAdd)
        self.optionsButton.clicked.connect(self.show_options)
        self.exitButton.clicked.connect(self.show_exit)

        # Загрузка иконок для кнопок
        self.profileIcon = QIcon(
            self.settings.value("profileIcon", "user.png"))
        self.calendarIcon = QIcon(
            self.settings.value("calendarIcon", "calendar.png"))
        self.notificationsIcon = QIcon(self.settings.value(
            "notificationIcon", "notification.png"))
        self.reminderIcon = QIcon(
            self.settings.value("reminderIcon", "notes.png"))
        self.chatIcon = QIcon(self.settings.value("chatIcon", "chat.png"))
        self.taskAddIcon = QIcon(
            self.settings.value("taskAddIcon", "add-file.png"))
        self.optionsIcon = QIcon(
            self.settings.value("optionsIcon", "wrench.png"))
        self.exitIcon = QIcon(self.settings.value("exitIcon", "exit.png"))

        # Задание иконок кнопкам
        self.profileButton.setIcon(self.profileIcon)
        self.calendarButton.setIcon(self.calendarIcon)
        self.notificationsButton.setIcon(self.notificationsIcon)
        self.reminderButton.setIcon(self.reminderIcon)
        self.chatButton.setIcon(self.chatIcon)
        self.taskAddButton.setIcon(self.taskAddIcon)
        self.optionsButton.setIcon(self.optionsIcon)
        self.exitButton.setIcon(self.exitIcon)

        # Добавление кнопок на тулбар
        self.tabsToolBar.addWidget(self.profileButton)
        self.tabsToolBar.addWidget(self.calendarButton)
        self.tabsToolBar.addWidget(self.notificationsButton)
        self.tabsToolBar.addWidget(self.reminderButton)
        self.tabsToolBar.addWidget(self.chatButton)
        self.tabsToolBar.addWidget(self.taskAddButton)
        self.tabsToolBar.addWidget(self.spacer)
        self.tabsToolBar.addWidget(self.optionsButton)
        self.tabsToolBar.addWidget(self.exitButton)

        # Добавление тулбара
        self.tabsToolBar.setStyleSheet("background-color:gray;")
        self.tabsToolBar.setIconSize(QSize(40, 40))
        self.addToolBar(Qt.ToolBarArea(1), self.tabsToolBar)

    def show_profile(self):
        self.stacked_widget.setCurrentIndex(0)

    def show_calendar(self):
        self.stacked_widget.setCurrentIndex(1)

    def show_notifications(self):
        self.stacked_widget.setCurrentIndex(2)

    def show_reminder(self):
        self.stacked_widget.setCurrentIndex(3)
        self.clearrrrr()

    def show_chat(self):
        self.stacked_widget.setCurrentIndex(4)

    def show_taskAdd(self):
        self.stacked_widget.setCurrentIndex(5)

    def show_options(self):
        self.stacked_widget.setCurrentIndex(6)

    def show_exit(self):
        self.close()

    def read_tasks(self):
        addata = []
        with open("tasks.json", "r") as file:
            data = json.load(file)
        for task in data:
            if task["Start"] <= self.calendarCalendar.selectedDate().toString(Qt.ISODate) <= task["End"]:
                addata.append(task)
        return addata

    def set_task_table(self):
        self.tasks = self.read_tasks()
        self.calendarList.setRowCount(len(self.tasks))
        self.calendarList.clearContents()
        self.curdate = self.calendarCalendar.selectedDate().toString(Qt.ISODate)
        for row, task in enumerate(self.tasks):
            name_item = QTableWidgetItem(task["Title"])
            button = QCheckBox("Выполнено")
            button.task_id = row
            button.setChecked(task["Completed"])
            button.clicked.connect(self.toggle_completed)
            self.calendarList.setItem(row, 0, name_item)
            self.calendarList.setCellWidget(row, 1, button)

    def toggle_completed(self):
        button = self.sender()  # Получаем нажатую кнопку
        task_id = button.task_id  # Получаем индекс задачи

        # Изменяем значение поля "Completed" в задаче
        self.tasks[task_id]["Completed"] = not self.tasks[task_id]["Completed"]
        
        # Записываем обновленный список задач в файл
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f)

    def clearrrrr(self):
        with open("tasks.json", "r") as f:
            self.tasks = json.load(f)
        # Создаем виджеты для каждой задачи и добавляем их в список задач
        for i in reversed(range(self.reminderBox.count())):
            self.reminderBox.itemAt(i).widget().setParent(None)
        for task in self.tasks:
            task_widget = TaskWidget2(task)
            self.reminderBox.addWidget(task_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    Form = QWidget()
    login = Ui_Frame()

    login.setupUi(Form)
    Form.show()

    login.pushButton.clicked.connect(window.show)
    login.pushButton.clicked.connect(Form.close)

    sys.exit(app.exec_())
