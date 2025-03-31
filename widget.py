# This Python file uses the following encoding: utf-8
import sys, argparse, time, os, json
# using subprocess instead of os call is neater apparently and cross platform, but I'm getting permissions errors with it on mac and not with os
# a good refactor for this code would be to properly implement qt's model view paradigm and signal paradigm and to have a better control on where the db is instantiated within this file
# current db paradigm is when db is called, instantiate it locally, update the db, fetch the value, and update the GUI with the fetched value, fpath is primary key

#pyside imports
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QTableWidgetItem, QLabel, QInputDialog
from PySide6.QtGui import QStandardItemModel, QStandardItem, QPixmap
from PySide6.QtCore import Qt

#other imports
from abletoolz import cli
import re
from tinydb import TinyDB, where, Query

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_Widget

#generates a placeholder image for star ratings, feature was replaced with heart emoji favorites
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

#uses os and local method to open a folder
def openProject(row, column):
    if column == 0: #checks for proper cell   
        os.system("open " + "\'" + getFpath(row)  + "\'") #need another command for windows and checking os type
        #os.system needs filepath whitespace to be formatted like "open '/this/is/ your filepath'"

#updates favorite/unfavorite on click
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
        #flips boolean value for favorite in db table
        newRow = db.search(where("Path") == fPath)
        db.update({"Favorite": not newRow[0]["Favorite"]}, where("Path") == fPath)

        #fetch updated favorite info and display
        newRow = db.search(where("Path") == fPath)
        widget.ui.tableWidget.setItem(row, 1, QTableWidgetItem( getFavIcon(newRow[0]["Favorite"]) ))

# lets user enter csv tags on click, string type, not enforced
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

# returns proper fav icon based on favorite T/F value in db
def getFavIcon(favorite):
        if favorite == True:
            return "♥️"
        if favorite == False:
            return "🖤"
        else:
            return "Empty"

# fpath is pkey, grabs hardcoded column location based on row that is clicked on, returning fpath as pkey for use in db calls
def getFpath(row):
    #would like this to grab the column that has fpath so I can move it around if needed, it's hard coded
    #also item works, itemAt always returns item 0,0 https://stackoverflow.com/questions/2984287/qtablewidgetitemat-returns-seemingly-random-items
    return widget.ui.tableWidget.item(row, 5).text()

#uses ctime, which is not properly implemented currently. Sorting on ctime gives strange results
def readableTime(timestamp):
    return time.ctime(timestamp)

# button click starts open directory system dialogue, selecting a folder runs local methods that update local data, populate a db with that data, and then update the GUI with the db data
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

# uses a parent/root folder location to use abletoolz cli method to get all of the subfolders and .als files
# creates GUI table headers
# refactoring could clean this method up and separate it into multiple simpler methods
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

# same as make table above except the software tries this first to see if there's a pre-existing db to load (so the user doesn't have to create a new one every time they start the software)
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

#creates a tinyDB instance variable and creates a db file on local system, uses abletoolz cli method to populate db with data, uses os methods to get file data
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

#assumes db exists, is similar to maketableinit, goes through an existing db and fills table columns with appropriate data
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

# enables search bar to do basic text query powered by tinydb methods. Could be a source of some errors. Clears table and fills it with data returned from the tinydb search
# searching for nothing returns the entire db and is the equivalent of clearing the search bar to get everything
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

#main widget logic, creates the main GUI widget, creates and displays components and connects methods to components and buttons, runs init db when started to try to fill table with pre-existing data calls maketableinit as well
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

#main logic that creates the application, the GUI widget, and calls init methods
if __name__ == "__main__":    
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    widget.initDB()
    sys.exit(app.exec())

