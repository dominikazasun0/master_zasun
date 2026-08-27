# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'data_processing.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QTabWidget, QTreeView, QVBoxLayout, QWidget)

class Ui_data_processing(object):
    def setupUi(self, data_processing):
        if not data_processing.objectName():
            data_processing.setObjectName(u"data_processing")
        data_processing.resize(1112, 652)
        self.horizontalLayout_2 = QHBoxLayout(data_processing)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.dir_tree_view = QTreeView(data_processing)
        self.dir_tree_view.setObjectName(u"dir_tree_view")

        self.gridLayout_7.addWidget(self.dir_tree_view, 1, 0, 1, 2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_2, 0, 1, 1, 1)

        self.tree_view_refresh_btn = QPushButton(data_processing)
        self.tree_view_refresh_btn.setObjectName(u"tree_view_refresh_btn")

        self.gridLayout_7.addWidget(self.tree_view_refresh_btn, 0, 0, 1, 1)


        self.horizontalLayout_2.addLayout(self.gridLayout_7)

        self.post_processing_tabs = QTabWidget(data_processing)
        self.post_processing_tabs.setObjectName(u"post_processing_tabs")
        self.detail_tab = QWidget()
        self.detail_tab.setObjectName(u"detail_tab")
        self.verticalLayout_3 = QVBoxLayout(self.detail_tab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.detail_tab_grid = QGridLayout()
        self.detail_tab_grid.setObjectName(u"detail_tab_grid")
        self.overview_grp = QGroupBox(self.detail_tab)
        self.overview_grp.setObjectName(u"overview_grp")
        self.gridLayout_6 = QGridLayout(self.overview_grp)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.general_cfg = QGridLayout()
        self.general_cfg.setObjectName(u"general_cfg")
        self.label_8 = QLabel(self.overview_grp)
        self.label_8.setObjectName(u"label_8")

        self.general_cfg.addWidget(self.label_8, 6, 0, 1, 1)

        self.label_6 = QLabel(self.overview_grp)
        self.label_6.setObjectName(u"label_6")

        self.general_cfg.addWidget(self.label_6, 4, 0, 1, 1)

        self.label_4 = QLabel(self.overview_grp)
        self.label_4.setObjectName(u"label_4")

        self.general_cfg.addWidget(self.label_4, 3, 0, 1, 1)

        self.label_2 = QLabel(self.overview_grp)
        self.label_2.setObjectName(u"label_2")

        self.general_cfg.addWidget(self.label_2, 2, 0, 1, 1)

        self.t_stop_lbl = QLabel(self.overview_grp)
        self.t_stop_lbl.setObjectName(u"t_stop_lbl")

        self.general_cfg.addWidget(self.t_stop_lbl, 3, 1, 1, 1)

        self.devices_lbl = QLabel(self.overview_grp)
        self.devices_lbl.setObjectName(u"devices_lbl")

        self.general_cfg.addWidget(self.devices_lbl, 6, 1, 1, 1)

        self.duration_lbl = QLabel(self.overview_grp)
        self.duration_lbl.setObjectName(u"duration_lbl")

        self.general_cfg.addWidget(self.duration_lbl, 5, 1, 1, 1)

        self.label_7 = QLabel(self.overview_grp)
        self.label_7.setObjectName(u"label_7")

        self.general_cfg.addWidget(self.label_7, 5, 0, 1, 1)

        self.label = QLabel(self.overview_grp)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(True)
        self.label.setFont(font)

        self.general_cfg.addWidget(self.label, 0, 0, 1, 1)

        self.t_start_lbl = QLabel(self.overview_grp)
        self.t_start_lbl.setObjectName(u"t_start_lbl")

        self.general_cfg.addWidget(self.t_start_lbl, 2, 1, 1, 1)

        self.operator_lbl = QLabel(self.overview_grp)
        self.operator_lbl.setObjectName(u"operator_lbl")

        self.general_cfg.addWidget(self.operator_lbl, 4, 1, 1, 1)

        self.label_17 = QLabel(self.overview_grp)
        self.label_17.setObjectName(u"label_17")

        self.general_cfg.addWidget(self.label_17, 7, 0, 1, 1)

        self.probe_lbl = QLabel(self.overview_grp)
        self.probe_lbl.setObjectName(u"probe_lbl")

        self.general_cfg.addWidget(self.probe_lbl, 7, 1, 1, 1)


        self.gridLayout_6.addLayout(self.general_cfg, 0, 0, 1, 1)

        self.vna_cfg = QGridLayout()
        self.vna_cfg.setObjectName(u"vna_cfg")
        self.label_9 = QLabel(self.overview_grp)
        self.label_9.setObjectName(u"label_9")

        self.vna_cfg.addWidget(self.label_9, 4, 0, 1, 1)

        self.label_13 = QLabel(self.overview_grp)
        self.label_13.setObjectName(u"label_13")

        self.vna_cfg.addWidget(self.label_13, 1, 0, 1, 1)

        self.label_3 = QLabel(self.overview_grp)
        self.label_3.setObjectName(u"label_3")

        self.vna_cfg.addWidget(self.label_3, 2, 0, 1, 1)

        self.rf_pwr_lbl = QLabel(self.overview_grp)
        self.rf_pwr_lbl.setObjectName(u"rf_pwr_lbl")

        self.vna_cfg.addWidget(self.rf_pwr_lbl, 1, 1, 1, 1)

        self.label_12 = QLabel(self.overview_grp)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font)

        self.vna_cfg.addWidget(self.label_12, 0, 0, 1, 1)

        self.label_5 = QLabel(self.overview_grp)
        self.label_5.setObjectName(u"label_5")

        self.vna_cfg.addWidget(self.label_5, 3, 0, 1, 1)

        self.label_10 = QLabel(self.overview_grp)
        self.label_10.setObjectName(u"label_10")

        self.vna_cfg.addWidget(self.label_10, 5, 0, 1, 1)

        self.f_start_lbl = QLabel(self.overview_grp)
        self.f_start_lbl.setObjectName(u"f_start_lbl")

        self.vna_cfg.addWidget(self.f_start_lbl, 2, 1, 1, 1)

        self.f_stop_lbl = QLabel(self.overview_grp)
        self.f_stop_lbl.setObjectName(u"f_stop_lbl")

        self.vna_cfg.addWidget(self.f_stop_lbl, 3, 1, 1, 1)

        self.n_f_lbl = QLabel(self.overview_grp)
        self.n_f_lbl.setObjectName(u"n_f_lbl")

        self.vna_cfg.addWidget(self.n_f_lbl, 4, 1, 1, 1)

        self.param_lbl = QLabel(self.overview_grp)
        self.param_lbl.setObjectName(u"param_lbl")

        self.vna_cfg.addWidget(self.param_lbl, 5, 1, 1, 1)


        self.gridLayout_6.addLayout(self.vna_cfg, 2, 0, 1, 1)

        self.aut_cfg = QGridLayout()
        self.aut_cfg.setObjectName(u"aut_cfg")
        self.aut_com_lbl = QLabel(self.overview_grp)
        self.aut_com_lbl.setObjectName(u"aut_com_lbl")

        self.aut_cfg.addWidget(self.aut_com_lbl, 3, 1, 1, 1)

        self.aut_sn_lbl = QLabel(self.overview_grp)
        self.aut_sn_lbl.setObjectName(u"aut_sn_lbl")

        self.aut_cfg.addWidget(self.aut_sn_lbl, 2, 1, 1, 1)

        self.label_18 = QLabel(self.overview_grp)
        self.label_18.setObjectName(u"label_18")

        self.aut_cfg.addWidget(self.label_18, 1, 0, 1, 1)

        self.label_14 = QLabel(self.overview_grp)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setFont(font)

        self.aut_cfg.addWidget(self.label_14, 0, 0, 1, 1)

        self.label_22 = QLabel(self.overview_grp)
        self.label_22.setObjectName(u"label_22")

        self.aut_cfg.addWidget(self.label_22, 3, 0, 1, 1)

        self.label_20 = QLabel(self.overview_grp)
        self.label_20.setObjectName(u"label_20")

        self.aut_cfg.addWidget(self.label_20, 2, 0, 1, 1)

        self.aut_type_lbl = QLabel(self.overview_grp)
        self.aut_type_lbl.setObjectName(u"aut_type_lbl")

        self.aut_cfg.addWidget(self.aut_type_lbl, 1, 1, 1, 1)


        self.gridLayout_6.addLayout(self.aut_cfg, 1, 0, 1, 1)

        self.meas_cfg = QGridLayout()
        self.meas_cfg.setObjectName(u"meas_cfg")
        self.custom_val_3_lbl = QLabel(self.overview_grp)
        self.custom_val_3_lbl.setObjectName(u"custom_val_3_lbl")

        self.meas_cfg.addWidget(self.custom_val_3_lbl, 6, 1, 1, 1)

        self.label_15 = QLabel(self.overview_grp)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font)

        self.meas_cfg.addWidget(self.label_15, 0, 0, 1, 1)

        self.custom_det_3_lbl = QLabel(self.overview_grp)
        self.custom_det_3_lbl.setObjectName(u"custom_det_3_lbl")

        self.meas_cfg.addWidget(self.custom_det_3_lbl, 6, 0, 1, 1)

        self.custom_det_2_lbl = QLabel(self.overview_grp)
        self.custom_det_2_lbl.setObjectName(u"custom_det_2_lbl")

        self.meas_cfg.addWidget(self.custom_det_2_lbl, 5, 0, 1, 1)

        self.custom_det_0_lbl = QLabel(self.overview_grp)
        self.custom_det_0_lbl.setObjectName(u"custom_det_0_lbl")

        self.meas_cfg.addWidget(self.custom_det_0_lbl, 3, 0, 1, 1)

        self.custom_val_2_lbl = QLabel(self.overview_grp)
        self.custom_val_2_lbl.setObjectName(u"custom_val_2_lbl")

        self.meas_cfg.addWidget(self.custom_val_2_lbl, 5, 1, 1, 1)

        self.custom_val_4_lbl = QLabel(self.overview_grp)
        self.custom_val_4_lbl.setObjectName(u"custom_val_4_lbl")

        self.meas_cfg.addWidget(self.custom_val_4_lbl, 7, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.meas_cfg.addItem(self.verticalSpacer, 9, 1, 1, 1)

        self.custom_val_0_lbl = QLabel(self.overview_grp)
        self.custom_val_0_lbl.setObjectName(u"custom_val_0_lbl")

        self.meas_cfg.addWidget(self.custom_val_0_lbl, 3, 1, 1, 1)

        self.custom_val_1_lbl = QLabel(self.overview_grp)
        self.custom_val_1_lbl.setObjectName(u"custom_val_1_lbl")

        self.meas_cfg.addWidget(self.custom_val_1_lbl, 4, 1, 1, 1)

        self.custom_det_4_lbl = QLabel(self.overview_grp)
        self.custom_det_4_lbl.setObjectName(u"custom_det_4_lbl")

        self.meas_cfg.addWidget(self.custom_det_4_lbl, 7, 0, 1, 1)

        self.meas_type_lbl = QLabel(self.overview_grp)
        self.meas_type_lbl.setObjectName(u"meas_type_lbl")

        self.meas_cfg.addWidget(self.meas_type_lbl, 1, 1, 1, 1)

        self.label_11 = QLabel(self.overview_grp)
        self.label_11.setObjectName(u"label_11")

        self.meas_cfg.addWidget(self.label_11, 2, 0, 1, 1)

        self.label_16 = QLabel(self.overview_grp)
        self.label_16.setObjectName(u"label_16")

        self.meas_cfg.addWidget(self.label_16, 1, 0, 1, 1)

        self.meas_dist_lbl = QLabel(self.overview_grp)
        self.meas_dist_lbl.setObjectName(u"meas_dist_lbl")

        self.meas_cfg.addWidget(self.meas_dist_lbl, 2, 1, 1, 1)

        self.custom_det_1_lbl = QLabel(self.overview_grp)
        self.custom_det_1_lbl.setObjectName(u"custom_det_1_lbl")

        self.meas_cfg.addWidget(self.custom_det_1_lbl, 4, 0, 1, 1)

        self.custom_det_5_lbl = QLabel(self.overview_grp)
        self.custom_det_5_lbl.setObjectName(u"custom_det_5_lbl")

        self.meas_cfg.addWidget(self.custom_det_5_lbl, 8, 0, 1, 1)

        self.custom_val_5_lbl = QLabel(self.overview_grp)
        self.custom_val_5_lbl.setObjectName(u"custom_val_5_lbl")

        self.meas_cfg.addWidget(self.custom_val_5_lbl, 8, 1, 1, 1)


        self.gridLayout_6.addLayout(self.meas_cfg, 0, 1, 3, 1)


        self.detail_tab_grid.addWidget(self.overview_grp, 0, 0, 1, 1)

        self.post_proc_grp = QGroupBox(self.detail_tab)
        self.post_proc_grp.setObjectName(u"post_proc_grp")
        self.verticalLayout_4 = QVBoxLayout(self.post_proc_grp)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.copolar_radio_btn = QRadioButton(self.post_proc_grp)
        self.copolar_radio_btn.setObjectName(u"copolar_radio_btn")
        self.copolar_radio_btn.setEnabled(False)

        self.horizontalLayout_5.addWidget(self.copolar_radio_btn)

        self.crosspolar_radio_btn = QRadioButton(self.post_proc_grp)
        self.crosspolar_radio_btn.setObjectName(u"crosspolar_radio_btn")
        self.crosspolar_radio_btn.setEnabled(False)

        self.horizontalLayout_5.addWidget(self.crosspolar_radio_btn)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.label_19 = QLabel(self.post_proc_grp)
        self.label_19.setObjectName(u"label_19")

        self.horizontalLayout_5.addWidget(self.label_19)

        self.sel_freq_combo = QComboBox(self.post_proc_grp)
        self.sel_freq_combo.setObjectName(u"sel_freq_combo")

        self.horizontalLayout_5.addWidget(self.sel_freq_combo)

        self.horizontalLayout_5.setStretch(3, 1)
        self.horizontalLayout_5.setStretch(4, 3)

        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.line = QFrame(self.post_proc_grp)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_4.addWidget(self.line)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.trans_start_btn = QPushButton(self.post_proc_grp)
        self.trans_start_btn.setObjectName(u"trans_start_btn")

        self.gridLayout_2.addWidget(self.trans_start_btn, 1, 2, 1, 1)

        self.label_21 = QLabel(self.post_proc_grp)
        self.label_21.setObjectName(u"label_21")

        self.gridLayout_2.addWidget(self.label_21, 0, 0, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")

        self.gridLayout_2.addLayout(self.horizontalLayout_6, 0, 2, 1, 1)

        self.transform_combo = QComboBox(self.post_proc_grp)
        self.transform_combo.setObjectName(u"transform_combo")

        self.gridLayout_2.addWidget(self.transform_combo, 0, 1, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout_2)


        self.detail_tab_grid.addWidget(self.post_proc_grp, 1, 0, 1, 1)

        self.result_grp = QGroupBox(self.detail_tab)
        self.result_grp.setObjectName(u"result_grp")
        self.gridLayout_4 = QGridLayout(self.result_grp)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.frame_6 = QFrame(self.result_grp)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.frame_6)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.det_res_plt_2 = QVBoxLayout()
        self.det_res_plt_2.setObjectName(u"det_res_plt_2")

        self.verticalLayout_12.addLayout(self.det_res_plt_2)


        self.gridLayout_4.addWidget(self.frame_6, 3, 0, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.det_res_plt_2_title = QLabel(self.result_grp)
        self.det_res_plt_2_title.setObjectName(u"det_res_plt_2_title")
        font1 = QFont()
        font1.setPointSize(13)
        self.det_res_plt_2_title.setFont(font1)
        self.det_res_plt_2_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.det_res_plt_2_title, 0, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_3, 2, 0, 1, 1)

        self.frame_5 = QFrame(self.result_grp)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.frame_5)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.det_res_plt_1 = QVBoxLayout()
        self.det_res_plt_1.setObjectName(u"det_res_plt_1")

        self.verticalLayout_10.addLayout(self.det_res_plt_1)


        self.gridLayout_4.addWidget(self.frame_5, 1, 0, 1, 1)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.det_res_plt_1_title = QLabel(self.result_grp)
        self.det_res_plt_1_title.setObjectName(u"det_res_plt_1_title")
        self.det_res_plt_1_title.setFont(font1)
        self.det_res_plt_1_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.det_res_plt_1_title, 0, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_5, 0, 0, 1, 1)


        self.detail_tab_grid.addWidget(self.result_grp, 0, 1, 2, 1)

        self.detail_tab_grid.setColumnStretch(0, 3)
        self.detail_tab_grid.setColumnStretch(1, 3)

        self.verticalLayout_3.addLayout(self.detail_tab_grid)

        self.post_processing_tabs.addTab(self.detail_tab, "")
        self.FF_tab = QWidget()
        self.FF_tab.setObjectName(u"FF_tab")
        self.verticalLayout = QVBoxLayout(self.FF_tab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.ff_plots = QTabWidget(self.FF_tab)
        self.ff_plots.setObjectName(u"ff_plots")
        self.ff_uv_plot_tab = QWidget()
        self.ff_uv_plot_tab.setObjectName(u"ff_uv_plot_tab")
        self.verticalLayout_9 = QVBoxLayout(self.ff_uv_plot_tab)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.frame_2 = QFrame(self.ff_uv_plot_tab)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.ff_3d_plot_color_bar = QVBoxLayout()
        self.ff_3d_plot_color_bar.setObjectName(u"ff_3d_plot_color_bar")

        self.horizontalLayout_8.addLayout(self.ff_3d_plot_color_bar)

        self.ff_3d_plot = QVBoxLayout()
        self.ff_3d_plot.setObjectName(u"ff_3d_plot")

        self.horizontalLayout_8.addLayout(self.ff_3d_plot)

        self.ff_uv_plot = QVBoxLayout()
        self.ff_uv_plot.setObjectName(u"ff_uv_plot")

        self.horizontalLayout_8.addLayout(self.ff_uv_plot)

        self.horizontalLayout_8.setStretch(0, 1)
        self.horizontalLayout_8.setStretch(1, 6)
        self.horizontalLayout_8.setStretch(2, 6)

        self.verticalLayout_9.addWidget(self.frame_2)

        self.ff_plots.addTab(self.ff_uv_plot_tab, "")
        self.ff_pattern_cuts = QWidget()
        self.ff_pattern_cuts.setObjectName(u"ff_pattern_cuts")
        self.verticalLayout_11 = QVBoxLayout(self.ff_pattern_cuts)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.style1_widgets = QWidget(self.ff_pattern_cuts)
        self.style1_widgets.setObjectName(u"style1_widgets")
        self.horizontalLayout_3 = QHBoxLayout(self.style1_widgets)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")

        self.horizontalLayout.addWidget(self.style1_widgets)

        self.style2_widgets = QWidget(self.ff_pattern_cuts)
        self.style2_widgets.setObjectName(u"style2_widgets")
        self.horizontalLayout_4 = QHBoxLayout(self.style2_widgets)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")

        self.horizontalLayout.addWidget(self.style2_widgets)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_11.addLayout(self.horizontalLayout)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame_4 = QFrame(self.ff_pattern_cuts)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frame_4)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.ff_cut2_plot = QVBoxLayout()
        self.ff_cut2_plot.setObjectName(u"ff_cut2_plot")

        self.verticalLayout_8.addLayout(self.ff_cut2_plot)


        self.gridLayout.addWidget(self.frame_4, 0, 1, 1, 1)

        self.frame_3 = QFrame(self.ff_pattern_cuts)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_3)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.ff_cut1_plot = QVBoxLayout()
        self.ff_cut1_plot.setObjectName(u"ff_cut1_plot")

        self.verticalLayout_7.addLayout(self.ff_cut1_plot)


        self.gridLayout.addWidget(self.frame_3, 0, 0, 1, 1)


        self.verticalLayout_11.addLayout(self.gridLayout)

        self.ff_plots.addTab(self.ff_pattern_cuts, "")

        self.verticalLayout.addWidget(self.ff_plots)

        self.post_processing_tabs.addTab(self.FF_tab, "")

        self.horizontalLayout_2.addWidget(self.post_processing_tabs)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 3)

        self.retranslateUi(data_processing)

        self.post_processing_tabs.setCurrentIndex(1)
        self.ff_plots.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(data_processing)
    # setupUi

    def retranslateUi(self, data_processing):
        data_processing.setWindowTitle(QCoreApplication.translate("data_processing", u"Form", None))
        self.tree_view_refresh_btn.setText(QCoreApplication.translate("data_processing", u"Refresh", None))
        self.overview_grp.setTitle(QCoreApplication.translate("data_processing", u"Overview", None))
        self.label_8.setText(QCoreApplication.translate("data_processing", u"Devices:", None))
        self.label_6.setText(QCoreApplication.translate("data_processing", u"Operator:", None))
        self.label_4.setText(QCoreApplication.translate("data_processing", u"Time Stop:", None))
        self.label_2.setText(QCoreApplication.translate("data_processing", u"Time Start:", None))
        self.t_stop_lbl.setText("")
        self.devices_lbl.setText("")
        self.duration_lbl.setText("")
        self.label_7.setText(QCoreApplication.translate("data_processing", u"Duration:", None))
        self.label.setText(QCoreApplication.translate("data_processing", u"General", None))
        self.t_start_lbl.setText("")
        self.operator_lbl.setText("")
        self.label_17.setText(QCoreApplication.translate("data_processing", u"Probe:", None))
        self.probe_lbl.setText("")
        self.label_9.setText(QCoreApplication.translate("data_processing", u"N-points:", None))
        self.label_13.setText(QCoreApplication.translate("data_processing", u"RF Power:", None))
        self.label_3.setText(QCoreApplication.translate("data_processing", u"F start:", None))
        self.rf_pwr_lbl.setText("")
        self.label_12.setText(QCoreApplication.translate("data_processing", u"VNA", None))
        self.label_5.setText(QCoreApplication.translate("data_processing", u"F stop:", None))
        self.label_10.setText(QCoreApplication.translate("data_processing", u"Parameter:", None))
        self.f_start_lbl.setText("")
        self.f_stop_lbl.setText("")
        self.n_f_lbl.setText("")
        self.param_lbl.setText("")
        self.aut_com_lbl.setText("")
        self.aut_sn_lbl.setText("")
        self.label_18.setText(QCoreApplication.translate("data_processing", u"Type:", None))
        self.label_14.setText(QCoreApplication.translate("data_processing", u"AUT", None))
        self.label_22.setText(QCoreApplication.translate("data_processing", u"Comment:", None))
        self.label_20.setText(QCoreApplication.translate("data_processing", u"Serial Number:", None))
        self.aut_type_lbl.setText("")
        self.custom_val_3_lbl.setText("")
        self.label_15.setText(QCoreApplication.translate("data_processing", u"Measurement:", None))
        self.custom_det_3_lbl.setText("")
        self.custom_det_2_lbl.setText("")
        self.custom_det_0_lbl.setText("")
        self.custom_val_2_lbl.setText("")
        self.custom_val_4_lbl.setText("")
        self.custom_val_0_lbl.setText("")
        self.custom_val_1_lbl.setText("")
        self.custom_det_4_lbl.setText("")
        self.meas_type_lbl.setText("")
        self.label_11.setText(QCoreApplication.translate("data_processing", u"Distance:", None))
        self.label_16.setText(QCoreApplication.translate("data_processing", u"Type:", None))
        self.meas_dist_lbl.setText("")
        self.custom_det_1_lbl.setText("")
        self.custom_det_5_lbl.setText("")
        self.custom_val_5_lbl.setText("")
        self.post_proc_grp.setTitle(QCoreApplication.translate("data_processing", u"Post Processing", None))
        self.copolar_radio_btn.setText(QCoreApplication.translate("data_processing", u"Copolar", None))
        self.crosspolar_radio_btn.setText(QCoreApplication.translate("data_processing", u"Cross-polar", None))
        self.label_19.setText(QCoreApplication.translate("data_processing", u"Frequency:", None))
        self.trans_start_btn.setText(QCoreApplication.translate("data_processing", u"Transform", None))
        self.label_21.setText(QCoreApplication.translate("data_processing", u"Transformation:", None))
        self.result_grp.setTitle(QCoreApplication.translate("data_processing", u"Results", None))
        self.det_res_plt_2_title.setText("")
        self.det_res_plt_1_title.setText("")
        self.post_processing_tabs.setTabText(self.post_processing_tabs.indexOf(self.detail_tab), QCoreApplication.translate("data_processing", u"Detail", None))
        self.ff_plots.setTabText(self.ff_plots.indexOf(self.ff_uv_plot_tab), QCoreApplication.translate("data_processing", u"3D Pattern / UV plot", None))
        self.ff_plots.setTabText(self.ff_plots.indexOf(self.ff_pattern_cuts), QCoreApplication.translate("data_processing", u"Pattern Cuts", None))
        self.post_processing_tabs.setTabText(self.post_processing_tabs.indexOf(self.FF_tab), QCoreApplication.translate("data_processing", u"Far-Field", None))
    # retranslateUi

