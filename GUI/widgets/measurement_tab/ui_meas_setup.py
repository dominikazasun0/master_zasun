# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'meas_setup.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QVBoxLayout, QWidget)

class Ui_measurement(object):
    def setupUi(self, measurement):
        if not measurement.objectName():
            measurement.setObjectName(u"measurement")
        measurement.resize(970, 648)
        self.verticalLayout = QVBoxLayout(measurement)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.setup_label = QLabel(measurement)
        self.setup_label.setObjectName(u"setup_label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.setup_label.sizePolicy().hasHeightForWidth())
        self.setup_label.setSizePolicy(sizePolicy)
        self.setup_label.setMinimumSize(QSize(160, 0))

        self.horizontalLayout_2.addWidget(self.setup_label)

        self.setup_comboBox = QComboBox(measurement)
        self.setup_comboBox.setObjectName(u"setup_comboBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.setup_comboBox.sizePolicy().hasHeightForWidth())
        self.setup_comboBox.setSizePolicy(sizePolicy1)
        self.setup_comboBox.setMinimumSize(QSize(100, 28))

        self.horizontalLayout_2.addWidget(self.setup_comboBox)

        self.dev_name = QLabel(measurement)
        self.dev_name.setObjectName(u"dev_name")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.dev_name.sizePolicy().hasHeightForWidth())
        self.dev_name.setSizePolicy(sizePolicy2)
        self.dev_name.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_2.addWidget(self.dev_name)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.reqCtrl_btn = QPushButton(measurement)
        self.reqCtrl_btn.setObjectName(u"reqCtrl_btn")

        self.horizontalLayout_2.addWidget(self.reqCtrl_btn)

        self.startButton = QPushButton(measurement)
        self.startButton.setObjectName(u"startButton")
        sizePolicy1.setHeightForWidth(self.startButton.sizePolicy().hasHeightForWidth())
        self.startButton.setSizePolicy(sizePolicy1)
        self.startButton.setMinimumSize(QSize(100, 60))

        self.horizontalLayout_2.addWidget(self.startButton)

        self.pauseButton = QPushButton(measurement)
        self.pauseButton.setObjectName(u"pauseButton")
        self.pauseButton.setMinimumSize(QSize(100, 60))

        self.horizontalLayout_2.addWidget(self.pauseButton)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 10)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.setup_widget = QStackedWidget(measurement)
        self.setup_widget.setObjectName(u"setup_widget")
        self.page_empty = QWidget()
        self.page_empty.setObjectName(u"page_empty")
        self.setup_widget.addWidget(self.page_empty)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.setup_widget.addWidget(self.page_4)

        self.verticalLayout.addWidget(self.setup_widget)


        self.retranslateUi(measurement)

        self.setup_widget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(measurement)
    # setupUi

    def retranslateUi(self, measurement):
        measurement.setWindowTitle(QCoreApplication.translate("measurement", u"Form", None))
        self.setup_label.setText(QCoreApplication.translate("measurement", u"MEASUREMENT SETUP", None))
        self.dev_name.setText(QCoreApplication.translate("measurement", u"Devices:", None))
        self.reqCtrl_btn.setText(QCoreApplication.translate("measurement", u"Get Control", None))
        self.startButton.setText(QCoreApplication.translate("measurement", u"START", None))
        self.pauseButton.setText(QCoreApplication.translate("measurement", u"Pause", None))
    # retranslateUi

