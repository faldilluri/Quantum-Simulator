#!/usr/bin/env python
# coding: utf-8

# Importet dhe inicializimi

# In[2]:


import numpy as np
import sys
sys.path.append('./')  # Për të siguruar që modulet tona gjenden

from gates import hadamard, pauli_x, pauli_z, pauli_y, cnot, swap, cz, phase_s, phase_t, ry_gate, rz_gate

from simulator import initialize_state, apply_single_qubit_gate, apply_cnot, apply_two_qubit_gate, measure, get_probabilities
from visualization import plot_probabilities, plot_bloch_sphere


# Bell State

# In[ ]:


def bell_state():
    """
    Krijon gjendjen Bell |Φ⁺⟩ = (|00> + |11>)/√2.

    Returns:
        numpy.ndarray: Vektori i gjendjes përfundimtare.
    """
    n_qubits = 2
    state = initialize_state(n_qubits)

    # Hapi 1: Hadamard në kubitin e parë (indeksi 0)
    state = apply_single_qubit_gate(state, hadamard(), target=0, n_qubits=n_qubits)

    # Hapi 2: CNOT me kontroll kubitin 0 dhe objektiv kubitin 1
    state = apply_cnot(state, control=0, target=1, n_qubits=n_qubits)

    return state

# Testimi
state_bell = bell_state()
print("Gjendja Bell |Φ⁺⟩:")
print(state_bell)
print("Probabilitetet:", get_probabilities(state_bell))

# Vizualizimi
plot_probabilities(state_bell, title="Gjendja Bell |Φ⁺⟩")


#  Deutsch

# In[ ]:


def deutsch(oracle_type='constant_0'):
    """
    Implementon algoritmin e Deutsch-it për një funksion me 1 bit hyrje.

    Args:
        oracle_type (str): Lloji i orakullit. Opsionet:
            'constant_0': f(x) = 0
            'constant_1': f(x) = 1
            'balanced_id': f(x) = x
            'balanced_not': f(x) = NOT x

    Returns:
        int: 0 nëse funksioni është konstant, 1 nëse është i balancuar.
    """
    n_qubits = 2
    state = initialize_state(n_qubits)

    # Hapi 1: Aplikojmë X në kubitin e dytë
    state = apply_single_qubit_gate(state, pauli_x(), target=1, n_qubits=n_qubits)

    # Hapi 2: Hadamard në të dy kubitët
    state = apply_single_qubit_gate(state, hadamard(), target=0, n_qubits=n_qubits)
    state = apply_single_qubit_gate(state, hadamard(), target=1, n_qubits=n_qubits)

    # Hapi 3: Aplikojmë orakullin
    if oracle_type == 'constant_0':
        pass  # Bëj asgjë
    elif oracle_type == 'constant_1':
        # X në kubitin e dytë
        state = apply_single_qubit_gate(state, pauli_x(), target=1, n_qubits=n_qubits)
    elif oracle_type == 'balanced_id':
        # CNOT me kontroll 0, objektiv 1
        state = apply_cnot(state, control=0, target=1, n_qubits=n_qubits)
    elif oracle_type == 'balanced_not':
        # CNOT pastaj X
        state = apply_cnot(state, control=0, target=1, n_qubits=n_qubits)
        state = apply_single_qubit_gate(state, pauli_x(), target=1, n_qubits=n_qubits)

    # Hapi 4: Hadamard në kubitin e parë
    state = apply_single_qubit_gate(state, hadamard(), target=0, n_qubits=n_qubits)

    # Hapi 5: Matja e kubitit të parë
    collapsed_state, result_bit = measure(state)

    # Nxjerrim bitin e kubitit të parë (më domethënësin)
    # Për 2 kubitë, biti i parë është result_bit >> 1
    bit0 = (result_bit >> 1) & 1

    return bit0


# Deutsch-Jozsa
# 

# In[ ]:


def deutsch_jozsa(oracle_type='constant_0', n_qubits=3):
    """
    Implementon algoritmin Deutsch-Jozsa për n kubite.

    Args:
        oracle_type (str): 'constant_0' ose 'balanced'.
        n_qubits (int): Numri i kubitëve (përfshirë 1 kubit ndihmës).

    Returns:
        int: 0 nëse funksioni është konstant, 1 nëse është i balancuar.
    """
    state = initialize_state(n_qubits)

    # Hapi 1: X në kubitin e fundit (ndihmës)
    state = apply_single_qubit_gate(state, pauli_x(), target=n_qubits-1, n_qubits=n_qubits)

    # Hapi 2: Hadamard në të gjithë kubitët
    for i in range(n_qubits):
        state = apply_single_qubit_gate(state, hadamard(), target=i, n_qubits=n_qubits)

    # Hapi 3: Aplikojmë orakullin
    if oracle_type == 'balanced':
        # CNOT mbi të gjithë kubitët e kontrollit (0 deri n_qubits-2) dhe objektiv kubitin e fundit
        for i in range(n_qubits - 1):
            state = apply_cnot(state, control=i, target=n_qubits-1, n_qubits=n_qubits)

    # Hapi 4: Hadamard në të gjithë kubitët përveç të fundit
    for i in range(n_qubits - 1):
        state = apply_single_qubit_gate(state, hadamard(), target=i, n_qubits=n_qubits)

    # Hapi 5: Matja e të gjithë kubitëve
    collapsed_state, result_bits = measure(state)

    # Nëse të gjithë kubitët përveç të fundit janë 0, funksioni është konstant.
    # Kubiti ndihmës është më pak i rëndësishmi, kështu që vlerat 0 ose 1 për result_bits
    # tregojnë se bitët e tjerë janë 0.
    if result_bits <= 1:
        return 0  # Konstant
    else:
        return 1  # I balancuar



