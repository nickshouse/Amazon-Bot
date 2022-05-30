import ctypes
import subprocess
import sys
import amazon
import os
import shutil
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QIcon
from threading import Thread

class ShopBot(QMainWindow):
    # Load UI
    def __init__(self):
        super(ShopBot, self).__init__()
        uic.loadUi("ui.ui", self)
        # Window settings
        self.setFixedSize(411, 278)
        self.setWindowTitle("Shop Bot")
        self.setWindowIcon(QIcon("robot.png"))
        self.instances = 0 # Current number of chrome windows opened

        # Hide chrome console window
        console_hwnd = ctypes.windll.kernel32.GetConsoleWindow ()
        ctypes.windll.user32.ShowWindow (console_hwnd, subprocess.SW_HIDE)

        # Read in info, ignore errors
        try:
            self.readIn(self.comboBox, "usernames.txt")
            self.readIn(self.comboBox_2, "passwords.txt")
            self.readIn(self.comboBox_3, "links.txt")
            self.readIn(self.comboBox_4, "prices.txt")
        except:
            pass
        # Make current text on combo boxes blank
        self.blanker(self.comboBox)
        self.blanker(self.comboBox_2)
        self.blanker(self.comboBox_3)
        self.blanker(self.comboBox_4)

        ##################################################### BUTTONS
        # Save buttons
        self.saveButton.setIcon(QIcon("save.png"))
        self.saveButton.setToolTip("Save list to a txt file located inside this program's directory")
        self.saveButton.clicked.connect(lambda: self.save(self.comboBox, "usernames.txt"))
        self.saveButton2.setIcon(QIcon("save.png"))
        self.saveButton2.setToolTip("Save list to a txt file located inside this program's directory")
        self.saveButton2.clicked.connect(lambda: self.save(self.comboBox_2, "passwords.txt"))
        self.saveButton3.setIcon(QIcon("save.png"))
        self.saveButton3.setToolTip("Save list to a txt file located inside this program's directory")
        self.saveButton3.clicked.connect(lambda: self.save(self.comboBox_3, "links.txt"))
        self.saveButton4.setIcon(QIcon("save.png"))
        self.saveButton4.setToolTip("Save list to a txt file located inside this program's directory")
        self.saveButton4.clicked.connect(lambda: self.save(self.comboBox_4, "prices.txt"))
        # Add buttons
        self.addButton.setIcon(QIcon("plus.png"))
        self.addButton.setToolTip("Add selected item to the list")
        self.addButton.clicked.connect(lambda: self.add(self.comboBox))
        self.addButton2.setIcon(QIcon("plus.png"))
        self.addButton2.setToolTip("Add selected item to the list")
        self.addButton2.clicked.connect(lambda: self.add(self.comboBox_2))
        self.addButton3.setIcon(QIcon("plus.png"))
        self.addButton3.setToolTip("Add selected item to the list")
        self.addButton3.clicked.connect(lambda: self.add(self.comboBox_3))
        self.addButton4.setIcon(QIcon("plus.png"))
        self.addButton4.setToolTip("Add selected item to the list")
        self.addButton4.clicked.connect(lambda: self.add(self.comboBox_4))

        # Minus buttons
        self.minusButton.setIcon(QIcon("minus.png"))
        self.minusButton.setToolTip("Remove selected item from the list\nThis does not remove the item from your saved txt list")
        self.minusButton.clicked.connect(lambda: self.remove(self.comboBox))
        self.minusButton2.setIcon(QIcon("minus.png"))
        self.minusButton2.setToolTip("Remove selected item from the list\nThis does not remove the item from your saved txt list")
        self.minusButton2.clicked.connect(lambda: self.remove(self.comboBox_2))
        self.minusButton3.setIcon(QIcon("minus.png"))
        self.minusButton3.setToolTip("Remove selected item from the list\nThis does not remove the item from your saved txt list")
        self.minusButton3.clicked.connect(lambda: self.remove(self.comboBox_3))
        self.minusButton4.setIcon(QIcon("minus.png"))
        self.minusButton4.setToolTip("Remove selected item from the list\nThis does not remove the item from your saved txt list")
        self.minusButton4.clicked.connect(lambda: self.remove(self.comboBox_4))
        # Clear buttons
        self.clearButton.setIcon(QIcon("delete.png"))
        self.clearButton.setToolTip("Clear all items from the list\nThis does not clear the items from your saved txt list")
        self.clearButton.clicked.connect(lambda: self.clear(self.comboBox))
        self.clearButton2.setIcon(QIcon("delete.png"))
        self.clearButton2.setToolTip("Clear all items from the list\nThis does not clear the items from your saved txt list")
        self.clearButton2.clicked.connect(lambda: self.clear(self.comboBox_2))
        self.clearButton3.setIcon(QIcon("delete.png"))
        self.clearButton3.setToolTip("Clear all items from the list\nThis does not clear the items from your saved txt list")
        self.clearButton3.clicked.connect(lambda: self.clear(self.comboBox_3))
        self.clearButton4.setIcon(QIcon("delete.png"))
        self.clearButton4.setToolTip("Clear all items from the list\nThis does not clear the items from your saved txt list")
        self.clearButton4.clicked.connect(lambda: self.clear(self.comboBox_4))

        self.startButton.clicked.connect(self.start)
        ############################################### END OF BUTTONS

        self.show()

    # Add item
    def add(self, cBox):
        cBox.addItem(cBox.currentText())
        self.blanker(cBox)
        self.log("Item added to list")

    # Remove item
    def remove(self, cBox):
        index = cBox.findText(cBox.currentText())
        cBox.removeItem(index)
        self.log("Item removed from list")

    # Clear list
    def clear(self, cBox):
        cBox.clear()
        self.log("Items cleared from list")

    # Grab current info and begin
    def start(self):
        username = self.comboBox.currentText()
        password = self.comboBox_2.currentText()
        url = self.comboBox_3.currentText()
        limit = self.comboBox_4.currentText()

        self.instances = self.instances + 1     # Increment chrome instance counter
        localappdata = os.environ.get("LOCALAPPDATA")
        seleniumdata = localappdata + "/Google/Chrome/Selenium" + str(self.instances)

        t = Thread(target=amazon.Amazon, args=(username, password, url, limit, seleniumdata, self.textBrowser))
        t.daemon = True
        t.start()

    # Reading in
    def readIn(self, cBox, itemsList):
        f = open(itemsList, 'r')
        for i in f.readlines():
            cBox.addItem(i.strip())
        f.close()

    # Writing out
    def save(self, cBox, file):
        self.writeOut(cBox, file)
        self.log("Items saved to " + file)
    # Helper function
    def writeOut(self, cBox, itemsList):
        AllItems = [cBox.itemText(i) for i in range(cBox.count())]
        with open(itemsList, 'w+') as f:
            for items in AllItems:
                f.write(items + "\n")
        f.close()

    # Blanker
    def blanker(self, cBox):
        cBox.setCurrentText("")

    # Logging
    def log(self, message):
        self.textBrowser.append(message)


# Remove old selenium data
my_dir = os.environ.get("LOCALAPPDATA") + "/Google/Chrome"
for fname in os.listdir(my_dir):
    if fname.startswith("Selenium"):
        shutil.rmtree(os.path.join(my_dir, fname))

# Launch program
app = QApplication(sys.argv)
app.setStyle("Fusion")
window = ShopBot()
sys.exit(app.exec())
