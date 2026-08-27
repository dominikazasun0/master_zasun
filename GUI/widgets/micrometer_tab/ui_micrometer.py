# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'micrometer.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_micrometer(object):
    def setupUi(self, micrometer):
        if not micrometer.objectName():
            micrometer.setObjectName(u"micrometer")
        micrometer.resize(1088, 557)
        self.horizontalLayoutWidget = QWidget(micrometer)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(90, 220, 461, 80))
        self.refresh_layout = QHBoxLayout(self.horizontalLayoutWidget)
        self.refresh_layout.setObjectName(u"refresh_layout")
        self.refresh_layout.setContentsMargins(0, 0, 0, 0)
        self.refresh_label = QLabel(self.horizontalLayoutWidget)
        self.refresh_label.setObjectName(u"refresh_label")

        self.refresh_layout.addWidget(self.refresh_label)

        self.delay_comboBox = QComboBox(self.horizontalLayoutWidget)
        self.delay_comboBox.setObjectName(u"delay_comboBox")

        self.refresh_layout.addWidget(self.delay_comboBox)

        self.verticalLayoutWidget = QWidget(micrometer)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(90, 120, 461, 80))
        self.layout = QVBoxLayout(self.verticalLayoutWidget)
        self.layout.setObjectName(u"layout")
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.layout.addWidget(self.label_3)

        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")

        self.layout.addWidget(self.label)

        self.startButton = QPushButton(micrometer)
        self.startButton.setObjectName(u"startButton")
        self.startButton.setGeometry(QRect(560, 120, 82, 71))
        self.reqCtrl = QPushButton(micrometer)
        self.reqCtrl.setObjectName(u"reqCtrl")
        self.reqCtrl.setGeometry(QRect(560, 50, 82, 28))

        self.retranslateUi(micrometer)

        QMetaObject.connectSlotsByName(micrometer)
    # setupUi

    def retranslateUi(self, micrometer):
        micrometer.setWindowTitle(QCoreApplication.translate("micrometer", u"Form", None))
        self.refresh_label.setText(QCoreApplication.translate("micrometer", u"Delay [ms]", None))
        self.label_3.setText(QCoreApplication.translate("micrometer", u"Latest data", None))
        self.label.setText(QCoreApplication.translate("micrometer", u"waiting for data ...", None))
        self.startButton.setText(QCoreApplication.translate("micrometer", u"Start", None))
        self.reqCtrl.setText(QCoreApplication.translate("micrometer", u"getControl", None))
    # retranslateUi