# Algoritmi i Grover-it (2-4 kubitë)

# In[ ]:


import numpy as np
import math
from gates import hadamard, pauli_x
from simulator import initialize_state, apply_single_qubit_gate, measure

def grover(n_qubits=2, marked_item=3):
    """
    Implementon algoritmin e kërkimit të Grover-it.
    """
    state = initialize_state(n_qubits)

    # Hadamard në të gjithë kubitët
    for i in range(n_qubits):
        state = apply_single_qubit_gate(state, hadamard(), target=i, n_qubits=n_qubits)

    # Numri i iteracioneve
    N = 2 ** n_qubits
    iterations = int(math.pi / 4 * math.sqrt(N))

    for _ in range(iterations):
        state = apply_oracle(state, marked_item, n_qubits)
        state = apply_diffusion(state, n_qubits)

    collapsed_state, result = measure(state)
    return collapsed_state, result

def apply_oracle(state, marked_item, n_qubits):
    """Inverton fazën e gjendjes së shënuar."""
    new_state = state.copy()
    new_state[marked_item] = -state[marked_item]
    return new_state

def apply_diffusion(state, n_qubits):
    """Operatori i difuzionit të Grover-it."""
    # Hadamard në të gjithë kubitët
    for i in range(n_qubits):
        state = apply_single_qubit_gate(state, hadamard(), target=i, n_qubits=n_qubits)

    # Përmbys fazën e gjendjes |00...0⟩
    state[0] = -state[0]

    # Hadamard përsëri
    for i in range(n_qubits):
        state = apply_single_qubit_gate(state, hadamard(), target=i, n_qubits=n_qubits)

    return state


# Teleportimi Kuantik

# In[ ]:


def teleportation():
    """
    Implementon teleportimin kuantik për 3 kubite.

    Protokolli:
    1. Përgatit gjendjen hyrëse |+> në kubitin 0 (Alice).
    2. Krijon çiftin Bell midis kubitëve 1 dhe 2 (1 është i Alice, 2 i Bobit).
    3. Alice kryen matje në bazën e Bell mbi kubitët 0 dhe 1.
    4. Sipas rezultatit të matjes, Bob aplikon korrigjime (X, Z) mbi kubitin 2.

    Në këtë implementim, matjet dhe korrigjimet realizohen nëpërmjet
    portave të kontrolluara, duke lejuar verifikimin e gjendjes përfundimtare
    pa e kolapsuar atë. Kjo qasje është ekuivalente me protokollin standard
    dhe lehtëson analizën matematikore të rezultatit.

    Returns:
        tuple: (gjendja_përfundimtare, rezultati_i_matjes)
    """
    n_qubits = 3
    state = initialize_state(n_qubits)

    # Përgatisim gjendjen hyrëse |+> në kubitin 0
    state = apply_single_qubit_gate(state, hadamard(), target=0, n_qubits=n_qubits)

    # Hapi 1: Krijimi i çiftit Bell midis kubitëve 1 dhe 2
    state = apply_single_qubit_gate(state, hadamard(), target=1, n_qubits=n_qubits)
    state = apply_cnot(state, control=1, target=2, n_qubits=n_qubits)

    # Hapi 2: Alice aplikon CNOT dhe Hadamard mbi kubitët e saj (0 dhe 1)
    state = apply_cnot(state, control=0, target=1, n_qubits=n_qubits)
    state = apply_single_qubit_gate(state, hadamard(), target=0, n_qubits=n_qubits)

    # Hapi 3: Korrigjimet e Bobit me porta të kontrolluara (ekuivalente me matjen)
    # CNOT i kontrolluar nga kubiti 1 mbi kubitin 2 (korrigjimi X)
    state = apply_cnot(state, control=1, target=2, n_qubits=n_qubits)

    # CZ midis kubitëve 0 dhe 2 (korrigjimi Z), implementuar direkt
    size = 2 ** n_qubits
    pos1 = n_qubits - 1 - 0  # kontrolli
    pos2 = n_qubits - 1 - 2  # objektivi
    for i in range(size):
        if ((i >> pos1) & 1) and ((i >> pos2) & 1):
            state[i] = -state[i]

    # Hapi 4: Matja përfundimtare (për të marrë rezultatin e matjes së Alice)
    collapsed_state, result = measure(state)
    return collapsed_state, result


# In[4]:


def teleportation_state():
    """
    Implementon teleportimin kuantik dhe kthen gjendjen PARA matjes.
    Kjo lejon verifikimin direkt të gjendjes së Bobit.
    """
    n_qubits = 3
    state = initialize_state(n_qubits)

    # Përgatisim gjendjen hyrëse |+> në kubitin 0
    state = apply_single_qubit_gate(state, hadamard(), target=0, n_qubits=n_qubits)

    # Krijimi i çiftit Bell midis kubitëve 1 dhe 2
    state = apply_single_qubit_gate(state, hadamard(), target=1, n_qubits=n_qubits)
    state = apply_cnot(state, control=1, target=2, n_qubits=n_qubits)

    # Operacionet e Alice
    state = apply_cnot(state, control=0, target=1, n_qubits=n_qubits)
    state = apply_single_qubit_gate(state, hadamard(), target=0, n_qubits=n_qubits)

    # Korrigjimet e Bobit (pa matje)
    state = apply_cnot(state, control=1, target=2, n_qubits=n_qubits) # X
    # CZ e implementuar direkt
    size = 2 ** n_qubits
    pos1 = n_qubits - 1 - 0
    pos2 = n_qubits - 1 - 2
    for i in range(size):
        if ((i >> pos1) & 1) and ((i >> pos2) & 1):
            state[i] = -state[i]

    return state # <--- Kthehet gjendja PARA matjes

