from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from vogl import VoglGame


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # self.game = Game(self)
        self.textboxLevel = QLineEdit(self)

        self.themeLabel = QLabel(self)
        self.labelLevel = QLabel(self)

        self.radioBtnLite = QRadioButton(self)
        self.radioBtnDark = QRadioButton(self)

        self.buttonStart = QPushButton(self)
        self.buttonHelp = QPushButton(self)

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 400, 400)
        self.setWindowTitle('Вогл')
        # self.setWindowIcon(QIcon('items/logo.png'))
        # self.setStyleSheet("background-color: #E6E6FA")

        self.themeLabel.setText('Цветовая тема')
        self.themeLabel.move(120, 120)
        self.themeLabel.resize(80, 20)

        self.labelLevel.setText('Номер уровня 1-10')
        self.labelLevel.move(120, 180)
        self.labelLevel.resize(80, 20)

        self.radioBtnLite.setText('Светлая')
        self.radioBtnLite.move(120, 140)
        self.radioBtnLite.resize(80, 20)
        self.radioBtnDark.setText('Темная')
        self.radioBtnDark.move(200, 140)
        self.radioBtnDark.resize(80, 20)

        self.textboxLevel.move(220, 180)
        self.textboxLevel.resize(50, 20)
        self.textboxLevel.setText('1')

        self.buttonStart.move(100, 230)
        self.buttonStart.resize(200, 50)
        self.buttonStart.setText('START')
        self.buttonStart.clicked.connect(self.on_action)

        self.buttonHelp.move(100, 300)
        self.buttonHelp.resize(200, 30)
        self.buttonHelp.setText('HELP')
        # self.buttonHelp.clicked.connect(self.on_action_help)

    def on_action(self):
        theme = 0
        if self.radioBtnDark.isChecked():
            theme = 1
        if self.textboxLevel.text() == '':
            self.game = Game(self, 0, theme)
            self.buttonStart.setText('RESTART')
            self.game.show()
            self.hide()
        elif int(self.textboxLevel.text()) > 0:
            self.game = Game(self, int(self.textboxLevel.text()), theme)
            self.buttonStart.setText('RESTART')
            self.game.show()
            self.hide()

    # def on_action_help(self):
    #     webbrowser.open('items\index.html')


class Game(QWidget):
    def __init__(self, main, level=1, theme=1):
        super().__init__()

        self.vogl_game = VoglGame(level)
        self.level = level
        self.theme = theme

        self.main_window = main

        self.square_side = 100
        self.window_width = self.vogl_game.size * self.square_side
        self.window_height = self.vogl_game.size * self.square_side + 50

        self.buttonRestart = QPushButton(self)
        # self.levelLabel = QLabel(self)
        # self.textBoxLevel = QLineEdit(self)

        self.initGame()

    def initGame(self):
        self.setGeometry(700, 300, self.window_width, self.window_height)
        self.setWindowTitle('Вогл')

        self.buttonRestart.setText('Рестарт')
        self.buttonRestart.move(100, self.window_height - 40)
        self.buttonRestart.resize(80, 40)
        self.buttonRestart.clicked.connect(self.restart)

        # self.levelLabel.setText("Уровень")
        # self.buttonRestart.move(100, self.window_height - 40)
        # self.buttonRestart.resize(120, 40)

        if self.theme == 1:
            self.setStyleSheet("background-color: #202020")
            self.buttonRestart.setStyleSheet("background-color: #404040")
        else:
            self.setStyleSheet("background-color: #E6E6FA")
            self.buttonRestart.setStyleSheet("background-color: #E6E6FA")

    def restart(self):
        self.vogl_game.restart()
        self.update()

    def set_level(self, level: int):
        self.vogl_game.set_level(level)
        self.update()

    def paintEvent(self, e):
        super().paintEvent(e)
        if not self.vogl_game.is_level_complete():
            qp = QPainter()
            qp.begin(self)
            self.drawRectangles(qp)
            self.drawCircles(qp)
            qp.end()
        else:
            qp = QPainter()
            qp.begin(self)
            self.drawRectangles(qp)
            self.drawCircles(qp)
            self.drawVictory(True, qp)
            qp.end()

    def mousePressEvent(self, e: QMouseEvent):
        row = e.y() // self.square_side
        col = e.x() // self.square_side

        self.vogl_game.set_current_point(row, col)
        self.vogl_game.left_mouse_click(row, col)
        self.update()

    def drawVictory(self, win, qp):
        msgBox = QMessageBox(self)
        msgBox.setText("Вы победили!")
        msgBox.setFont(QFont('Bahnschrift SemiBold', 15))
        msgBox.setStyleSheet("background-color: #E6E6FA")
        self.hide()
        msgBox.exec()

    def drawRectangles(self, qp):
        col = QColor(0, 0, 0)
        col.setNamedColor('#FFFFFF')
        qp.setPen(col)

        spaceY = 0
        for i in range(int(self.window_height / self.square_side)):
            spaceX = 0
            for j in range(int(self.window_width / self.square_side)):
                qp.drawRect(spaceX, spaceY, self.square_side, self.square_side)
                spaceX += self.square_side
            spaceY += self.square_side

    def drawCircles(self, qp):
        qp.setPen(QPen(Qt.GlobalColor.black))
        qp.setBrush(Qt.GlobalColor.gray)
        spaceY = 0
        current_point = self.vogl_game.current_point
        for i in range(len(self.vogl_game.level)):
            spaceX = 0
            for j in range(len(self.vogl_game.level[i])):
                element = self.vogl_game.level[i][j]
                if element == 1:
                    if current_point is not None and current_point.row == i and current_point.colm == j:
                        if self.theme == 1:
                            qp.setBrush(Qt.GlobalColor.cyan)
                        else:
                            qp.setBrush(Qt.GlobalColor.black)
                        qp.drawEllipse(spaceX + 5, spaceY + 5, self.square_side - 10, self.square_side - 10)
                        qp.setBrush(Qt.GlobalColor.gray)
                    else:
                        qp.drawEllipse(spaceX + 5, spaceY + 5, self.square_side - 10, self.square_side - 10)
                spaceX += self.square_side
            spaceY += self.square_side
