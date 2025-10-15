import sys
from PyQt5.QtWidgets import QApplication

from gui.startscreen import StartScreen


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StartScreen()
    ex.get_raw_text()
    ex.filtering()
    ex.show()
    sys.exit(app.exec_())