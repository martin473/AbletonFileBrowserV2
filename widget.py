# This Python file uses the following encoding: utf-8
import sys, argparse, time, os, json
# using subprocess instead of os call is neater apparently and cross platform, but I'm getting permissions errors with it on mac and not with os

from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QTableWidgetItem, QLabel, QInputDialog
from PySide6.QtGui import QStandardItemModel, QStandardItem, QPixmap
from PySide6.QtCore import Qt

from abletoolz import cli
import re
from tinydb import TinyDB, where, Query

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_Widget


class ImgWidget1(QLabel): #hardcoded image,

    def __init__(self, parent=None):
        super(ImgWidget1, self).__init__(parent)
        pic = QPixmap("./assets/ui_form.png")
        #add a dir list of files or something here
        self.setPixmap(pic)
        scaled = pic.scaled(
            100, 20,
            Qt.KeepAspectRatio) #set image size here x, y as 100, 20, have it autosize to parent size
        self.setPixmap(scaled)

def openProject(row, column):
    if column == 0: #checks for proper cell   
        os.system("open " + "\'" + getFpath(row)  + "\'") #need another command for windows and checking os type
        #os.system needs filepath whitespace to be formatted like "open '/this/is/ your filepath'"

def setFavorite(row, column):
    if column == 1: #checks for proper cell
        #get db
        try:
            db = TinyDB('db.json')
            data = db.all()
        except Exception as e:
            print("Couldn't load db", e)
        fPath = getFpath(row)

        #fetch and update line
        newRow = db.search(where("Path") == fPath)
        db.update({"Favorite": not newRow[0]["Favorite"]}, where("Path") == fPath)

        #fetch updated line and display
        newRow = db.search(where("Path") == fPath)
        widget.ui.tableWidget.setItem(row, 1, QTableWidgetItem( getFavIcon(newRow[0]["Favorite"]) ))

def setTags(row, column):
    if column == 2: #checks for proper cell
        #get db
        try:
            db = TinyDB('db.json')
            data = db.all()
        except Exception as e:
            print("Couldn't load db", e)
        fPath = getFpath(row)

        #get old tags, user input (there's definitely a simpler way to do this, but this works)
        newRow = db.search(where("Path") == fPath)
        newTags = newRow[0]["Tags"]
        dialog = QInputDialog()
        dialog.setLabelText("Tags")
        dialog.setTextValue(newTags)
        clickedButton = dialog.exec()

        #update line and refresh or don't
        if clickedButton:
            db.update({"Tags": dialog.textValue()}, where("Path") == fPath)
            newRow = db.search(where("Path") == fPath)
            widget.ui.tableWidget.setItem(row, 2, QTableWidgetItem(newRow[0]["Tags"]))
        else:
            print("tags not updated")

def getFavIcon(favorite):
        if favorite == True:
            return "♥️"
        if favorite == False:
            return "🖤"
        else:
            return "Empty"

def getFpath(row):
    #would like this to grab the column that has fpath so I can move it around if needed, it's hard coded
    #also item works, itemAt always returns item 0,0 https://stackoverflow.com/questions/2984287/qtablewidgetitemat-returns-seemingly-random-items
    return widget.ui.tableWidget.item(row, 5).text()


def readableTime(timestamp):
    return time.ctime(timestamp)

def openFolder(self): #not sure if C dir will mess things up on other systems, I'd like to remove it
        folder = QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QFileDialog.ShowDirsOnly)
        try:
            print("making table")
            makeTable(self, folder)
            print("populating db")
            populateDb(self, folder)
            print("filling table with data")
            fillTable(self)
        except Exception as e:
            print("Error: ", e)

def makeTable(self, folder): #deleteDummy image when importing actual file ratings

    #Load parent dir
    try:
        print("Getting data")
        data = cli.get_pathlib_objects([str(folder)])
        print(data)
    except Exception as e:
        print("couldn't parse parent directory", e)

    #create table display schema
    try:
        print("setting schema")
        widget.ui.tableWidget.setRowCount(len(data))
        headerLabels = ["Name", "Favorite", "Tags", "Opened", "Created", "Location"]
        widget.ui.tableWidget.setColumnCount(len(headerLabels))
        widget.ui.tableWidget.setHorizontalHeaderLabels(headerLabels)
    except Exception as e:
        print("Table creation error", e)

def makeTableInit(self): #deleteDummy image when importing actual file ratings

    #open db
    try:
        db = TinyDB('db.json')
        data = db.all()
    except Exception as e:
        print("Couldn't load db", e)

    #create table display schema
    try:
        print("setting schema")
        widget.ui.tableWidget.setRowCount(len(data))
        headerLabels = ["Name", "Favorite", "Tags", "Opened", "Created", "Location"]
        widget.ui.tableWidget.setColumnCount(len(headerLabels))
        widget.ui.tableWidget.setHorizontalHeaderLabels(headerLabels)
    except Exception as e:
        print("Table creation error", e)

