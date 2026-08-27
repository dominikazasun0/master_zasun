# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'vna.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QPushButton, QRadioButton, QSizePolicy, QWidget)

class Ui_vna(object):
    def setupUi(self, vna):
        if not vna.objectName():
            vna.setObjectName(u"vna")
        vna.resize(1125, 578)
        self.plotWidgetPlaceholder = QWidget(vna)
        self.plotWidgetPlaceholder.setObjectName(u"plotWidgetPlaceholder")
        self.plotWidgetPlaceholder.setGeometry(QRect(20, 40, 550, 350))
        self.getTrace = QPushButton(vna)
        self.getTrace.setObjectName(u"getTrace")
        self.getTrace.setGeometry(QRect(590, 60, 101, 71))
        self.label_name = QLabel(vna)
        self.label_name.setObjectName(u"label_name")
        self.label_name.setGeometry(QRect(100, 10, 411, 20))
        self.traceLabel = QLabel(vna)
        self.traceLabel.setObjectName(u"traceLabel")
        self.traceLabel.setGeometry(QRect(600, 160, 63, 20))
        self.fstartEntry = QLineEdit(vna)
        self.fstartEntry.setObjectName(u"fstartEntry")
        self.fstartEntry.setGeometry(QRect(590, 290, 81, 26))
        self.fstopEntry = QLineEdit(vna)
        self.fstopEntry.setObjectName(u"fstopEntry")
        self.fstopEntry.setGeometry(QRect(700, 290, 81, 26))
        self.fstartLabel = QLabel(vna)
        self.fstartLabel.setObjectName(u"fstartLabel")
        self.fstartLabel.setGeometry(QRect(600, 260, 63, 20))
        self.fstopLabel = QLabel(vna)
        self.fstopLabel.setObjectName(u"fstopLabel")
        self.fstopLabel.setGeometry(QRect(710, 260, 63, 20))
        self.NLabel = QLabel(vna)
        self.NLabel.setObjectName(u"NLabel")
        self.NLabel.setGeometry(QRect(600, 340, 31, 20))
        self.NEntry = QLineEdit(vna)
        self.NEntry.setObjectName(u"NEntry")
        self.NEntry.setGeometry(QRect(590, 360, 81, 26))
        self.tracelistWidget = QListWidget(vna)
        QListWidgetItem(self.tracelistWidget)
        QListWidgetItem(self.tracelistWidget)
        QListWidgetItem(self.tracelistWidget)
        QListWidgetItem(self.tracelistWidget)
        self.tracelistWidget.setObjectName(u"tracelistWidget")
        self.tracelistWidget.setGeometry(QRect(590, 180, 101, 71))
        self.tracelistWidget.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.reqCtrl = QPushButton(vna)
        self.reqCtrl.setObjectName(u"reqCtrl")
        self.reqCtrl.setGeometry(QRect(740, 40, 101, 31))
        self.f_units_comboBox = QComboBox(vna)
        self.f_units_comboBox.setObjectName(u"f_units_comboBox")
        self.f_units_comboBox.setGeometry(QRect(800, 290, 81, 26))
        self.ymaxEntry = QLineEdit(vna)
        self.ymaxEntry.setObjectName(u"ymaxEntry")
        self.ymaxEntry.setGeometry(QRect(10, 10, 71, 26))
        self.yminEntry = QLineEdit(vna)
        self.yminEntry.setObjectName(u"yminEntry")
        self.yminEntry.setGeometry(QRect(10, 390, 71, 26))
        self.format_comboBox = QComboBox(vna)
        self.format_comboBox.setObjectName(u"format_comboBox")
        self.format_comboBox.setGeometry(QRect(700, 180, 87, 26))
        self.radioA = QRadioButton(vna)
        self.radioA.setObjectName(u"radioA")
        self.radioA.setGeometry(QRect(800, 180, 121, 24))
        self.radioB = QRadioButton(vna)
        self.radioB.setObjectName(u"radioB")
        self.radioB.setGeometry(QRect(800, 210, 121, 24))
        self.power_comboBox = QComboBox(vna)
        self.power_comboBox.setObjectName(u"power_comboBox")
        self.power_comboBox.setGeometry(QRect(800, 360, 81, 26))
        self.format_label = QLabel(vna)
        self.format_label.setObjectName(u"format_label")
        self.format_label.setGeometry(QRect(700, 160, 63, 20))
        self.RF_checkBox = QCheckBox(vna)
        self.RF_checkBox.setObjectName(u"RF_checkBox")
        self.RF_checkBox.setGeometry(QRect(710, 360, 90, 24))
        self.delay_comboBox = QComboBox(vna)
        self.delay_comboBox.setObjectName(u"delay_comboBox")
        self.delay_comboBox.setGeometry(QRect(800, 100, 81, 26))
        self.label = QLabel(vna)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(720, 100, 71, 20))

        self.retranslateUi(vna)

        QMetaObject.connectSlotsByName(vna)
    # setupUi

    def retranslateUi(self, vna):
        vna.setWindowTitle(QCoreApplication.translate("vna", u"Form", None))
        self.getTrace.setText(QCoreApplication.translate("vna", u"Read VNA", None))
        self.label_name.setText(QCoreApplication.translate("vna", u"vna name", None))
        self.traceLabel.setText(QCoreApplication.translate("vna", u"traces", None))
        self.fstartLabel.setText(QCoreApplication.translate("vna", u"f start", None))
        self.fstopLabel.setText(QCoreApplication.translate("vna", u"f stop", None))
        self.NLabel.setText(QCoreApplication.translate("vna", u"N", None))
        self.NEntry.setText(QCoreApplication.translate("vna", u"1001", None))

        __sortingEnabled = self.tracelistWidget.isSortingEnabled()
        self.tracelistWidget.setSortingEnabled(False)
        ___qlistwidgetitem = self.tracelistWidget.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("vna", u"S11", None));
        ___qlistwidgetitem1 = self.tracelistWidget.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("vna", u"S12", None));
        ___qlistwidgetitem2 = self.tracelistWidget.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("vna", u"S21", None));
        ___qlistwidgetitem3 = self.tracelistWidget.item(3)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("vna", u"S22", None));
        self.tracelistWidget.setSortingEnabled(__sortingEnabled)

        self.reqCtrl.setText(QCoreApplication.translate("vna", u"Get Control", None))
        self.ymaxEntry.setText(QCoreApplication.translate("vna", u"-10", None))
        self.yminEntry.setText(QCoreApplication.translate("vna", u"-100", None))
        self.radioA.setText(QCoreApplication.translate("vna", u"amp [dB]", None))
        self.radioB.setText(QCoreApplication.translate("vna", u"phase [deg]", None))
        self.format_label.setText(QCoreApplication.translate("vna", u"format", None))
        self.RF_checkBox.setText(QCoreApplication.translate("vna", u"RF power", None))
        self.label.setText(QCoreApplication.translate("vna", u"delay [ms]", None))
    # retranslateUi

