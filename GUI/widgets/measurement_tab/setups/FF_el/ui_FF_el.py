# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FF_el.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QTabWidget, QVBoxLayout,
    QWidget)

class Ui_FF_el(object):
    def setupUi(self, FF_el):
        if not FF_el.objectName():
            FF_el.setObjectName(u"FF_el")
        FF_el.resize(970, 648)
        self.verticalLayout_2 = QVBoxLayout(FF_el)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tabWidget = QTabWidget(FF_el)
        self.tabWidget.setObjectName(u"tabWidget")
        self.setup_tab = QWidget()
        self.setup_tab.setObjectName(u"setup_tab")
        self.verticalLayout = QVBoxLayout(self.setup_tab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.dev_label = QLabel(self.setup_tab)
        self.dev_label.setObjectName(u"dev_label")

        self.horizontalLayout.addWidget(self.dev_label)

        self.label_dev_name = QLabel(self.setup_tab)
        self.label_dev_name.setObjectName(u"label_dev_name")

        self.horizontalLayout.addWidget(self.label_dev_name)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.start_btn = QPushButton(self.setup_tab)
        self.start_btn.setObjectName(u"start_btn")

        self.horizontalLayout_2.addWidget(self.start_btn)

        self.pause_btn = QPushButton(self.setup_tab)
        self.pause_btn.setObjectName(u"pause_btn")

        self.horizontalLayout_2.addWidget(self.pause_btn)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.tabWidget.addTab(self.setup_tab, "")
        self.results_tab = QWidget()
        self.results_tab.setObjectName(u"results_tab")
        self.tabWidget.addTab(self.results_tab, "")

        self.verticalLayout_2.addWidget(self.tabWidget)


        self.retranslateUi(FF_el)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(FF_el)
    # setupUi

    def retranslateUi(self, FF_el):
        FF_el.setWindowTitle(QCoreApplication.translate("FF_el", u"Form", None))
        self.dev_label.setText(QCoreApplication.translate("FF_el", u"Devices:", None))
        self.label_dev_name.setText("")
        self.start_btn.setText(QCoreApplication.translate("FF_el", u"Start", None))
        self.pause_btn.setText(QCoreApplication.translate("FF_el", u"Pause", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.setup_tab), QCoreApplication.translate("FF_el", u"Setup", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.results_tab), QCoreApplication.translate("FF_el", u"Results", None))
    # retranslateUi

