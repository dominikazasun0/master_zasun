# robot_viewer.py (PyQt6)
import os
import math
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.Qt3DCore import QEntity, QTransform
from PyQt6.Qt3DExtras import (
    Qt3DWindow, QCylinderMesh, QPhongMaterial, QOrbitCameraController,
    QConeMesh, QCuboidMesh  # Cuboid not used, but handy if you swap shapes
)
from PyQt6.Qt3DRender import QPointLight


# ---------- Small helper to build XYZ axes ----------
def add_axes(parent: QEntity, length=0.6, radius=0.01, head_len=0.06, head_rad=0.03):
    def make_arrow(color: QtGui.QColor, axis: str):
        # Shaft (cylinder, aligned on Y by default)
        shaft = QEntity(parent)
        shaft_mesh = QCylinderMesh()
        shaft_mesh.setLength(length)
        shaft_mesh.setRadius(radius)
        shaft_tf = QTransform()
        shaft_tf.setTranslation(QtGui.QVector3D(0, length/2, 0))
        shaft_mat = QPhongMaterial(shaft)
        shaft_mat.setDiffuse(color)
        shaft.addComponent(shaft_mesh)
        shaft.addComponent(shaft_tf)
        shaft.addComponent(shaft_mat)

        # Head (cone)
        head = QEntity(parent)
        head_mesh = QConeMesh()
        head_mesh.setLength(head_len)
        head_mesh.setTopRadius(0.0)
        head_mesh.setBottomRadius(head_rad)
        head_tf = QTransform()
        head_tf.setTranslation(QtGui.QVector3D(0, length + head_len/2, 0))
        head_mat = QPhongMaterial(head)
        head_mat.setDiffuse(color)
        head.addComponent(head_mesh)
        head.addComponent(head_tf)
        head.addComponent(head_mat)

        # Rotate to desired axis (default is +Y)
        if axis == "x":
            for tf in (shaft_tf, head_tf):
                tf.setRotationZ(-90)  # Y -> X
        elif axis == "z":
            for tf in (shaft_tf, head_tf):
                tf.setRotationX(90)   # Y -> Z

    make_arrow(QtGui.QColor("#FF3B30"), "x")  # red-ish
    make_arrow(QtGui.QColor("#34C759"), "y")  # green-ish
    make_arrow(QtGui.QColor("#0A84FF"), "z")  # blue-ish


class RevoluteLink:
    def __init__(self, parent: QEntity, length: float, radius: float, color: QtGui.QColor):
        self.jointEntity = QEntity(parent)
        self.jointTf = QTransform()
        self.jointEntity.addComponent(self.jointTf)

        self.linkEntity = QEntity(self.jointEntity)
        self.mesh = QCylinderMesh()
        self.mesh.setLength(length)
        self.mesh.setRadius(radius)

        self.linkTf = QTransform()
        self.linkTf.setTranslation(QtGui.QVector3D(0.0, length / 2.0, 0.0))

        self.mat = QPhongMaterial(self.linkEntity)
        self.mat.setDiffuse(color)

        self.linkEntity.addComponent(self.mesh)
        self.linkEntity.addComponent(self.linkTf)
        self.linkEntity.addComponent(self.mat)

        self.tipEntity = QEntity(self.linkEntity)
        self.tipTf = QTransform()
        self.tipTf.setTranslation(QtGui.QVector3D(0.0, length / 2.0, 0.0))
        self.tipEntity.addComponent(self.tipTf)

    def set_angle_deg(self, deg: float, axis: str = "z"):
        ax = axis.lower()
        if ax == "z":
            self.jointTf.setRotationZ(deg)
        elif ax == "y":
            self.jointTf.setRotationY(deg)
        elif ax == "x":
            self.jointTf.setRotationX(deg)


class RobotViewer(QtWidgets.QWidget):
    def __init__(self, link_lengths=(1.0, 0.7, 0.5), parent=None):
        super().__init__(parent)

        self.view = Qt3DWindow()
        self.container = QtWidgets.QWidget.createWindowContainer(self.view, self)
        self.container.setMinimumSize(800, 600)
        self.container.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.container)

        self.root = QEntity()

        # Light
        lightEnt = QEntity(self.root)
        light = QPointLight(lightEnt)
        light.setColor(QtGui.QColor("white"))
        light.setIntensity(1.0)
        lightTf = QTransform()
        lightTf.setTranslation(QtGui.QVector3D(6, 6, 6))
        lightEnt.addComponent(light)
        lightEnt.addComponent(lightTf)

        # Axes
        add_axes(self.root, length=0.5)

        # Robot links
        self.links = []
        parent_entity = self.root
        colors = [QtGui.QColor("#4CAF50"), QtGui.QColor("#03A9F4"), QtGui.QColor("#FFC107")]
        radius = 0.05
        for i, L in enumerate(link_lengths):
            link = RevoluteLink(parent_entity, L, radius, colors[i % len(colors)])
            self.links.append(link)
            parent_entity = link.tipEntity

        # Camera
        self._setup_camera()

        self.view.setRootEntity(self.root)

    def _setup_camera(self):
        cam = self.view.camera()
        cam.lens().setPerspectiveProjection(45.0, 16/9, 0.01, 100.0)
        cam.setPosition(QtGui.QVector3D(3.0, 2.0, 3.5))
        cam.setViewCenter(QtGui.QVector3D(0.0, 0.5, 0.0))
        cam.setUpVector(QtGui.QVector3D(0.0, 1.0, 0.0))

        controller = QOrbitCameraController(self.root)
        controller.setLinearSpeed(4.0)
        controller.setLookSpeed(120.0)
        controller.setCamera(cam)

    def set_joint_angles(self, angles_deg, axes=None):
        if axes is None:
            axes = ["z"] * len(angles_deg)
        for link, a, ax in zip(self.links, angles_deg, axes):
            link.set_angle_deg(float(a), ax)

    def set_joint_angles_rad(self, angles_rad, axes=None):
        self.set_joint_angles([math.degrees(a) for a in angles_rad], axes)


if __name__ == "__main__":
    import sys, math
    app = QtWidgets.QApplication(sys.argv)

    w = RobotViewer(link_lengths=(1.0, 0.7, 0.5))
    w.setWindowTitle("Qt3D Robot Viewer (PyQt6)")
    w.resize(900, 650)
    w.show()

    w.t = 0.0
    w.timer = QtCore.QTimer(w)  # keep as child of the widget
    w.timer.setInterval(16)

    def tick():
        try:
            w.t += 0.016
            q1 = 30.0 * math.sin(w.t * 0.9)
            q2 = 45.0 * math.sin(w.t * 1.2 + 0.7)
            q3 = 60.0 * math.sin(w.t * 1.6 + 1.1)
            w.set_joint_angles([q1, q2, q3])
        except Exception as e:
            import traceback; traceback.print_exc()
            w.timer.stop()  # don’t keep crashing the loop

    w.timer.timeout.connect(tick)
    w.timer.start()

    sys.exit(app.exec())
