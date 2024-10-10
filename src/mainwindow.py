from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt, QTimer

class MainWindow(QMainWindow):
    def __init__(self, listWidget):
        super(MainWindow, self).__init__()

        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | 
                            Qt.WindowType.FramelessWindowHint)

        self.TIMER_DELAY = 10

        self.createTimerToUpdateWindowPosition()

        self.listWidget = listWidget
        self.setCentralWidget(self.listWidget)

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.windowActions = []
        self.is_active = True

    def getListWidget(self):
        return self.listWidget

    def createTimerToUpdateWindowPosition(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.windowTimerLoop)
        self.timer.start(self.TIMER_DELAY)

    def windowTimerLoop(self):
        if self.is_active:
            self.updateCursorPosition()
            self.executeWindowActions()

    def updateCursorPosition(self):
        if self.isVisible():
            current_cursor_position = QCursor.pos()
            x, y = current_cursor_position.x(), current_cursor_position.y()
            self.move(10 + x, 10 + y)

    def executeWindowActions(self):
        if self.windowActions:
            match(self.windowActions.pop()):
                case 'hide':
                    super().hide()
                case 'show':
                    super().show()

    def addWindowAction(self, exec_cmd):
        self.windowActions.append(exec_cmd)

    def activate(self):
        self.is_active = True
    
    def deactivate(self):
        super().hide()
        self.is_active = False

    def hide(self):
        self.addWindowAction('hide')

    def show(self):
        self.addWindowAction('show')