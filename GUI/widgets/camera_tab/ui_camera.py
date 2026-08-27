# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'camera.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
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
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSplitter, QWidget)

class Ui_camera(object):
    def setupUi(self, camera):
        if not camera.objectName():
            camera.setObjectName(u"camera")
        camera.resize(1760, 987)
        self.label = QLabel(camera)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, -60, 1211, 821))
        self.splitter = QSplitter(camera)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setGeometry(QRect(1320, 50, 101, 52))
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.get_control_btn = QPushButton(self.splitter)
        self.get_control_btn.setObjectName(u"get_control_btn")
        self.splitter.addWidget(self.get_control_btn)
        self.start_btn = QPushButton(self.splitter)
        self.start_btn.setObjectName(u"start_btn")
        self.splitter.addWidget(self.start_btn)
        self.splitter_5 = QSplitter(camera)
        self.splitter_5.setObjectName(u"splitter_5")
        self.splitter_5.setGeometry(QRect(1320, 110, 175, 91))
        self.splitter_5.setOrientation(Qt.Orientation.Vertical)
        self.label_11 = QLabel(self.splitter_5)
        self.label_11.setObjectName(u"label_11")
        self.splitter_5.addWidget(self.label_11)
        self.splitter_4 = QSplitter(self.splitter_5)
        self.splitter_4.setObjectName(u"splitter_4")
        self.splitter_4.setOrientation(Qt.Orientation.Vertical)
        self.splitter_3 = QSplitter(self.splitter_4)
        self.splitter_3.setObjectName(u"splitter_3")
        self.splitter_3.setOrientation(Qt.Orientation.Horizontal)
        self.label_4 = QLabel(self.splitter_3)
        self.label_4.setObjectName(u"label_4")
        self.splitter_3.addWidget(self.label_4)
        self.lineEdit_h = QLineEdit(self.splitter_3)
        self.lineEdit_h.setObjectName(u"lineEdit_h")
        self.splitter_3.addWidget(self.lineEdit_h)
        self.splitter_4.addWidget(self.splitter_3)
        self.splitter_2 = QSplitter(self.splitter_4)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Orientation.Horizontal)
        self.label_2 = QLabel(self.splitter_2)
        self.label_2.setObjectName(u"label_2")
        self.splitter_2.addWidget(self.label_2)
        self.lineEdit_w = QLineEdit(self.splitter_2)
        self.lineEdit_w.setObjectName(u"lineEdit_w")
        self.splitter_2.addWidget(self.lineEdit_w)
        self.splitter_4.addWidget(self.splitter_2)
        self.splitter_5.addWidget(self.splitter_4)
        self.send_dim_btn = QPushButton(self.splitter_5)
        self.send_dim_btn.setObjectName(u"send_dim_btn")
        self.splitter_5.addWidget(self.send_dim_btn)
        self.splitter_6 = QSplitter(camera)
        self.splitter_6.setObjectName(u"splitter_6")
        self.splitter_6.setGeometry(QRect(1320, 210, 122, 51))
        self.splitter_6.setOrientation(Qt.Orientation.Vertical)
        self.label_12 = QLabel(self.splitter_6)
        self.label_12.setObjectName(u"label_12")
        self.splitter_6.addWidget(self.label_12)
        self.fps_comboBox = QComboBox(self.splitter_6)
        self.fps_comboBox.addItem("")
        self.fps_comboBox.addItem("")
        self.fps_comboBox.addItem("")
        self.fps_comboBox.addItem("")
        self.fps_comboBox.addItem("")
        self.fps_comboBox.addItem("")
        self.fps_comboBox.addItem("")
        self.fps_comboBox.setObjectName(u"fps_comboBox")
        self.splitter_6.addWidget(self.fps_comboBox)

        self.retranslateUi(camera)

        QMetaObject.connectSlotsByName(camera)
    # setupUi

    def retranslateUi(self, camera):
        camera.setWindowTitle(QCoreApplication.translate("camera", u"Form", None))
        self.label.setText(QCoreApplication.translate("camera", u"TextLabel", None))
        self.get_control_btn.setText(QCoreApplication.translate("camera", u"get_control", None))
        self.start_btn.setText(QCoreApplication.translate("camera", u"start", None))
        self.label_11.setText(QCoreApplication.translate("camera", u"Enter detection shape ", None))
        self.label_4.setText(QCoreApplication.translate("camera", u"h [mm]", None))
        self.label_2.setText(QCoreApplication.translate("camera", u"w [mm]", None))
        self.send_dim_btn.setText(QCoreApplication.translate("camera", u"send", None))
        self.label_12.setText(QCoreApplication.translate("camera", u"Enter frame per second", None))
        self.fps_comboBox.setItemText(0, QCoreApplication.translate("camera", u"10", None))
        self.fps_comboBox.setItemText(1, QCoreApplication.translate("camera", u"1", None))
        self.fps_comboBox.setItemText(2, QCoreApplication.translate("camera", u"20", None))
        self.fps_comboBox.setItemText(3, QCoreApplication.translate("camera", u"30", None))
        self.fps_comboBox.setItemText(4, QCoreApplication.translate("camera", u"40", None))
        self.fps_comboBox.setItemText(5, QCoreApplication.translate("camera", u"50", None))
        self.fps_comboBox.setItemText(6, QCoreApplication.translate("camera", u"50", None))

    # retranslateUi

