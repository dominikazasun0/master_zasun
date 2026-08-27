# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'robot_control.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QSpinBox, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_robot_control(object):
    def setupUi(self, robot_control):
        if not robot_control.objectName():
            robot_control.setObjectName(u"robot_control")
        robot_control.resize(1195, 913)
        self.verticalLayout = QVBoxLayout(robot_control)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.settings_group_box = QGroupBox(robot_control)
        self.settings_group_box.setObjectName(u"settings_group_box")
        self.layoutWidget = QWidget(self.settings_group_box)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(70, 30, 343, 24))
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.freq = QLineEdit(self.layoutWidget)
        self.freq.setObjectName(u"freq")

        self.horizontalLayout_2.addWidget(self.freq)

        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.lamda = QLineEdit(self.layoutWidget)
        self.lamda.setObjectName(u"lamda")

        self.horizontalLayout_2.addWidget(self.lamda)

        self.layoutWidget1 = QWidget(self.settings_group_box)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(70, 80, 314, 26))
        self.horizontalLayout_3 = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.layoutWidget1)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.delta_x = QLineEdit(self.layoutWidget1)
        self.delta_x.setObjectName(u"delta_x")

        self.horizontalLayout_3.addWidget(self.delta_x)

        self.calc_x_btn = QRadioButton(self.layoutWidget1)
        self.calc_x_btn.setObjectName(u"calc_x_btn")

        self.horizontalLayout_3.addWidget(self.calc_x_btn)

        self.calc_x_combo = QComboBox(self.layoutWidget1)
        self.calc_x_combo.setObjectName(u"calc_x_combo")

        self.horizontalLayout_3.addWidget(self.calc_x_combo)

        self.layoutWidget2 = QWidget(self.settings_group_box)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(70, 110, 314, 26))
        self.horizontalLayout_4 = QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.layoutWidget2)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.delta_y = QLineEdit(self.layoutWidget2)
        self.delta_y.setObjectName(u"delta_y")

        self.horizontalLayout_4.addWidget(self.delta_y)

        self.calc_y_btn = QRadioButton(self.layoutWidget2)
        self.calc_y_btn.setObjectName(u"calc_y_btn")

        self.horizontalLayout_4.addWidget(self.calc_y_btn)

        self.calc_y_combo = QComboBox(self.layoutWidget2)
        self.calc_y_combo.setObjectName(u"calc_y_combo")

        self.horizontalLayout_4.addWidget(self.calc_y_combo)

        self.layoutWidget3 = QWidget(self.settings_group_box)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(70, 140, 244, 25))
        self.horizontalLayout_5 = QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.layoutWidget3)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_5.addWidget(self.label_5)

        self.N_x = QSpinBox(self.layoutWidget3)
        self.N_x.setObjectName(u"N_x")
        self.N_x.setMaximum(999)

        self.horizontalLayout_5.addWidget(self.N_x)

        self.label_6 = QLabel(self.layoutWidget3)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_5.addWidget(self.label_6)

        self.N_y = QSpinBox(self.layoutWidget3)
        self.N_y.setObjectName(u"N_y")
        self.N_y.setMaximum(999)

        self.horizontalLayout_5.addWidget(self.N_y)

        self.layoutWidget4 = QWidget(self.settings_group_box)
        self.layoutWidget4.setObjectName(u"layoutWidget4")
        self.layoutWidget4.setGeometry(QRect(70, 210, 221, 18))
        self.horizontalLayout_6 = QHBoxLayout(self.layoutWidget4)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label_7 = QLabel(self.layoutWidget4)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_6.addWidget(self.label_7)

        self.x_dims = QLabel(self.layoutWidget4)
        self.x_dims.setObjectName(u"x_dims")

        self.horizontalLayout_6.addWidget(self.x_dims)

        self.layoutWidget5 = QWidget(self.settings_group_box)
        self.layoutWidget5.setObjectName(u"layoutWidget5")
        self.layoutWidget5.setGeometry(QRect(70, 240, 221, 18))
        self.horizontalLayout_7 = QHBoxLayout(self.layoutWidget5)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label_8 = QLabel(self.layoutWidget5)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_7.addWidget(self.label_8)

        self.y_dims = QLabel(self.layoutWidget5)
        self.y_dims.setObjectName(u"y_dims")

        self.horizontalLayout_7.addWidget(self.y_dims)

        self.dims_calc_btn = QPushButton(self.settings_group_box)
        self.dims_calc_btn.setObjectName(u"dims_calc_btn")
        self.dims_calc_btn.setGeometry(QRect(70, 270, 101, 24))
        self.coordinates_table = QTableWidget(self.settings_group_box)
        self.coordinates_table.setObjectName(u"coordinates_table")
        self.coordinates_table.setGeometry(QRect(560, 30, 661, 281))
        self.show_matrix_btn = QPushButton(self.settings_group_box)
        self.show_matrix_btn.setObjectName(u"show_matrix_btn")
        self.show_matrix_btn.setGeometry(QRect(70, 300, 101, 24))
        self.horizontalLayoutWidget_2 = QWidget(self.settings_group_box)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(70, 170, 160, 31))
        self.horizontalLayout_11 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.label_19 = QLabel(self.horizontalLayoutWidget_2)
        self.label_19.setObjectName(u"label_19")

        self.horizontalLayout_11.addWidget(self.label_19)

        self.ant_dist = QLineEdit(self.horizontalLayoutWidget_2)
        self.ant_dist.setObjectName(u"ant_dist")

        self.horizontalLayout_11.addWidget(self.ant_dist)


        self.verticalLayout.addWidget(self.settings_group_box)

        self.robot_control_box = QGroupBox(robot_control)
        self.robot_control_box.setObjectName(u"robot_control_box")
        self.layoutWidget6 = QWidget(self.robot_control_box)
        self.layoutWidget6.setObjectName(u"layoutWidget6")
        self.layoutWidget6.setGeometry(QRect(10, 26, 181, 26))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.reqCtrl = QPushButton(self.layoutWidget6)
        self.reqCtrl.setObjectName(u"reqCtrl")

        self.horizontalLayout.addWidget(self.reqCtrl)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.load_matrix_btn = QPushButton(self.layoutWidget6)
        self.load_matrix_btn.setObjectName(u"load_matrix_btn")

        self.horizontalLayout.addWidget(self.load_matrix_btn)

        self.home_btn = QPushButton(self.robot_control_box)
        self.home_btn.setObjectName(u"home_btn")
        self.home_btn.setGeometry(QRect(10, 100, 101, 71))
        self.run_btn = QPushButton(self.robot_control_box)
        self.run_btn.setObjectName(u"run_btn")
        self.run_btn.setGeometry(QRect(10, 230, 101, 71))
        self.resume_btn = QPushButton(self.robot_control_box)
        self.resume_btn.setObjectName(u"resume_btn")
        self.resume_btn.setGeometry(QRect(120, 230, 101, 71))
        self.layoutWidget7 = QWidget(self.robot_control_box)
        self.layoutWidget7.setObjectName(u"layoutWidget7")
        self.layoutWidget7.setGeometry(QRect(10, 60, 231, 26))
        self.horizontalLayout_8 = QHBoxLayout(self.layoutWidget7)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.label_9 = QLabel(self.layoutWidget7)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_8.addWidget(self.label_9)

        self.robot_state = QLabel(self.layoutWidget7)
        self.robot_state.setObjectName(u"robot_state")

        self.horizontalLayout_8.addWidget(self.robot_state)

        self.get_state_btn = QPushButton(self.layoutWidget7)
        self.get_state_btn.setObjectName(u"get_state_btn")

        self.horizontalLayout_8.addWidget(self.get_state_btn)

        self.layoutWidget8 = QWidget(self.robot_control_box)
        self.layoutWidget8.setObjectName(u"layoutWidget8")
        self.layoutWidget8.setGeometry(QRect(11, 179, 651, 26))
        self.horizontalLayout_9 = QHBoxLayout(self.layoutWidget8)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.label_10 = QLabel(self.layoutWidget8)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_9.addWidget(self.label_10)

        self.x_start = QLineEdit(self.layoutWidget8)
        self.x_start.setObjectName(u"x_start")

        self.horizontalLayout_9.addWidget(self.x_start)

        self.label_11 = QLabel(self.layoutWidget8)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_9.addWidget(self.label_11)

        self.y_start = QLineEdit(self.layoutWidget8)
        self.y_start.setObjectName(u"y_start")

        self.horizontalLayout_9.addWidget(self.y_start)

        self.label_12 = QLabel(self.layoutWidget8)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_9.addWidget(self.label_12)

        self.z_start = QLineEdit(self.layoutWidget8)
        self.z_start.setObjectName(u"z_start")

        self.horizontalLayout_9.addWidget(self.z_start)

        self.label_15 = QLabel(self.layoutWidget8)
        self.label_15.setObjectName(u"label_15")

        self.horizontalLayout_9.addWidget(self.label_15)

        self.roll_start = QLineEdit(self.layoutWidget8)
        self.roll_start.setObjectName(u"roll_start")

        self.horizontalLayout_9.addWidget(self.roll_start)

        self.label_14 = QLabel(self.layoutWidget8)
        self.label_14.setObjectName(u"label_14")

        self.horizontalLayout_9.addWidget(self.label_14)

        self.pitch_start = QLineEdit(self.layoutWidget8)
        self.pitch_start.setObjectName(u"pitch_start")

        self.horizontalLayout_9.addWidget(self.pitch_start)

        self.label_16 = QLabel(self.layoutWidget8)
        self.label_16.setObjectName(u"label_16")

        self.horizontalLayout_9.addWidget(self.label_16)

        self.yaw_start = QLineEdit(self.layoutWidget8)
        self.yaw_start.setObjectName(u"yaw_start")

        self.horizontalLayout_9.addWidget(self.yaw_start)

        self.label_13 = QLabel(self.layoutWidget8)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_9.addWidget(self.label_13)

        self.move_to_start_btn = QPushButton(self.layoutWidget8)
        self.move_to_start_btn.setObjectName(u"move_to_start_btn")

        self.horizontalLayout_9.addWidget(self.move_to_start_btn)

        self.label_17 = QLabel(self.layoutWidget8)
        self.label_17.setObjectName(u"label_17")

        self.horizontalLayout_9.addWidget(self.label_17)

        self.gridLayoutWidget = QWidget(self.robot_control_box)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(240, 220, 239, 86))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.mov_up_btn = QPushButton(self.gridLayoutWidget)
        self.mov_up_btn.setObjectName(u"mov_up_btn")

        self.gridLayout.addWidget(self.mov_up_btn, 0, 1, 1, 1)

        self.mov_down_btn = QPushButton(self.gridLayoutWidget)
        self.mov_down_btn.setObjectName(u"mov_down_btn")

        self.gridLayout.addWidget(self.mov_down_btn, 2, 1, 1, 1)

        self.mov_left_btn = QPushButton(self.gridLayoutWidget)
        self.mov_left_btn.setObjectName(u"mov_left_btn")

        self.gridLayout.addWidget(self.mov_left_btn, 1, 0, 1, 1)

        self.mov_right_btn = QPushButton(self.gridLayoutWidget)
        self.mov_right_btn.setObjectName(u"mov_right_btn")

        self.gridLayout.addWidget(self.mov_right_btn, 1, 2, 1, 1)

        self.mov_to_0 = QPushButton(self.gridLayoutWidget)
        self.mov_to_0.setObjectName(u"mov_to_0")

        self.gridLayout.addWidget(self.mov_to_0, 1, 1, 1, 1)

        self.horizontalLayoutWidget = QWidget(self.robot_control_box)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(150, 90, 211, 80))
        self.horizontalLayout_10 = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.label_18 = QLabel(self.horizontalLayoutWidget)
        self.label_18.setObjectName(u"label_18")

        self.horizontalLayout_10.addWidget(self.label_18)

        self.copolar_rotation_spin = QSpinBox(self.horizontalLayoutWidget)
        self.copolar_rotation_spin.setObjectName(u"copolar_rotation_spin")
        self.copolar_rotation_spin.setMaximum(90)

        self.horizontalLayout_10.addWidget(self.copolar_rotation_spin)

        self.reset_btn = QPushButton(self.robot_control_box)
        self.reset_btn.setObjectName(u"reset_btn")
        self.reset_btn.setGeometry(QRect(200, 30, 121, 24))

        self.verticalLayout.addWidget(self.robot_control_box)


        self.retranslateUi(robot_control)

        QMetaObject.connectSlotsByName(robot_control)
    # setupUi

    def retranslateUi(self, robot_control):
        robot_control.setWindowTitle(QCoreApplication.translate("robot_control", u"Form", None))
        self.settings_group_box.setTitle(QCoreApplication.translate("robot_control", u"Settings", None))
        self.label.setText(QCoreApplication.translate("robot_control", u"f [Hz]:", None))
        self.label_2.setText(QCoreApplication.translate("robot_control", u"\u03bb [cm]:", None))
        self.label_3.setText(QCoreApplication.translate("robot_control", u"\u2206x [cm]", None))
        self.calc_x_btn.setText(QCoreApplication.translate("robot_control", u"Calc", None))
        self.label_4.setText(QCoreApplication.translate("robot_control", u"\u2206y [cm]", None))
        self.calc_y_btn.setText(QCoreApplication.translate("robot_control", u"Calc", None))
        self.label_5.setText(QCoreApplication.translate("robot_control", u"x-points", None))
        self.label_6.setText(QCoreApplication.translate("robot_control", u"y-points", None))
        self.label_7.setText(QCoreApplication.translate("robot_control", u"x dim:", None))
        self.x_dims.setText("")
        self.label_8.setText(QCoreApplication.translate("robot_control", u"y dim:", None))
        self.y_dims.setText("")
        self.dims_calc_btn.setText(QCoreApplication.translate("robot_control", u"Calc Dimensions", None))
        self.show_matrix_btn.setText(QCoreApplication.translate("robot_control", u"Show Matrix", None))
        self.label_19.setText(QCoreApplication.translate("robot_control", u"Distance [cm]", None))
        self.ant_dist.setText(QCoreApplication.translate("robot_control", u"5", None))
        self.robot_control_box.setTitle(QCoreApplication.translate("robot_control", u"Robot Control", None))
        self.reqCtrl.setText(QCoreApplication.translate("robot_control", u"Get Control", None))
        self.load_matrix_btn.setText(QCoreApplication.translate("robot_control", u"Load Matrix", None))
        self.home_btn.setText(QCoreApplication.translate("robot_control", u"HOME", None))
        self.run_btn.setText(QCoreApplication.translate("robot_control", u"START", None))
        self.resume_btn.setText(QCoreApplication.translate("robot_control", u"RESUME", None))
        self.label_9.setText(QCoreApplication.translate("robot_control", u"State:", None))
        self.robot_state.setText("")
        self.get_state_btn.setText(QCoreApplication.translate("robot_control", u"Get state", None))
        self.label_10.setText(QCoreApplication.translate("robot_control", u"START: [", None))
        self.label_11.setText(QCoreApplication.translate("robot_control", u",", None))
        self.label_12.setText(QCoreApplication.translate("robot_control", u",", None))
        self.label_15.setText(QCoreApplication.translate("robot_control", u",", None))
        self.label_14.setText(QCoreApplication.translate("robot_control", u",", None))
        self.label_16.setText(QCoreApplication.translate("robot_control", u",", None))
        self.label_13.setText(QCoreApplication.translate("robot_control", u"]", None))
        self.move_to_start_btn.setText(QCoreApplication.translate("robot_control", u"GO!", None))
        self.label_17.setText(QCoreApplication.translate("robot_control", u"[x,y,z,r,p,y]", None))
        self.mov_up_btn.setText(QCoreApplication.translate("robot_control", u"^", None))
        self.mov_down_btn.setText(QCoreApplication.translate("robot_control", u"v", None))
        self.mov_left_btn.setText(QCoreApplication.translate("robot_control", u"<", None))
        self.mov_right_btn.setText(QCoreApplication.translate("robot_control", u">", None))
        self.mov_to_0.setText(QCoreApplication.translate("robot_control", u"0", None))
        self.label_18.setText(QCoreApplication.translate("robot_control", u"Copolar axis rotation [deg]", None))
        self.reset_btn.setText(QCoreApplication.translate("robot_control", u"Reset robot settings", None))
    # retranslateUi

