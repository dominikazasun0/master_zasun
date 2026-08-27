__author__ = "Kacper Marks"
__copyright__ = ""
__version__ = "1.0"
__email__ = "k.marks@microamp-solutions.com"
__status__ = "Development"
__year__ = "2025"

import numpy as np
import logging
from .base import NF2FF, NF2FFData
from src.Data_Processing.measurement.config import FFData

log = logging.getLogger("GUI")

class PWS(NF2FF):
    def compute(self) -> FFData:
        try:
            # 1. Setup dimensions and Sampling
            N_pad = 256  # Target size
            dy, dx = self.nf.sampling  # sampling in meters
            dy = round(dy/100.0,7)
            dx = round(dx/100.0,7)
            E_co = self.nf.copolar_data
            copolar_rot_rad = 0
            if self.nf.cross_pol:
                E_cross = self.nf.crosspolar_data
            else:
                E_cross = np.zeros_like(E_co)
            Ex_nf = -E_cross*np.cos(copolar_rot_rad) + E_co*np.sin(copolar_rot_rad)
            Ey_nf =  E_cross*np.sin(copolar_rot_rad) + E_co*np.cos(copolar_rot_rad)

            Ax = np.fft.fftshift(np.fft.ifft2(Ex_nf, (N_pad, N_pad))) * dx * dy
            Ay = np.fft.fftshift(np.fft.ifft2(Ey_nf, (N_pad, N_pad))) * dx * dy
            Ax = np.flipud(Ax)
            Ay = np.flipud(Ay)
            kx_step = 2 * np.pi / (N_pad * dx)
            ky_step = 2 * np.pi / (N_pad * dy)
            kx = np.linspace(-1 * kx_step * N_pad/2, kx_step * N_pad/2 , N_pad)
            ky = np.linspace(-1 * ky_step * N_pad/2, ky_step * N_pad/2 , N_pad)
            U = kx / self.k
            V = ky / self.k
            U_grid, V_grid = np.meshgrid(U, V)
            mask = U_grid**2 + V_grid**2 <= 1

            r=100
            theta = np.arcsin(np.sqrt(U_grid**2 + V_grid**2))
            phi = np.arctan2(V_grid, U_grid)
            C = (1j * self.k * np.exp(-1j * self.k * r)) / (2 * np.pi * r)
            E_theta = C * (Ax * np.cos(phi) + Ay * np.sin(phi))
            E_phi = C * np.cos(theta) * (-Ax * np.sin(phi) + Ay * np.cos(phi))
            E_theta[~mask] = None
            E_phi[~mask] = None
            theta[~mask] = None
            phi[~mask] = None
            return FFData(
                frequency_hz=self.nf.frequency_hz,
                meshgrid=np.stack([theta, phi]), 
                e_theta=E_theta,
                e_phi=E_phi,
            )
        except Exception as e:
            log.error(e)

class MoM(NF2FF):
    def compute(self):
        pass