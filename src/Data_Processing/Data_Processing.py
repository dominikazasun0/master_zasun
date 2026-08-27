import sys
import numpy as np
from PySide6 import QtWidgets
from PySide6.QtGui import QColor
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from OpenGL import GL as gl_lib



# ---------- Axes ----------
class Axes3D(gl.GLGraphicsItem.GLGraphicsItem):
    def __init__(self, size=1.2):
        super().__init__()
        self.size = size
        self.color_x = (0.85, 0.1, 0.1, 1.0)
        self.color_y = (0.1, 0.6, 0.1, 1.0)
        self.color_z = (0.1, 0.1, 0.9, 1.0)
    def paint(self):
        gl_lib.glLineWidth(3.0)
        gl_lib.glBegin(gl_lib.GL_LINES)
        gl_lib.glColor4f(*self.color_x); gl_lib.glVertex3f(0,0,0); gl_lib.glVertex3f(self.size,0,0)
        gl_lib.glColor4f(*self.color_y); gl_lib.glVertex3f(0,0,0); gl_lib.glVertex3f(0,self.size,0)
        gl_lib.glColor4f(*self.color_z); gl_lib.glVertex3f(0,0,0); gl_lib.glVertex3f(0,0,self.size)
        gl_lib.glEnd()


# ---------- Array factor (rectangular array) ----------
def array_factor_rect(Nx=16, Ny=16, dx=0.5, dy=0.5,
                      theta0_deg=20.0, phi0_deg=30.0,
                      window="hann",
                      n_theta=120, n_phi=240,
                      upper_hemisphere_only=True):
    """
    AF for Nx x Ny array; spacings dx,dy in wavelengths. Returns TH, PH, AF_mag (linear, max=1).
    If upper_hemisphere_only=True, theta spans [0, pi/2] (z>0).
    """
    k0 = 2.0 * np.pi  # spacings in wavelengths => k0=2π

    th0 = np.deg2rad(theta0_deg)
    ph0 = np.deg2rad(phi0_deg)
    sx0 = np.sin(th0) * np.cos(ph0)
    sy0 = np.sin(th0) * np.sin(ph0)

    mx = np.arange(Nx) - (Nx - 1) / 2.0
    my = np.arange(Ny) - (Ny - 1) / 2.0
    x = mx * dx
    y = my * dy

    if not window:
        wx = np.ones(Nx); wy = np.ones(Ny)
    else:
        w = window.lower()
        wx = np.hanning(Nx) if w == "hann" else (np.hamming(Nx) if w == "hamming" else np.ones(Nx))
        wy = np.hanning(Ny) if w == "hann" else (np.hamming(Ny) if w == "hamming" else np.ones(Ny))
    w2d = np.outer(wx, wy)

    th_max = np.pi/2 if upper_hemisphere_only else np.pi
    theta = np.linspace(0.0, th_max, n_theta, endpoint=True)
    phi   = np.linspace(0.0, 2*np.pi, n_phi, endpoint=False)
    TH, PH = np.meshgrid(theta, phi, indexing="ij")

    sx = np.sin(TH) * np.cos(PH)
    sy = np.sin(TH) * np.sin(PH)

    # phase factors (vectorized)
    P = sx.size
    phase_x = np.exp(1j * k0 * np.outer(x, (sx - sx0).ravel()))  # (Nx, P)
    phase_y = np.exp(1j * k0 * np.outer(y, (sy - sy0).ravel()))  # (Ny, P)
    AF = (phase_x[:, None, :] * phase_y[None, :, :]) * w2d[:, :, None]
    AF = AF.sum(axis=(0,1)).reshape(TH.shape)

    AF_mag = np.abs(AF).astype(np.float32)
    AF_mag /= AF_mag.max() + 1e-12
    return TH, PH, AF_mag


