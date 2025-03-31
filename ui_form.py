# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QTableWidget, QTableWidgetItem,
    QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(800, 600)
        icon = QIcon()
        icon.addFile(u"../../../../../../nova logo.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        Widget.setWindowIcon(icon)
        self.folderButton = QPushButton(Widget)
        self.folderButton.setObjectName(u"folderButton")
        self.folderButton.setGeometry(QRect(10, 0, 111, 32))
        self.folderButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.tableWidget = QTableWidget(Widget)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(10, 30, 781, 561))
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.verticalHeader().setProperty(u"showSortIndicator", False)
        self.searchBar = QLineEdit(Widget)
        self.searchBar.setObjectName(u"searchBar")
        self.searchBar.setGeometry(QRect(331, 4, 355, 21))
        self.searchButton = QPushButton(Widget)
        self.searchButton.setObjectName(u"searchButton")
        self.searchButton.setGeometry(QRect(690, -1, 100, 32))
        self.label = QLabel(Widget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(126, 1, 28, 28))
        self.label.setPixmap(QPixmap(u"../../../../../../nova logo.ico"))
        self.label.setScaledContents(True)
        self.label_2 = QLabel(Widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(158, 6, 174, 16))

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Nova's Song Organizer", None))
        self.folderButton.setText(QCoreApplication.translate("Widget", u"Choose Folder ...", None))
        self.searchButton.setText(QCoreApplication.translate("Widget", u"Search", None))
        self.label.setText("")
        self.label_2.setText(QCoreApplication.translate("Widget", u"novanewchorus@gmail.com", None))
    # retranslateUi

