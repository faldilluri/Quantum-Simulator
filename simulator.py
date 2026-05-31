#!/usr/bin/env python
# coding: utf-8

# In[8]:


import numpy as np

def initialize_state(n_qubits):
    """
    Krijon gjendjen fillestare |0...0> për n kubite.

    Args:
        n_qubits (int): Numri i kubitëve.

    Returns:
        numpy.ndarray: Vektori i gjendjes me 2^n elemente.
                       Elementi i parë është 1+0j, të tjerët 0+0j.
    """
    size = 2 ** n_qubits
    state = np.zeros(size, dtype=complex)
    state[0] = 1 + 0j
    return state


# Ky funksion krijon një vektor me 2^n
#   elemente, ku vetëm gjendja ∣0⟩ ⊗n
#   ka amplitudë 1. Për shembull, për 2 kubite, prodhon [1+0j, 0+0j, 0+0j, 0+0j].

# In[2]:


def apply_single_qubit_gate(state, gate, target, n_qubits):
    """
    Aplikon një portë me një kubit (matricë 2x2) mbi një kubit të caktuar.

    Args:
        state (numpy.ndarray): Vektori i gjendjes aktuale.
        gate (numpy.ndarray): Matrica 2x2 e portës.
        target (int): Indeksi i kubitit mbi të cilin aplikohet porta (0 = më i rëndësishmi).
        n_qubits (int): Numri total i kubitëve.

    Returns:
        numpy.ndarray: Vektori i gjendjes pas aplikimit të portës.
    """
    size = 2 ** n_qubits
    new_state = np.zeros(size, dtype=complex)

    # Për çdo indeks të bazës, llogarisim çiftin përkatës
    for i in range(size):
        # Kontrollojmë nëse biti i synuar është 0 apo 1 në indeksin i
        # Nëse është 1, e kapërcejmë sepse do të përpunohet nga çifti i tij
        if (i >> (n_qubits - 1 - target)) & 1:
            continue

        # Ndërtojmë indeksin e çiftit (ku biti i synuar është 1)
        i_pair = i | (1 << (n_qubits - 1 - target))

        # Marrim amplitudat përkatëse
        a0 = state[i]
        a1 = state[i_pair]

        # Aplikojmë portën
        new_state[i] = gate[0, 0] * a0 + gate[0, 1] * a1
        new_state[i_pair] = gate[1, 0] * a0 + gate[1, 1] * a1

    return new_state


# Aplikimi i një porte me një kubit
# Këtu zbatojmë teknikën qubit-wise multiplication nga tutoriali i McGuffin. Supozojmë se biti më i rëndësishëm është kubiti 0 (majtas), siç kemi vepruar në të gjithë shembujt

# In[3]:


def apply_cnot(state, control, target, n_qubits):
    """
    Aplikon portën CNOT me kontroll dhe objektiv të caktuar.

    Args:
        state (numpy.ndarray): Vektori i gjendjes.
        control (int): Indeksi i kubitit të kontrollit.
        target (int): Indeksi i kubitit objektiv.
        n_qubits (int): Numri total i kubitëve.

    Returns:
        numpy.ndarray: Vektori i gjendjes pas CNOT.
    """
    size = 2 ** n_qubits
    new_state = state.copy()

    pos_c = n_qubits - 1 - control
    pos_t = n_qubits - 1 - target

    for i in range(size):
        # Kontrollojmë nëse biti i kontrollit është 1
        if (i >> pos_c) & 1:
            # Përmbys bitin e objektivit
            i_flipped = i ^ (1 << pos_t)
            # Këmbejmë amplitudat
            new_state[i], new_state[i_flipped] = state[i_flipped], state[i]

    return new_state


# Aplikimi i një porte CNOT
# Për portën CNOT, mund ta implementojmë si
# një funksion të veçantë që përdor një qasje 
# të ngjashme, duke përpunuar vetëm kombinimet
# ku kubiti i kontrollit është 1.

# Measure state (poshte)

# In[4]:


import random

