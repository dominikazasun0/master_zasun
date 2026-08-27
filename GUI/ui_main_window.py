# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
    QHBoxLayout, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QTabWidget, QTextEdit, QToolBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1200, 600)
        MainWindow.setAutoFillBackground(True)
        MainWindow.setStyleSheet(u"")
        self.Start_Meas = QAction(MainWindow)
        self.Start_Meas.setObjectName(u"Start_Meas")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackStart))
        self.Start_Meas.setIcon(icon)
        self.Start_Meas.setMenuRole(QAction.MenuRole.NoRole)
        self.Pause_Meas = QAction(MainWindow)
        self.Pause_Meas.setObjectName(u"Pause_Meas")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackPause))
        self.Pause_Meas.setIcon(icon1)
        self.Pause_Meas.setMenuRole(QAction.MenuRole.NoRole)
        self.Abort_Meas = QAction(MainWindow)
        self.Abort_Meas.setObjectName(u"Abort_Meas")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackStop))
        self.Abort_Meas.setIcon(icon2)
        self.Abort_Meas.setMenuRole(QAction.MenuRole.NoRole)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setAutoFillBackground(False)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.main_tabs = QTabWidget(self.centralwidget)
        self.main_tabs.setObjectName(u"main_tabs")
        sizePolicy.setHeightForWidth(self.main_tabs.sizePolicy().hasHeightForWidth())
        self.main_tabs.setSizePolicy(sizePolicy)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout = QGridLayout(self.tab)
        self.gridLayout.setObjectName(u"gridLayout")
        self.main_tabs.addTab(self.tab, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.main_tabs.addTab(self.tab_3, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.main_tabs.addTab(self.tab_2, "")

        self.verticalLayout.addWidget(self.main_tabs)

        self.logger_box = QGroupBox(self.centralwidget)
        self.logger_box.setObjectName(u"logger_box")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.logger_box.sizePolicy().hasHeightForWidth())
        self.logger_box.setSizePolicy(sizePolicy1)
        self.logger_box.setMinimumSize(QSize(0, 200))
        self.verticalLayout_3 = QVBoxLayout(self.logger_box)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.log_text_box = QTextEdit(self.logger_box)
        self.log_text_box.setObjectName(u"log_text_box")
        self.log_text_box.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.log_text_box)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.log_all_box = QCheckBox(self.logger_box)
        self.log_all_box.setObjectName(u"log_all_box")
        self.log_all_box.setChecked(True)

        self.horizontalLayout.addWidget(self.log_all_box)

        self.log_debug_box = QCheckBox(self.logger_box)
        self.log_debug_box.setObjectName(u"log_debug_box")
        self.log_debug_box.setChecked(True)

        self.horizontalLayout.addWidget(self.log_debug_box)

        self.log_info_box = QCheckBox(self.logger_box)
        self.log_info_box.setObjectName(u"log_info_box")
        self.log_info_box.setChecked(True)

        self.horizontalLayout.addWidget(self.log_info_box)

        self.log_warning_box = QCheckBox(self.logger_box)
        self.log_warning_box.setObjectName(u"log_warning_box")
        self.log_warning_box.setChecked(True)

        self.horizontalLayout.addWidget(self.log_warning_box)

        self.log_error_box = QCheckBox(self.logger_box)
        self.log_error_box.setObjectName(u"log_error_box")
        self.log_error_box.setChecked(True)

        self.horizontalLayout.addWidget(self.log_error_box)

        self.log_critical_box = QCheckBox(self.logger_box)
        self.log_critical_box.setObjectName(u"log_critical_box")
        self.log_critical_box.setChecked(True)

        self.horizontalLayout.addWidget(self.log_critical_box)

        self.log_clear_btn = QPushButton(self.logger_box)
        self.log_clear_btn.setObjectName(u"log_clear_btn")

        self.horizontalLayout.addWidget(self.log_clear_btn)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)


        self.verticalLayout.addWidget(self.logger_box)

        self.verticalLayout.setStretch(0, 15)
        self.verticalLayout.setStretch(1, 5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.toolBar.addAction(self.Start_Meas)
        self.toolBar.addAction(self.Pause_Meas)
        self.toolBar.addAction(self.Abort_Meas)

        self.retranslateUi(MainWindow)

        self.main_tabs.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Antenna Measurement App", None))
        self.Start_Meas.setText(QCoreApplication.translate("MainWindow", u"Start Measurement", None))
        self.Pause_Meas.setText(QCoreApplication.translate("MainWindow", u"Pause Measurement", None))
        self.Abort_Meas.setText(QCoreApplication.translate("MainWindow", u"Abort Measurement", None))
        self.main_tabs.setTabText(self.main_tabs.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"tab", None))
        self.main_tabs.setTabText(self.main_tabs.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"VNA", None))
        self.main_tabs.setTabText(self.main_tabs.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Tab 2", None))
        self.logger_box.setTitle(QCoreApplication.translate("MainWindow", u"Logger", None))
        self.log_all_box.setText(QCoreApplication.translate("MainWindow", u"All", None))
        self.log_debug_box.setText(QCoreApplication.translate("MainWindow", u"Debug", None))
        self.log_info_box.setText(QCoreApplication.translate("MainWindow", u"Info", None))
        self.log_warning_box.setText(QCoreApplication.translate("MainWindow", u"Warning", None))
        self.log_error_box.setText(QCoreApplication.translate("MainWindow", u"Error", None))
        self.log_critical_box.setText(QCoreApplication.translate("MainWindow", u"Critical", None))
        self.log_clear_btn.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

