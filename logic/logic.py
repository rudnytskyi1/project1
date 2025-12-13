from PyQt6.QtWidgets import QMainWindow, QMessageBox, QApplication
from ui.gui import Gui
from database.db import Database, IntegrityError


class Logic(QMainWindow, Gui):
    """
    Main logic class
    """

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.setFixedSize(450, 391)
        self.db = Database()
        self.pushButton.clicked.connect(self.submit_vote)

    def submit_vote(self) -> None:
        """
        Validates and adds a vote for selected candidate
        """

        user_id = self.lineEdit.text().strip()

        if not user_id.isnumeric():
            QMessageBox.critical(self, "Invalid Input", "ID must be a number.")
            self.reset()
            return

        user_id = int(user_id)

        if self.radioButton.isChecked():
            candidate = "Jane"
        elif self.radioButton_2.isChecked():
            candidate = "John"
        else:
            QMessageBox.critical(self, "Invalid input", "You must select a candidate.")
            self.reset()
            return

        try:
            self.db.add_vote(user_id, candidate)
        except IntegrityError:
            QMessageBox.critical(self, "Already voted", "You already voted!")
            self.reset()
            return

        QMessageBox.information(self, "Vote status", "Your vote was submitted.")
        self.reset()

    def reset(self) -> None:
        """
        Clears ID input, unchecks radio buttons
        """
        self.lineEdit.clear()
        self.radioButton.setAutoExclusive(False)
        self.radioButton_2.setAutoExclusive(False)
        self.radioButton.setChecked(False)
        self.radioButton_2.setChecked(False)
        self.radioButton.setAutoExclusive(True)
        self.radioButton_2.setAutoExclusive(True)