def measure(state):
    """
    Kryen një matje mbi të gjithë kubitët dhe kthen gjendjen e shembur.

    Args:
        state (numpy.ndarray): Vektori i gjendjes aktuale.

    Returns:
        tuple: (gjendja_e_shembur, rezultati_i_matjes)
               - gjendja_e_shembur: numpy.ndarray, vektori i gjendjes pas matjes.
               - rezultati_i_matjes: int, indeksi i gjendjes së matur.
    """
    n_qubits = int(np.log2(len(state)))
    probs = np.abs(state) ** 2

    # Zgjedh rastësisht një gjendje sipas probabiliteteve
    result = random.choices(range(len(state)), weights=probs, k=1)[0]

    # Shemb gjendjen: krijo një vektor të ri me 1 në pozicionin e matur
    collapsed_state = np.zeros(len(state), dtype=complex)
    collapsed_state[result] = state[result] / np.sqrt(probs[result])

    return collapsed_state, result


# lart Shpjegim:
# 
# Llogarisim probabilitetet për secilën gjendje bazë (∣ai∣ ne fuqi2 ).
# 
# Përdorim random.choices për të zgjedhur një gjendje në mënyrë të rastësishme, por të ponderuar.
# 
# Shembim gjendjen: krijojmë një vektor të ri ku vetëm gjendja e matur ruan amplitudën e saj, të ri-normalizuar.

# 5:Marrja e probabiliteteve pa shembje
# Ky funksion është i dobishëm për të parë shpërndarjen e probabiliteteve pa ndryshuar gjendjen.

# In[5]:


def get_probabilities(state):
    """
    Kthen probabilitetet e matjes për secilën gjendje bazë.

    Args:
        state (numpy.ndarray): Vektori i gjendjes aktuale.

    Returns:
        numpy.ndarray: Vektori me probabilitetet për secilën gjendje.
    """
    return np.abs(state) ** 2


# 6.Aplikimi i një porte me dy kubite (të përgjithshme)
# Ky funksion aplikon një matricë 4×4 mbi dy kubitë. Supozojmë se rendi i kubitëve në matricë është (control, target) në rastin e CNOT, ose (qubit1, qubit2) për SWAP.

# In[6]:


def apply_two_qubit_gate(state, gate, qubit1, qubit2, n_qubits):
    """
    Aplikon një portë me dy kubite (matricë 4x4) mbi dy kubitë.

    Args:
        state (numpy.ndarray): Vektori i gjendjes aktuale.
        gate (numpy.ndarray): Matrica 4x4 e portës.
        qubit1 (int): Indeksi i kubitit të parë.
        qubit2 (int): Indeksi i kubitit të dytë.
        n_qubits (int): Numri total i kubitëve.

    Returns:
        numpy.ndarray: Vektori i gjendjes pas aplikimit të portës.
    """
    size = 2 ** n_qubits
    new_state = np.zeros(size, dtype=complex)

    pos1 = n_qubits - 1 - qubit1
    pos2 = n_qubits - 1 - qubit2

    for i in range(size):
        # Përpunohen vetëm indekset ku të dy bitet janë 0
        if ((i >> pos1) & 1) or ((i >> pos2) & 1):
            continue

        # Ndërtohen katër indekset për kombinimet (00, 01, 10, 11)
        i00 = i
        i01 = i | (1 << pos2)
        i10 = i | (1 << pos1)
        i11 = i | (1 << pos1) | (1 << pos2)

        # Vlerat përkatëse
        amps = np.array([state[i00], state[i01], state[i10], state[i11]])

        # Aplikohet porta dhe ruhen rezultatet
        new_amps = gate @ amps

        new_state[i00] = new_amps[0]
        new_state[i01] = new_amps[1]
        new_state[i10] = new_amps[2]
        new_state[i11] = new_amps[3]

    return new_state


# 6: shpjegim 
# Identifikojmë pozicionet e biteve për kubitin e kontrollit dhe objektivit.
# 
# Kalojmë nëpër të gjithë indekset e vektorit të gjendjes. Ne përpunojmë vetëm ato ku të dy bitet (kontrolli dhe objektivi) janë 0.
# 
# Për secilin indeks të tillë, ndërtojmë katër indekset që përfaqësojnë kombinimet 00, 01, 10, 11 të këtyre dy biteve.
# 
# Aplikojmë portën 4×4 mbi katër amplitudat përkatëse.
# 

# In[ ]:




