# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FF_az.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_FF_az(object):
    def setupUi(self, FF_az):
        if not FF_az.objectName():
            FF_az.setObjectName(u"FF_az")
        FF_az.resize(1200, 480)
        self.verticalLayout_2 = QVBoxLayout(FF_az)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.start_posEntry = QLineEdit(FF_az)
        self.start_posEntry.setObjectName(u"start_posEntry")

        self.gridLayout.addWidget(self.start_posEntry, 1, 2, 1, 1)

        self.freq_comboBox = QComboBox(FF_az)
        self.freq_comboBox.setObjectName(u"freq_comboBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.freq_comboBox.sizePolicy().hasHeightForWidth())
        self.freq_comboBox.setSizePolicy(sizePolicy)
        self.freq_comboBox.setMinimumSize(QSize(150, 0))

        self.gridLayout.addWidget(self.freq_comboBox, 1, 9, 1, 1)

        self.stop_posLabel = QLabel(FF_az)
        self.stop_posLabel.setObjectName(u"stop_posLabel")

        self.gridLayout.addWidget(self.stop_posLabel, 1, 4, 1, 1)

        self.start_pos_Label = QLabel(FF_az)
        self.start_pos_Label.setObjectName(u"start_pos_Label")

        self.gridLayout.addWidget(self.start_pos_Label, 1, 0, 1, 1)

        self.freqLabel = QLabel(FF_az)
        self.freqLabel.setObjectName(u"freqLabel")

        self.gridLayout.addWidget(self.freqLabel, 1, 8, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 1, 7, 1, 1)

        self.current_posLabel = QLabel(FF_az)
        self.current_posLabel.setObjectName(u"current_posLabel")
        sizePolicy.setHeightForWidth(self.current_posLabel.sizePolicy().hasHeightForWidth())
        self.current_posLabel.setSizePolicy(sizePolicy)
        self.current_posLabel.setMinimumSize(QSize(150, 0))

        self.gridLayout.addWidget(self.current_posLabel, 1, 3, 1, 1)

        self.stepLabel = QLabel(FF_az)
        self.stepLabel.setObjectName(u"stepLabel")
        sizePolicy.setHeightForWidth(self.stepLabel.sizePolicy().hasHeightForWidth())
        self.stepLabel.setSizePolicy(sizePolicy)
        self.stepLabel.setMinimumSize(QSize(150, 0))

        self.gridLayout.addWidget(self.stepLabel, 1, 6, 1, 1)

        self.stop_posEntry = QLineEdit(FF_az)
        self.stop_posEntry.setObjectName(u"stop_posEntry")

        self.gridLayout.addWidget(self.stop_posEntry, 1, 5, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.plot2DWidgetPlaceholder = QWidget(FF_az)
        self.plot2DWidgetPlaceholder.setObjectName(u"plot2DWidgetPlaceholder")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.plot2DWidgetPlaceholder.sizePolicy().hasHeightForWidth())
        self.plot2DWidgetPlaceholder.setSizePolicy(sizePolicy1)
        self.plot2DWidgetPlaceholder.setMinimumSize(QSize(0, 350))

        self.horizontalLayout_3.addWidget(self.plot2DWidgetPlaceholder)

        self.plot3DWidgetPlaceholder = QWidget(FF_az)
        self.plot3DWidgetPlaceholder.setObjectName(u"plot3DWidgetPlaceholder")
        sizePolicy1.setHeightForWidth(self.plot3DWidgetPlaceholder.sizePolicy().hasHeightForWidth())
        self.plot3DWidgetPlaceholder.setSizePolicy(sizePolicy1)
        self.plot3DWidgetPlaceholder.setMinimumSize(QSize(0, 350))

        self.horizontalLayout_3.addWidget(self.plot3DWidgetPlaceholder)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.retranslateUi(FF_az)

        QMetaObject.connectSlotsByName(FF_az)
    # setupUi

    def retranslateUi(self, FF_az):
        FF_az.setWindowTitle(QCoreApplication.translate("FF_az", u"Form", None))
        self.start_posEntry.setText(QCoreApplication.translate("FF_az", u"0", None))
        self.stop_posLabel.setText(QCoreApplication.translate("FF_az", u"stop position", None))
        self.start_pos_Label.setText(QCoreApplication.translate("FF_az", u"start position", None))
        self.freqLabel.setText(QCoreApplication.translate("FF_az", u"frequency", None))
        self.current_posLabel.setText(QCoreApplication.translate("FF_az", u"current:", None))
        self.stepLabel.setText(QCoreApplication.translate("FF_az", u"step:", None))
    # retranslateUi

