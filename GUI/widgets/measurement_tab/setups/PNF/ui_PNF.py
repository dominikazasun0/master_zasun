# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PNF.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QProgressBar,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_PNF(object):
    def setupUi(self, PNF):
        if not PNF.objectName():
            PNF.setObjectName(u"PNF")
        PNF.resize(1147, 480)
        self.verticalLayout_2 = QVBoxLayout(PNF)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.current_posLabel = QLabel(PNF)
        self.current_posLabel.setObjectName(u"current_posLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.current_posLabel.sizePolicy().hasHeightForWidth())
        self.current_posLabel.setSizePolicy(sizePolicy)
        self.current_posLabel.setMinimumSize(QSize(150, 0))

        self.horizontalLayout.addWidget(self.current_posLabel)

        self.stepLabel = QLabel(PNF)
        self.stepLabel.setObjectName(u"stepLabel")
        sizePolicy.setHeightForWidth(self.stepLabel.sizePolicy().hasHeightForWidth())
        self.stepLabel.setSizePolicy(sizePolicy)
        self.stepLabel.setMinimumSize(QSize(150, 0))

        self.horizontalLayout.addWidget(self.stepLabel)

        self.calibration_lbl = QLabel(PNF)
        self.calibration_lbl.setObjectName(u"calibration_lbl")
        self.calibration_lbl.setMinimumSize(QSize(150, 0))

        self.horizontalLayout.addWidget(self.calibration_lbl)

        self.freqLabel = QLabel(PNF)
        self.freqLabel.setObjectName(u"freqLabel")

        self.horizontalLayout.addWidget(self.freqLabel)

        self.freq_comboBox = QComboBox(PNF)
        self.freq_comboBox.setObjectName(u"freq_comboBox")
        sizePolicy.setHeightForWidth(self.freq_comboBox.sizePolicy().hasHeightForWidth())
        self.freq_comboBox.setSizePolicy(sizePolicy)
        self.freq_comboBox.setMinimumSize(QSize(150, 0))

        self.horizontalLayout.addWidget(self.freq_comboBox)

        self.cross_pol_check = QCheckBox(PNF)
        self.cross_pol_check.setObjectName(u"cross_pol_check")
        self.cross_pol_check.setChecked(True)

        self.horizontalLayout.addWidget(self.cross_pol_check)

        self.line = QFrame(PNF)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.label_5 = QLabel(PNF)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout.addWidget(self.label_5)

        self.meas_progress = QProgressBar(PNF)
        self.meas_progress.setObjectName(u"meas_progress")
        self.meas_progress.setValue(24)

        self.horizontalLayout.addWidget(self.meas_progress)

        self.elapsed_time_lbl = QLabel(PNF)
        self.elapsed_time_lbl.setObjectName(u"elapsed_time_lbl")

        self.horizontalLayout.addWidget(self.elapsed_time_lbl)

        self.remaining_time_lbl = QLabel(PNF)
        self.remaining_time_lbl.setObjectName(u"remaining_time_lbl")

        self.horizontalLayout.addWidget(self.remaining_time_lbl)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_6)

        self.line_2 = QFrame(PNF)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout.addWidget(self.line_2)

        self.export_format_combo = QComboBox(PNF)
        self.export_format_combo.setObjectName(u"export_format_combo")

        self.horizontalLayout.addWidget(self.export_format_combo)

        self.export_btn = QPushButton(PNF)
        self.export_btn.setObjectName(u"export_btn")

        self.horizontalLayout.addWidget(self.export_btn)

        self.screenshot_btn = QPushButton(PNF)
        self.screenshot_btn.setObjectName(u"screenshot_btn")

        self.horizontalLayout.addWidget(self.screenshot_btn)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame_2 = QFrame(PNF)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_2.setLineWidth(5)
        self.verticalLayout_4 = QVBoxLayout(self.frame_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.Phase_2D_plot = QVBoxLayout()
        self.Phase_2D_plot.setObjectName(u"Phase_2D_plot")

        self.verticalLayout_4.addLayout(self.Phase_2D_plot)


        self.gridLayout.addWidget(self.frame_2, 1, 1, 1, 1)

        self.frame = QFrame(PNF)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.frame.setLineWidth(5)
        self.verticalLayout_3 = QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.Mag_2D_plot = QVBoxLayout()
        self.Mag_2D_plot.setObjectName(u"Mag_2D_plot")

        self.verticalLayout_3.addLayout(self.Mag_2D_plot)


        self.gridLayout.addWidget(self.frame, 1, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_3 = QLabel(PNF)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_4.addWidget(self.label_3)

        self.spinbox_lvl_mag_max = QSpinBox(PNF)
        self.spinbox_lvl_mag_max.setObjectName(u"spinbox_lvl_mag_max")
        self.spinbox_lvl_mag_max.setMinimum(-150)
        self.spinbox_lvl_mag_max.setMaximum(50)

        self.horizontalLayout_4.addWidget(self.spinbox_lvl_mag_max)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_4 = QLabel(PNF)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_5.addWidget(self.label_4)

        self.spinbox_lvl_mag_min = QSpinBox(PNF)
        self.spinbox_lvl_mag_min.setObjectName(u"spinbox_lvl_mag_min")
        self.spinbox_lvl_mag_min.setMinimum(-150)
        self.spinbox_lvl_mag_min.setMaximum(50)

        self.horizontalLayout_5.addWidget(self.spinbox_lvl_mag_min)


        self.verticalLayout.addLayout(self.horizontalLayout_5)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.label = QLabel(PNF)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(20)
        self.label.setFont(font)

        self.horizontalLayout_2.addWidget(self.label)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_5)


        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.spinBox_4 = QSpinBox(PNF)
        self.spinBox_4.setObjectName(u"spinBox_4")

        self.verticalLayout_5.addWidget(self.spinBox_4)

        self.spinBox_3 = QSpinBox(PNF)
        self.spinBox_3.setObjectName(u"spinBox_3")

        self.verticalLayout_5.addWidget(self.spinBox_3)


        self.horizontalLayout_3.addLayout(self.verticalLayout_5)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.label_2 = QLabel(PNF)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.horizontalLayout_3.addWidget(self.label_2)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 1, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)


        self.retranslateUi(PNF)

        QMetaObject.connectSlotsByName(PNF)
    # setupUi

    def retranslateUi(self, PNF):
        PNF.setWindowTitle(QCoreApplication.translate("PNF", u"Form", None))
        self.current_posLabel.setText(QCoreApplication.translate("PNF", u"Current:", None))
        self.stepLabel.setText(QCoreApplication.translate("PNF", u"Dims:", None))
        self.calibration_lbl.setText(QCoreApplication.translate("PNF", u"Calibration:", None))
        self.freqLabel.setText(QCoreApplication.translate("PNF", u"Frequency:", None))
        self.cross_pol_check.setText(QCoreApplication.translate("PNF", u"Add cross-polarization", None))
        self.label_5.setText(QCoreApplication.translate("PNF", u"Progress:", None))
        self.elapsed_time_lbl.setText("")
        self.remaining_time_lbl.setText("")
        self.export_btn.setText(QCoreApplication.translate("PNF", u"Export", None))
        self.screenshot_btn.setText(QCoreApplication.translate("PNF", u"Save Images", None))
        self.label_3.setText(QCoreApplication.translate("PNF", u"Max:", None))
        self.label_4.setText(QCoreApplication.translate("PNF", u"Min:", None))
        self.label.setText(QCoreApplication.translate("PNF", u"Magnitude [dB]", None))
        self.label_2.setText(QCoreApplication.translate("PNF", u"Phase [rad]", None))
    # retranslateUi

