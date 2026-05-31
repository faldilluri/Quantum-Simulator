#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np

import matplotlib.pyplot as plt
from qiskit.visualization import plot_bloch_vector
from qiskit.quantum_info import Statevector

def hadamard():
    """Kthen matricën e portës Hadamard."""
    return np.array([[1, 1], 
                    [1, -1]], dtype=complex) / np.sqrt(2)

def pauli_x():
    """Kthen matricën e portës X (NOT)."""
    return np.array([[0, 1],
                     [1, 0]], dtype=complex)

def pauli_y():
    """Kthen matricën e portës Y."""
    return np.array([[0, -1j], 
                    [1j, 0]], dtype=complex)

def pauli_z():
    """Kthen matricën e portës Z."""
    return np.array([[1, 0],
                     [0, -1]], dtype=complex)

def phase_s():
    """Kthen matricën e portës S (Phase)."""
    return np.array([[1, 0], 
                    [0, 1j]], dtype=complex)

def phase_t():
    """Kthen matricën e portës T."""
    return np.array([[1, 0],
                      [0, np.exp(1j * np.pi / 4)]], dtype=complex)

def ry_gate(theta):
    """Kthen matricën e rrotullimit Ry(theta)."""
    return np.array([[np.cos(theta/2), -np.sin(theta/2)],
                     [np.sin(theta/2),  np.cos(theta/2)]], dtype=complex)

def rz_gate(alpha):
    """Kthen matricën e rrotullimit Rz(alpha)."""
    return np.array([[np.exp(-1j * alpha/2), 0],
                     [0, np.exp(1j * alpha/2)]], dtype=complex)

def cnot():
    """Kthen matricën e portës CNOT (4x4, kontrolli kubiti 0, objektivi kubiti 1)."""
    return np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 1],
                     [0, 0, 1, 0]], dtype=complex)

def swap():
    """Kthen matricën e portës SWAP (4x4)."""
    return np.array([[1, 0, 0, 0],
                     [0, 0, 1, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 1]], dtype=complex)

def cz():
    """Kthen matricën e portës CZ (Controlled-Z)."""
    return np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, -1]], dtype=complex)