#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt

# Për sferën e Blokut do të përdorim Qiskit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector, plot_bloch_vector


# ky dokument permban funksionet per 
# 1.Shfaqjen e histogramave të probabiliteteve.
# 2.Krahasimi i histogramave (Para/Pas)
# 3.Vizatimin e diagramës së qarkut (telat dhe portat) me Matplotlib.
# 
# 4.Vizatimin e sferës së Blokut.

# In[ ]:


def plot_probabilities(state, title="Probabilitetet e Gjendjes"):
    """
    Shfaq histogramën e probabiliteteve për secilën gjendje bazë.

    Args:
        state (numpy.ndarray): Vektori i gjendjes kuantike.
        title (str): Titulli i grafikut.
    """
    n_qubits = int(np.log2(len(state)))
    probs = np.abs(state) ** 2

    # Krijojmë etiketat për secilën gjendje bazë
    labels = []
    for i in range(len(state)):
        # Konvertojmë indeksin në string binar (p.sh., 2 -> '10')
        binary = format(i, f'0{n_qubits}b')
        labels.append(f'|{binary}⟩')

    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, probs, color='#4299E1', edgecolor='#2B6CB0', linewidth=1.2)

    # Shtojmë vlerat mbi shtyllat
    for bar, prob in zip(bars, probs):
        if prob > 0.01:
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                     f'{prob:.3f}', ha='center', va='bottom', fontsize=10)

    plt.title(title, fontsize=14, fontweight='bold')
    plt.ylabel('Probabiliteti', fontsize=12)
    plt.xlabel('Gjendjet Bazë', fontsize=12)
    plt.ylim(0, 1.05)
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.show()


# In[ ]:


def plot_probabilities_comparison(state_before, state_after, 
                                   title_before="Para", title_after="Pas",
                                   main_title="Krahasimi i Probabiliteteve"):
    """
    Shfaq dy histograma krah për krah për të krahasuar gjendjen para dhe pas një operacioni.

    Args:
        state_before (numpy.ndarray): Vektori i gjendjes para operacionit.
        state_after (numpy.ndarray): Vektori i gjendjes pas operacionit.
        title_before (str): Titulli për histogramën e parë.
        title_after (str): Titulli për histogramën e dytë.
        main_title (str): Titulli kryesor.
    """
    n_qubits = int(np.log2(len(state_before)))
    probs_before = np.abs(state_before) ** 2
    probs_after = np.abs(state_after) ** 2

    labels = [f'|{format(i, f"0{n_qubits}b")}⟩' for i in range(len(state_before))]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.bar(labels, probs_before, color='#48BB78', edgecolor='#38A169', linewidth=1.2)
    ax1.set_title(title_before, fontsize=12, fontweight='bold')
    ax1.set_ylabel('Probabiliteti')
    ax1.set_ylim(0, 1.05)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')

    ax2.bar(labels, probs_after, color='#4299E1', edgecolor='#2B6CB0', linewidth=1.2)
    ax2.set_title(title_after, fontsize=12, fontweight='bold')
    ax2.set_ylim(0, 1.05)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')

    fig.suptitle(main_title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()


# In[ ]:


def draw_circuit(gate_list, n_qubits, title="Diagrama e Qarkut Kuantik"):
    """
    Vizaton një diagramë qarku kuantik.

    Args:
        gate_list (list): Listë me tuplet (gate_name, target_qubit, [control_qubit]).
            Për portat me një kubit: (gate_name, target, None)
            Për portat me dy kubitë: (gate_name, target, control)
            Për matjen: ('M', target, None)
        n_qubits (int): Numri i kubitëve (linjave).
        title (str): Titulli i diagramës.
    """
    num_gates = len(gate_list)
    fig, ax = plt.subplots(figsize=(num_gates * 1.5 + 1, n_qubits * 1.2))

    # Vizatojmë linjat horizontale për çdo kubit
    line_spacing = 1.0
    for i in range(n_qubits):
        y = n_qubits - 1 - i
        ax.hlines(y=y, xmin=0.5, xmax=num_gates + 0.5, 
                  color='black', linewidth=1.2, zorder=1)
        # Etiketa e kubitit
        ax.text(-0.3, y, f'q{i}', ha='right', va='center', fontsize=12, fontweight='bold')

    # Vizatojmë portat
    for col, gate_info in enumerate(gate_list):
        x = col + 1.0

        # ---  Matja ---
        if len(gate_info) >= 2 and gate_info[0] == 'M':
            target = gate_info[1]
            y = n_qubits - 1 - target

            # Vizatojmë një kuti matjeje me sfond të kuq (lightcoral)
            bbox_props = dict(boxstyle='round,pad=0.3', facecolor='lightcoral', 
                             edgecolor='black', linewidth=1.5, alpha=0.9)
            ax.text(x, y, 'M', ha='center', va='center', fontsize=10, 
                   fontweight='bold', bbox=bbox_props, zorder=5)
            continue  # Kalo në portën tjetër

        # --- Rasti i portave me dy kubitë ---
        if len(gate_info) == 3 and gate_info[2] is not None:
            # Portë me dy kubitë
            gate_name, target, control = gate_info
            y_target = n_qubits - 1 - target
            y_control = n_qubits - 1 - control

            # Vizatojmë vijën lidhëse
            ax.plot([x, x], [min(y_target, y_control), max(y_target, y_control)], 
                   color='black', linewidth=1.2, zorder=1)

            # Vizatojmë pikën e kontrollit
            ax.scatter(x, y_control, s=150, c='black', zorder=3)

            # Vizatojmë simbolin ⊕ për objektivin
            circle = plt.Circle((x, y_target), 0.3, edgecolor='black', 
                               facecolor='white', linewidth=1.5, zorder=3)
            ax.add_patch(circle)
            ax.plot([x-0.18, x+0.18], [y_target, y_target], color='black', linewidth=1.2, zorder=4)
            ax.plot([x, x], [y_target-0.18, y_target+0.18], color='black', linewidth=1.2, zorder=4)

            # Emri i portës
            ax.text(x + 0.35, y_target, gate_name, ha='left', va='center', fontsize=9, fontstyle='italic')

        # --- Rasti i portave me një kubit ---
        else:
            gate_name = gate_info[0]
            target = gate_info[1]
            y = n_qubits - 1 - target

            # Vizatojmë kutinë e portës
            bbox_props = dict(boxstyle='round,pad=0.3', facecolor='#BEE3F8', 
                             edgecolor='#2B6CB0', linewidth=1.5, alpha=0.9)
            ax.text(x, y, gate_name, ha='center', va='center', fontsize=10, 
                   fontweight='bold', bbox=bbox_props, zorder=5)

    ax.set_xlim(0, num_gates + 1.5)
    ax.set_ylim(-0.5, n_qubits - 0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    ax.set_title(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()


# In[ ]:


def plot_bloch_sphere(state, title="Sfera e Blokut"):
    """
    Vizaton sferën e Blokut për një gjendje kuantike.

    Args:
        state (numpy.ndarray): Vektori i gjendjes kuantike.
        title (str): Titulli i figurës.
    """
    if len(state) == 2:
        # Për një kubit të vetëm
        sv = Statevector(state)
        plot_bloch_multivector(sv, title=title)
    elif len(state) == 4:
        # Për dy kubitë, shfaq sferat e Blokut për secilin
        sv = Statevector(state)
        plot_bloch_multivector(sv, title=title)
    else:
        print("Sfera e Blokut mbështetet vetëm për 1 ose 2 kubitë.")


# In[6]:


from qiskit import QuantumCircuit

def draw_circuit_qiskit(gate_list, n_qubits, title="Diagrama e Qarkut (Qiskit)"):
    """
    Vizaton një diagramë qarku kuantik duke përdorur Qiskit.

    Args:
        gate_list (list): Listë me tuplet (gate_name, target, [control]).
        n_qubits (int): Numri i kubitëve.
        title (str): Titulli i diagramës.

    Returns:
        Figura e vizatuar nga Qiskit.
    """
    qc = QuantumCircuit(n_qubits)

    for gate_info in gate_list:
        gate_name = gate_info[0]
        target = gate_info[1]

        if gate_name == 'H':
            qc.h(target)
        elif gate_name == 'X':
            qc.x(target)
        elif gate_name == 'Y':
            qc.y(target)
        elif gate_name == 'Z':
            qc.z(target)
        elif gate_name == 'S':
            qc.s(target)
        elif gate_name == 'T':
            qc.t(target)
        elif gate_name == 'CNOT' and len(gate_info) == 3:
            control = gate_info[2]
            qc.cx(control, target)
        elif gate_name == 'SWAP' and len(gate_info) == 3:
            qubit2 = gate_info[2]
            qc.swap(target, qubit2)
        elif gate_name == 'Matje':
            qc.measure(target, target)

    return qc.draw('mpl', title=title)