def populateDb(self, folder): #deleteDummy image when importing actual file ratings
    #gets filetree as list
    try:
        print("generating data")
        data = cli.get_pathlib_objects([str(folder)])
    except Exception as e:
        print("filepath error", e)

    #try to init or load a db
    try:
        db = TinyDB('db.json')
    except Exception as e:
        print("DB instance error", e)

    try:
        print("saving data")
        for dir in data:
            dateCreated = readableTime(os.path.getctime(dir)) 
            dateModified = readableTime(os.path.getctime(dir))
            name = str(os.path.basename(dir)) #other methods https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format
            db.insert({"Path": str(dir) , "Name": name, "Favorite": False, "Tags": "", "Opened": dateModified, "Created": dateCreated})
    except Exception as e:
        print("Table population error", e)

def fillTable(self):
    try:
        db = TinyDB('db.json')
        data = db.all()
    except Exception as e:
        print("Couldn't load db", e)

    try:
        for i, entry in enumerate(data):
            #load db line into memory
            path = entry["Path"]
            name = entry["Name"]
            favorite = entry["Favorite"]
            tags = entry["Tags"]
            dateModified = entry["Opened"]
            dateCreated = entry["Created"] #ctime should work for mac and windows but not other unix systems

            #enter db line into display table
            widget.ui.tableWidget.setItem(i, 0, QTableWidgetItem(name))
            widget.ui.tableWidget.setItem(i, 1, QTableWidgetItem( getFavIcon(favorite) ))
            widget.ui.tableWidget.setItem(i, 2, QTableWidgetItem(tags))
            widget.ui.tableWidget.setItem(i, 3, QTableWidgetItem(dateModified))
            widget.ui.tableWidget.setItem(i, 4, QTableWidgetItem(dateCreated))
            widget.ui.tableWidget.setItem(i, 5, QTableWidgetItem(path))
    except Exception as e: #potential better way to organize this? https://stackoverflow.com/questions/6785481/how-to-implement-a-filter-option-in-qtablewidget
        print("Table population error", e)

def searchFiles():
    userSearch = widget.ui.searchBar.text()
    if userSearch:
        db = TinyDB('db.json')
        songs = Query()
        results = db.search((songs.Name.search(userSearch, flags=re.IGNORECASE)) | (songs.Tags.search(userSearch, flags=re.IGNORECASE))) # .search(search, flags=re.IGNORECASE)) this uses regex to match any substring in the field
        print(results)
        #create table display schema
        try:
            print("setting schema")
            widget.ui.tableWidget.setRowCount(len(results))
            headerLabels = ["Name", "Favorite", "Tags", "Opened", "Created", "Location"]
            widget.ui.tableWidget.setColumnCount(len(headerLabels))
            widget.ui.tableWidget.setHorizontalHeaderLabels(headerLabels)
        except Exception as e:
            print("Table creation error", e)

        #fill table
        try:
            for i, entry in enumerate(results):
                #load db line into memory
                path = entry["Path"]
                name = entry["Name"]
                favorite = entry["Favorite"]
                tags = entry["Tags"]
                dateModified = entry["Opened"]
                dateCreated = entry["Created"] #ctime should work for mac and windows but not other unix systems

                #enter db line into display table
                widget.ui.tableWidget.setItem(i, 0, QTableWidgetItem(name))
                widget.ui.tableWidget.setItem(i, 1, QTableWidgetItem( getFavIcon(favorite) ))
                widget.ui.tableWidget.setItem(i, 2, QTableWidgetItem(tags))
                widget.ui.tableWidget.setItem(i, 3, QTableWidgetItem(dateModified))
                widget.ui.tableWidget.setItem(i, 4, QTableWidgetItem(dateCreated))
                widget.ui.tableWidget.setItem(i, 5, QTableWidgetItem(path))
        except Exception as e: #potential better way to organize this? https://stackoverflow.com/questions/6785481/how-to-implement-a-filter-option-in-qtablewidget
            print("Table population error", e)
    else:
        makeTableInit("dummy text")
        fillTable("dummy text")

    print(widget.ui.searchBar.text())

class Widget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)


        #UI COMPONENTS tableWidget and Buttons
        self.ui.tableWidget.show()
        self.ui.folderButton.clicked.connect(openFolder)
        self.ui.searchButton.clicked.connect(searchFiles)
        self.ui.tableWidget.cellDoubleClicked.connect(openProject)
        self.ui.tableWidget.cellDoubleClicked.connect(setFavorite)
        self.ui.tableWidget.cellDoubleClicked.connect(setTags)

    def initDB(self):
        print("running initdb")
        #issue is how I'm calling things, the entire script could be cleaned up, but I can't init the db before the widget object is created
        try:
            print("trying initdb")
            if os.path.isfile("db.json"):
                print("found db")
                makeTableInit(self)
                fillTable(self)
            else:
                print("No db")
        except Exception as e:
            print("Init db error", e)

    def getDummy(a):
        #a is not used, not sure what it's passing in automatically
        return self.dummyImage

if __name__ == "__main__":    
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    widget.initDB()
    sys.exit(app.exec())

