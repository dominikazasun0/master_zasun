# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'calib.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Calib(object):
    def setupUi(self, Calib):
        if not Calib.objectName():
            Calib.setObjectName(u"Calib")
        Calib.resize(1373, 658)
        self.layoutWidget = QWidget(Calib)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(950, 50, 281, 51))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(110, 16777215))

        self.horizontalLayout.addWidget(self.label)

        self.distance_label = QLabel(self.layoutWidget)
        self.distance_label.setObjectName(u"distance_label")

        self.horizontalLayout.addWidget(self.distance_label)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.pose_est_btn = QPushButton(Calib)
        self.pose_est_btn.setObjectName(u"pose_est_btn")
        self.pose_est_btn.setGeometry(QRect(950, 120, 111, 24))
        self.move_btn = QPushButton(Calib)
        self.move_btn.setObjectName(u"move_btn")
        self.move_btn.setGeometry(QRect(950, 370, 121, 24))
        self.video_label = QLabel(Calib)
        self.video_label.setObjectName(u"video_label")
        self.video_label.setGeometry(QRect(80, 30, 641, 441))
        self.layoutWidget1 = QWidget(Calib)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(950, 150, 328, 66))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.current_pose_label = QLabel(self.layoutWidget1)
        self.current_pose_label.setObjectName(u"current_pose_label")

        self.verticalLayout_2.addWidget(self.current_pose_label)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.layoutWidget1)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_3.addWidget(self.label_2)

        self.label_3 = QLabel(self.layoutWidget1)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_3.addWidget(self.label_3)

        self.label_4 = QLabel(self.layoutWidget1)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_3.addWidget(self.label_4)

        self.label_5 = QLabel(self.layoutWidget1)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_3.addWidget(self.label_5)

        self.label_6 = QLabel(self.layoutWidget1)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_3.addWidget(self.label_6)

        self.label_7 = QLabel(self.layoutWidget1)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_3.addWidget(self.label_7)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.old_x = QLabel(self.layoutWidget1)
        self.old_x.setObjectName(u"old_x")

        self.horizontalLayout_2.addWidget(self.old_x)

        self.old_y = QLabel(self.layoutWidget1)
        self.old_y.setObjectName(u"old_y")

        self.horizontalLayout_2.addWidget(self.old_y)

        self.old_z = QLabel(self.layoutWidget1)
        self.old_z.setObjectName(u"old_z")

        self.horizontalLayout_2.addWidget(self.old_z)

        self.old_roll = QLabel(self.layoutWidget1)
        self.old_roll.setObjectName(u"old_roll")

        self.horizontalLayout_2.addWidget(self.old_roll)

        self.old_pitch = QLabel(self.layoutWidget1)
        self.old_pitch.setObjectName(u"old_pitch")

        self.horizontalLayout_2.addWidget(self.old_pitch)

        self.old_yaw = QLabel(self.layoutWidget1)
        self.old_yaw.setObjectName(u"old_yaw")

        self.horizontalLayout_2.addWidget(self.old_yaw)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.layoutWidget2 = QWidget(Calib)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(950, 231, 397, 132))
        self.verticalLayout_10 = QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.current_pose_label_2 = QLabel(self.layoutWidget2)
        self.current_pose_label_2.setObjectName(u"current_pose_label_2")

        self.verticalLayout_10.addWidget(self.current_pose_label_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.label_8 = QLabel(self.layoutWidget2)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_9.addWidget(self.label_8)

        self.label_26 = QLabel(self.layoutWidget2)
        self.label_26.setObjectName(u"label_26")

        self.verticalLayout_9.addWidget(self.label_26)

        self.label_27 = QLabel(self.layoutWidget2)
        self.label_27.setObjectName(u"label_27")

        self.verticalLayout_9.addWidget(self.label_27)

        self.label_28 = QLabel(self.layoutWidget2)
        self.label_28.setObjectName(u"label_28")

        self.verticalLayout_9.addWidget(self.label_28)

        self.label_29 = QLabel(self.layoutWidget2)
        self.label_29.setObjectName(u"label_29")

        self.verticalLayout_9.addWidget(self.label_29)


        self.horizontalLayout_4.addLayout(self.verticalLayout_9)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_14 = QLabel(self.layoutWidget2)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMaximumSize(QSize(50, 16777215))

        self.verticalLayout_8.addWidget(self.label_14)

        self.center_x = QLabel(self.layoutWidget2)
        self.center_x.setObjectName(u"center_x")

        self.verticalLayout_8.addWidget(self.center_x)

        self.p0_x = QLabel(self.layoutWidget2)
        self.p0_x.setObjectName(u"p0_x")

        self.verticalLayout_8.addWidget(self.p0_x)

        self.px_x = QLabel(self.layoutWidget2)
        self.px_x.setObjectName(u"px_x")

        self.verticalLayout_8.addWidget(self.px_x)

        self.pxy_x = QLabel(self.layoutWidget2)
        self.pxy_x.setObjectName(u"pxy_x")

        self.verticalLayout_8.addWidget(self.pxy_x)


        self.horizontalLayout_4.addLayout(self.verticalLayout_8)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_15 = QLabel(self.layoutWidget2)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMaximumSize(QSize(50, 16777215))

        self.verticalLayout_7.addWidget(self.label_15)

        self.center_y = QLabel(self.layoutWidget2)
        self.center_y.setObjectName(u"center_y")

        self.verticalLayout_7.addWidget(self.center_y)

        self.p0_y = QLabel(self.layoutWidget2)
        self.p0_y.setObjectName(u"p0_y")

        self.verticalLayout_7.addWidget(self.p0_y)

        self.px_y = QLabel(self.layoutWidget2)
        self.px_y.setObjectName(u"px_y")

        self.verticalLayout_7.addWidget(self.px_y)

        self.pxy_y = QLabel(self.layoutWidget2)
        self.pxy_y.setObjectName(u"pxy_y")

        self.verticalLayout_7.addWidget(self.pxy_y)


        self.horizontalLayout_4.addLayout(self.verticalLayout_7)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_16 = QLabel(self.layoutWidget2)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMaximumSize(QSize(50, 16777215))

        self.verticalLayout_6.addWidget(self.label_16)

        self.center_z = QLabel(self.layoutWidget2)
        self.center_z.setObjectName(u"center_z")

        self.verticalLayout_6.addWidget(self.center_z)

        self.p0_z = QLabel(self.layoutWidget2)
        self.p0_z.setObjectName(u"p0_z")

        self.verticalLayout_6.addWidget(self.p0_z)

        self.px_z = QLabel(self.layoutWidget2)
        self.px_z.setObjectName(u"px_z")

        self.verticalLayout_6.addWidget(self.px_z)

        self.pxy_z = QLabel(self.layoutWidget2)
        self.pxy_z.setObjectName(u"pxy_z")

        self.verticalLayout_6.addWidget(self.pxy_z)


        self.horizontalLayout_4.addLayout(self.verticalLayout_6)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_17 = QLabel(self.layoutWidget2)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMaximumSize(QSize(50, 16777215))

        self.verticalLayout_5.addWidget(self.label_17)

        self.center_roll = QLabel(self.layoutWidget2)
        self.center_roll.setObjectName(u"center_roll")

        self.verticalLayout_5.addWidget(self.center_roll)

        self.p0_roll = QLabel(self.layoutWidget2)
        self.p0_roll.setObjectName(u"p0_roll")

        self.verticalLayout_5.addWidget(self.p0_roll)

        self.px_roll = QLabel(self.layoutWidget2)
        self.px_roll.setObjectName(u"px_roll")

        self.verticalLayout_5.addWidget(self.px_roll)

        self.pxy_roll = QLabel(self.layoutWidget2)
        self.pxy_roll.setObjectName(u"pxy_roll")

        self.verticalLayout_5.addWidget(self.pxy_roll)


        self.horizontalLayout_4.addLayout(self.verticalLayout_5)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_18 = QLabel(self.layoutWidget2)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMaximumSize(QSize(50, 16777215))

        self.verticalLayout_4.addWidget(self.label_18)

        self.center_pitch = QLabel(self.layoutWidget2)
        self.center_pitch.setObjectName(u"center_pitch")

        self.verticalLayout_4.addWidget(self.center_pitch)

        self.p0_pitch = QLabel(self.layoutWidget2)
        self.p0_pitch.setObjectName(u"p0_pitch")

        self.verticalLayout_4.addWidget(self.p0_pitch)

        self.px_pitch = QLabel(self.layoutWidget2)
        self.px_pitch.setObjectName(u"px_pitch")

        self.verticalLayout_4.addWidget(self.px_pitch)

        self.pxy_pitch = QLabel(self.layoutWidget2)
        self.pxy_pitch.setObjectName(u"pxy_pitch")

        self.verticalLayout_4.addWidget(self.pxy_pitch)


        self.horizontalLayout_4.addLayout(self.verticalLayout_4)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_19 = QLabel(self.layoutWidget2)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMaximumSize(QSize(50, 16777215))

        self.verticalLayout_3.addWidget(self.label_19)

        self.center_yaw = QLabel(self.layoutWidget2)
        self.center_yaw.setObjectName(u"center_yaw")

        self.verticalLayout_3.addWidget(self.center_yaw)

        self.p0_yaw = QLabel(self.layoutWidget2)
        self.p0_yaw.setObjectName(u"p0_yaw")

        self.verticalLayout_3.addWidget(self.p0_yaw)

        self.px_yaw = QLabel(self.layoutWidget2)
        self.px_yaw.setObjectName(u"px_yaw")

        self.verticalLayout_3.addWidget(self.px_yaw)

        self.pxy_yaw = QLabel(self.layoutWidget2)
        self.pxy_yaw.setObjectName(u"pxy_yaw")

        self.verticalLayout_3.addWidget(self.pxy_yaw)


        self.horizontalLayout_4.addLayout(self.verticalLayout_3)


        self.verticalLayout_10.addLayout(self.horizontalLayout_4)

        self.new_coordinate_btn = QPushButton(Calib)
        self.new_coordinate_btn.setObjectName(u"new_coordinate_btn")
        self.new_coordinate_btn.setGeometry(QRect(940, 490, 191, 24))
        self.layoutWidget_2 = QWidget(Calib)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.layoutWidget_2.setGeometry(QRect(940, 410, 328, 66))
        self.verticalLayout_11 = QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.current_pose_label_3 = QLabel(self.layoutWidget_2)
        self.current_pose_label_3.setObjectName(u"current_pose_label_3")

        self.verticalLayout_11.addWidget(self.current_pose_label_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_9 = QLabel(self.layoutWidget_2)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_5.addWidget(self.label_9)

        self.label_10 = QLabel(self.layoutWidget_2)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_5.addWidget(self.label_10)

        self.label_11 = QLabel(self.layoutWidget_2)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_5.addWidget(self.label_11)

        self.label_12 = QLabel(self.layoutWidget_2)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_5.addWidget(self.label_12)

        self.label_13 = QLabel(self.layoutWidget_2)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_5.addWidget(self.label_13)

        self.label_20 = QLabel(self.layoutWidget_2)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_5.addWidget(self.label_20)


        self.verticalLayout_11.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.new_cs_x = QLabel(self.layoutWidget_2)
        self.new_cs_x.setObjectName(u"new_cs_x")

        self.horizontalLayout_6.addWidget(self.new_cs_x)

        self.new_cs_y = QLabel(self.layoutWidget_2)
        self.new_cs_y.setObjectName(u"new_cs_y")

        self.horizontalLayout_6.addWidget(self.new_cs_y)

        self.new_cs_z = QLabel(self.layoutWidget_2)
        self.new_cs_z.setObjectName(u"new_cs_z")

        self.horizontalLayout_6.addWidget(self.new_cs_z)

        self.new_cs_roll = QLabel(self.layoutWidget_2)
        self.new_cs_roll.setObjectName(u"new_cs_roll")

        self.horizontalLayout_6.addWidget(self.new_cs_roll)

        self.new_cs_pitch = QLabel(self.layoutWidget_2)
        self.new_cs_pitch.setObjectName(u"new_cs_pitch")

        self.horizontalLayout_6.addWidget(self.new_cs_pitch)

        self.new_cs_yaw = QLabel(self.layoutWidget_2)
        self.new_cs_yaw.setObjectName(u"new_cs_yaw")

        self.horizontalLayout_6.addWidget(self.new_cs_yaw)


        self.verticalLayout_11.addLayout(self.horizontalLayout_6)

        self.start_verify_btn = QPushButton(Calib)
        self.start_verify_btn.setObjectName(u"start_verify_btn")
        self.start_verify_btn.setGeometry(QRect(950, 540, 121, 24))
        self.antenna_btn = QPushButton(Calib)
        self.antenna_btn.setObjectName(u"antenna_btn")
        self.antenna_btn.setGeometry(QRect(1150, 490, 141, 24))

        self.retranslateUi(Calib)

        QMetaObject.connectSlotsByName(Calib)
    # setupUi

    def retranslateUi(self, Calib):
        Calib.setWindowTitle(QCoreApplication.translate("Calib", u"Form", None))
        self.label.setText(QCoreApplication.translate("Calib", u"Distance to AB [mm]", None))
        self.distance_label.setText(QCoreApplication.translate("Calib", u"TextLabel", None))
        self.pose_est_btn.setText(QCoreApplication.translate("Calib", u"Calculate pose", None))
        self.move_btn.setText(QCoreApplication.translate("Calib", u"Move to new poses", None))
        self.video_label.setText(QCoreApplication.translate("Calib", u"TextLabel", None))
        self.current_pose_label.setText(QCoreApplication.translate("Calib", u"Current RARM pose", None))
        self.label_2.setText(QCoreApplication.translate("Calib", u"X", None))
        self.label_3.setText(QCoreApplication.translate("Calib", u"Y", None))
        self.label_4.setText(QCoreApplication.translate("Calib", u"Z", None))
        self.label_5.setText(QCoreApplication.translate("Calib", u"Roll", None))
        self.label_6.setText(QCoreApplication.translate("Calib", u"Pitch", None))
        self.label_7.setText(QCoreApplication.translate("Calib", u"Yaw", None))
        self.old_x.setText("")
        self.old_y.setText("")
        self.old_z.setText("")
        self.old_roll.setText("")
        self.old_pitch.setText("")
        self.old_yaw.setText("")
        self.current_pose_label_2.setText(QCoreApplication.translate("Calib", u"New RARM pose", None))
        self.label_8.setText("")
        self.label_26.setText(QCoreApplication.translate("Calib", u"Center", None))
        self.label_27.setText(QCoreApplication.translate("Calib", u"0", None))
        self.label_28.setText(QCoreApplication.translate("Calib", u"x", None))
        self.label_29.setText(QCoreApplication.translate("Calib", u"xy", None))
        self.label_14.setText(QCoreApplication.translate("Calib", u"X", None))
        self.center_x.setText("")
        self.p0_x.setText("")
        self.px_x.setText("")
        self.pxy_x.setText("")
        self.label_15.setText(QCoreApplication.translate("Calib", u"Y", None))
        self.center_y.setText("")
        self.p0_y.setText("")
        self.px_y.setText("")
        self.pxy_y.setText("")
        self.label_16.setText(QCoreApplication.translate("Calib", u"Z", None))
        self.center_z.setText("")
        self.p0_z.setText("")
        self.px_z.setText("")
        self.pxy_z.setText("")
        self.label_17.setText(QCoreApplication.translate("Calib", u"Roll", None))
        self.center_roll.setText("")
        self.p0_roll.setText("")
        self.px_roll.setText("")
        self.pxy_roll.setText("")
        self.label_18.setText(QCoreApplication.translate("Calib", u"Pitch", None))
        self.center_pitch.setText("")
        self.p0_pitch.setText("")
        self.px_pitch.setText("")
        self.pxy_pitch.setText("")
        self.label_19.setText(QCoreApplication.translate("Calib", u"Yaw", None))
        self.center_yaw.setText("")
        self.p0_yaw.setText("")
        self.px_yaw.setText("")
        self.pxy_yaw.setText("")
        self.new_coordinate_btn.setText(QCoreApplication.translate("Calib", u"Accept new coordinate system ", None))
        self.current_pose_label_3.setText(QCoreApplication.translate("Calib", u"New coordinate sysytem", None))
        self.label_9.setText(QCoreApplication.translate("Calib", u"X", None))
        self.label_10.setText(QCoreApplication.translate("Calib", u"Y", None))
        self.label_11.setText(QCoreApplication.translate("Calib", u"Z", None))
        self.label_12.setText(QCoreApplication.translate("Calib", u"Roll", None))
        self.label_13.setText(QCoreApplication.translate("Calib", u"Pitch", None))
        self.label_20.setText(QCoreApplication.translate("Calib", u"Yaw", None))
        self.new_cs_x.setText("")
        self.new_cs_y.setText("")
        self.new_cs_z.setText("")
        self.new_cs_roll.setText("")
        self.new_cs_pitch.setText("")
        self.new_cs_yaw.setText("")
        self.start_verify_btn.setText(QCoreApplication.translate("Calib", u"Start verification", None))
        self.antenna_btn.setText(QCoreApplication.translate("Calib", u"Change tcp to probe", None))
    # retranslateUi