# ---------- Mesh builder with dB coloring ----------
def pattern_mesh_db(theta, phi, AF_mag, min_db=-40.0, cmap_name="viridis",
                    radius_mode="db", gamma=1.0):
    """
    Map |AF| to dB for both color and (optionally) radius.
    radius_mode: "db" -> radius ∝ normalized dB, "linear" -> old behavior.
    gamma: visual contrast for dB radius (1.0 = linear; <1 boosts sidelobes).
    """
    # dB for coloring (and maybe radius)
    AF_dB = 20.0 * np.log10(np.clip(AF_mag, 1e-12, 1.0))
    AF_dB = np.maximum(AF_dB, min_db)

    if radius_mode == "db":
        # Normalize dB: min_db -> 0, 0 dB -> 1
        r = (AF_dB - min_db) / (0.0 - min_db)
        r = np.clip(r, 0.0, 1.0)
        if gamma != 1.0:
            r = np.power(r, gamma)   # e.g., gamma=0.7 makes sidelobes fatter
        r = r.astype(np.float32)
    else:
        r = AF_mag.astype(np.float32)  # legacy: linear amplitude

    # Spherical -> Cartesian
    st, ct = np.sin(theta), np.cos(theta)
    cp, sp = np.cos(phi), np.sin(phi)
    X = (r * st * cp).astype(np.float32)
    Y = (r * st * sp).astype(np.float32)
    Z = (r * ct).astype(np.float32)

    # Triangulate (wrap in phi)
    n_th, n_ph = theta.shape
    verts = np.stack([X, Y, Z], axis=-1).reshape(-1, 3)
    faces = []
    for i in range(n_th - 1):
        for j in range(n_ph):
            jn = (j + 1) % n_ph
            a = i * n_ph + j
            b = (i + 1) * n_ph + j
            c = (i + 1) * n_ph + jn
            d = i * n_ph + jn
            faces.append([a, b, c]); faces.append([a, c, d])
    faces = np.asarray(faces, dtype=np.int32)

    # Colors from dB
    t = (AF_dB.reshape(-1) - min_db) / (0.0 - min_db)
    t = np.clip(t, 0.0, 1.0)
    cmap = pg.colormap.get(cmap_name)
    colors = cmap.map(t, mode='float').astype(np.float32)

    md = gl.MeshData(vertexes=verts, faces=faces)
    md.setVertexColors(colors)
    return gl.GLMeshItem(meshdata=md, smooth=False, drawFaces=True, drawEdges=False)


# ---------- App widget ----------
class PhasedArrayPattern(QtWidgets.QWidget):
    def __init__(self,
                 Nx=16, Ny=16, dx=0.5, dy=0.5,
                 theta0=25.0, phi0=40.0,
                 window="hann",
                 n_theta=140, n_phi=280,
                 min_db=-40.0):
        super().__init__()
        lay = QtWidgets.QVBoxLayout(self); lay.setContentsMargins(0,0,0,0)

        self.view = gl.GLViewWidget()
        self.view.setBackgroundColor('w')      # white background
        self.view.opts['distance'] = 5
        lay.addWidget(self.view)

        # subtle grid + axes
        grid = gl.GLGridItem(); grid.setSize(2, 2); grid.setSpacing(0.1, 0.1)
        grid.setColor(QColor("black"))
        self.view.addItem(grid)
        self.view.addItem(Axes3D(size=1))

        # compute AF on upper hemisphere only
        TH, PH, AF = array_factor_rect(Nx=Nx, Ny=Ny, dx=dx, dy=dy,
                                       theta0_deg=theta0, phi0_deg=phi0,
                                       window=window, n_theta=n_theta, n_phi=n_phi,
                                       upper_hemisphere_only=True)

        mesh = pattern_mesh_db(TH, PH, AF,
                            min_db=-40.0,
                            cmap_name="viridis",
                            radius_mode="db",   # <- key change
                            gamma=0.8)          # try 0.6..1.0 to inflate sidelobes
        self.view.addItem(mesh)

    #     # steering direction arrow (always in upper hemisphere by request)
    #     self._add_steer_arrow(theta0, phi0)

    # def _add_steer_arrow(self, theta0, phi0, length=1.2, color=(0.0, 0.0, 0.0, 0.9)):
    #     th = np.deg2rad(theta0); ph = np.deg2rad(phi0)
    #     dir3 = np.array([np.sin(th)*np.cos(ph), np.sin(th)*np.sin(ph), np.cos(th)], dtype=np.float32)
    #     if dir3[2] <= 0:
    #         return  # skip if user steers below horizon but we plot only z>0
    #     line = np.vstack([np.zeros(3, np.float32), length*dir3]).astype(np.float32)
    #     self.view.addItem(gl.GLLinePlotItem(pos=line, width=3.0, mode='lines', color=color, antialias=True))

