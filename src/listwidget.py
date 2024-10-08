from PyQt6.QtWidgets import QListWidget, QListWidgetItem
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import QSize, Qt

from suggestionsmanager import SuggestionsManager

class ListWidget(QListWidget):
    def __init__(self):
        super(ListWidget, self).__init__()

        self.WIDTH = 300
        self.HEIGHT = 300

        self.TEXT_FONT = QFont('Lexend', 16)
        self.ITEM_SIZE = QSize(50, 50) 

        self.BACKGROUND_COLOUR = "#3a4352"
        self.SELECTED_ITEM_BACKGROUND_COLOUR = "#1d468f"
        self.SELECTED_ITEM_TEXT_COLOUR = "white"

        self.ITEM_TEXT_COLOUR = QColor("#737f94")
        self.ITEM_BACKGROUND_COLOUR = QColor("#3a4352")

        self.START_BRACKET = '{'
        self.END_BRACKET = '}'

        self.suggestionsManager = None

        self.setFixedWidth(self.WIDTH)
        self.setFixedHeight(self.HEIGHT)
   
        self._setStyleSheet()

        self.setCurrentRow(0)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def setPrecommand(self, precommand):
        if self.suggestionsManager != None:
            self.suggestionsManager.set_precommand(precommand)

    def setSuggestionsManager(self, suggestionsManager: SuggestionsManager):
        self.suggestionsManager = suggestionsManager

    def updateSuggestions(self):
        self.clearItems()

        suggestions = self.suggestionsManager.all()

        if suggestions:
            self.addItems(suggestions)
            self.setCurrentRow(0)

    def addItems(self, strings):
        for string in strings:
            self.addItem(string)

    def addItem(self, string):
        super().addItem(self.createItem(string))

    def clearItems(self):
        for _ in range(self.count()):
            self.takeItem(0)

    def createItem(self, string):
        item = QListWidgetItem(string)

        item.setSizeHint(self.ITEM_SIZE)
        item.setFont(self.TEXT_FONT)
        item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        item.setBackground(self.ITEM_BACKGROUND_COLOUR)
        item.setForeground(self.ITEM_TEXT_COLOUR)

        return item

    def _setStyleSheet(self):
        self.setStyleSheet(f"""
                           
            QListWidget 
            {self.START_BRACKET}
                background-color: {self.BACKGROUND_COLOUR};
                            
                border-width: 2px;
                padding: 6px;
                border-style: outset;
                border-radius: 10px;
                border-color: {self.BACKGROUND_COLOUR};
                min-width: 10em;
                           
            {self.END_BRACKET}

            QListWidget::item:selected 
            {self.START_BRACKET}

                color: {self.SELECTED_ITEM_TEXT_COLOUR};             
                background-color: {self.SELECTED_ITEM_BACKGROUND_COLOUR};

            {self.END_BRACKET}

        """)
        
    def removeCurrentItem(self):
        self.takeItem(self.currentRow())

    def goUp(self):
        current = self.currentRow()

        if current - 1 >= 0:
            self.setCurrentRow(current - 1)

    def goDown(self):
        current = self.currentRow()

        if current + 1 < self.count():
            self.setCurrentRow(current + 1)
