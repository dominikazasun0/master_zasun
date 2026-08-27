# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'positioners.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QFrame,
    QGridLayout, QLabel, QLayout, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_positioners(object):
    def setupUi(self, positioners):
        if not positioners.objectName():
            positioners.setObjectName(u"positioners")
        positioners.resize(1088, 557)
        self.gridLayoutWidget = QWidget(positioners)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(20, 90, 511, 130))
        self.Positioner_gridLayout = QGridLayout(self.gridLayoutWidget)
        self.Positioner_gridLayout.setObjectName(u"Positioner_gridLayout")
        self.Positioner_gridLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.Positioner_gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.Positioner_gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        self.delay_comboBox = QComboBox(self.gridLayoutWidget)
        self.delay_comboBox.setObjectName(u"delay_comboBox")

        self.Positioner_gridLayout.addWidget(self.delay_comboBox, 2, 8, 1, 1)

        self.label_6 = QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName(u"label_6")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.Positioner_gridLayout.addWidget(self.label_6, 0, 6, 1, 1)

        self.target_posEntry = QLineEdit(self.gridLayoutWidget)
        self.target_posEntry.setObjectName(u"target_posEntry")

        self.Positioner_gridLayout.addWidget(self.target_posEntry, 1, 1, 1, 1)

        self.step_comboBox = QComboBox(self.gridLayoutWidget)
        self.step_comboBox.setObjectName(u"step_comboBox")

        self.Positioner_gridLayout.addWidget(self.step_comboBox, 2, 1, 1, 1)

        self.start_posEntry = QLineEdit(self.gridLayoutWidget)
        self.start_posEntry.setObjectName(u"start_posEntry")

        self.Positioner_gridLayout.addWidget(self.start_posEntry, 0, 1, 1, 1)

        self.label_2 = QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.Positioner_gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.Positioner_gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.step_entry = QLineEdit(self.gridLayoutWidget)
        self.step_entry.setObjectName(u"step_entry")
        self.step_entry.setEnabled(False)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.step_entry.sizePolicy().hasHeightForWidth())
        self.step_entry.setSizePolicy(sizePolicy1)
        self.step_entry.setMinimumSize(QSize(40, 0))

        self.Positioner_gridLayout.addWidget(self.step_entry, 2, 6, 1, 1)

        self.startButton = QPushButton(self.gridLayoutWidget)
        self.startButton.setObjectName(u"startButton")
        self.startButton.setMinimumSize(QSize(50, 0))

        self.Positioner_gridLayout.addWidget(self.startButton, 1, 6, 1, 1)

        self.label_5 = QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName(u"label_5")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy2)
        self.label_5.setMinimumSize(QSize(60, 0))

        self.Positioner_gridLayout.addWidget(self.label_5, 2, 7, 1, 1)

        self.rightButton = QPushButton(self.gridLayoutWidget)
        self.rightButton.setObjectName(u"rightButton")

        self.Positioner_gridLayout.addWidget(self.rightButton, 1, 8, 1, 1)

        self.leftButton = QPushButton(self.gridLayoutWidget)
        self.leftButton.setObjectName(u"leftButton")
        sizePolicy1.setHeightForWidth(self.leftButton.sizePolicy().hasHeightForWidth())
        self.leftButton.setSizePolicy(sizePolicy1)
        self.leftButton.setMinimumSize(QSize(75, 0))

        self.Positioner_gridLayout.addWidget(self.leftButton, 1, 7, 1, 1)

        self.setButton = QPushButton(self.gridLayoutWidget)
        self.setButton.setObjectName(u"setButton")

        self.Positioner_gridLayout.addWidget(self.setButton, 0, 8, 1, 1)

        self.actual_posLabel = QLabel(self.gridLayoutWidget)
        self.actual_posLabel.setObjectName(u"actual_posLabel")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.actual_posLabel.setFont(font)
        self.actual_posLabel.setFrameShape(QFrame.Shape.NoFrame)
        self.actual_posLabel.setFrameShadow(QFrame.Shadow.Plain)
        self.actual_posLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.Positioner_gridLayout.addWidget(self.actual_posLabel, 0, 7, 1, 1)

        self.formLayoutWidget = QWidget(positioners)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(20, 10, 381, 31))
        self.formLayout_2 = QFormLayout(self.formLayoutWidget)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_name = QLabel(self.formLayoutWidget)
        self.label_name.setObjectName(u"label_name")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.label_name)

        self.energizeButton = QPushButton(self.formLayoutWidget)
        self.energizeButton.setObjectName(u"energizeButton")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.energizeButton)

        self.formLayoutWidget_2 = QWidget(positioners)
        self.formLayoutWidget_2.setObjectName(u"formLayoutWidget_2")
        self.formLayoutWidget_2.setGeometry(QRect(20, 40, 381, 31))
        self.formLayout = QFormLayout(self.formLayoutWidget_2)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.current_limitEntry = QLineEdit(self.formLayoutWidget_2)
        self.current_limitEntry.setObjectName(u"current_limitEntry")
        sizePolicy1.setHeightForWidth(self.current_limitEntry.sizePolicy().hasHeightForWidth())
        self.current_limitEntry.setSizePolicy(sizePolicy1)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.current_limitEntry)

        self.label_4 = QLabel(self.formLayoutWidget_2)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_4)

        self.reqCtrl = QPushButton(positioners)
        self.reqCtrl.setObjectName(u"reqCtrl")
        self.reqCtrl.setGeometry(QRect(420, 10, 111, 31))

        self.retranslateUi(positioners)

        QMetaObject.connectSlotsByName(positioners)
    # setupUi

    def retranslateUi(self, positioners):
        positioners.setWindowTitle(QCoreApplication.translate("positioners", u"Form", None))
        self.label_3.setText(QCoreApplication.translate("positioners", u"target position", None))
        self.label_6.setText(QCoreApplication.translate("positioners", u"current position", None))
        self.target_posEntry.setText(QCoreApplication.translate("positioners", u"90", None))
        self.start_posEntry.setText(QCoreApplication.translate("positioners", u"0", None))
        self.label_2.setText(QCoreApplication.translate("positioners", u"Step [deg]", None))
        self.label.setText(QCoreApplication.translate("positioners", u"start position", None))
        self.step_entry.setText(QCoreApplication.translate("positioners", u"0.9", None))
        self.startButton.setText(QCoreApplication.translate("positioners", u"Start", None))
        self.label_5.setText(QCoreApplication.translate("positioners", u"delay [ms]", None))
        self.rightButton.setText(QCoreApplication.translate("positioners", u">", None))
        self.leftButton.setText(QCoreApplication.translate("positioners", u"<", None))
        self.setButton.setText(QCoreApplication.translate("positioners", u"Set to 0", None))
        self.actual_posLabel.setText(QCoreApplication.translate("positioners", u"0", None))
        self.label_name.setText(QCoreApplication.translate("positioners", u"name", None))
        self.energizeButton.setText(QCoreApplication.translate("positioners", u"Energize", None))
        self.current_limitEntry.setText(QCoreApplication.translate("positioners", u"800", None))
        self.label_4.setText(QCoreApplication.translate("positioners", u"Current Limit [mA]", None))
        self.reqCtrl.setText(QCoreApplication.translate("positioners", u"Get Control", None))
    # retranslateUi

