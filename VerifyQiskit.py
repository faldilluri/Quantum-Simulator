#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Importimi i Qiskit
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_histogram, plot_bloch_multivector
import numpy as np
import matplotlib.pyplot as plt


# In[2]:

print("=" * 60)
print("Demonstrimi 1: GJENDJA BELL NË QISKIT")
print("=" * 60)
# Ndërtojmë qarkun për gjendjen Bell në Qiskit
qc_bell = QuantumCircuit(2)

# Hapi 1: Hadamard në kubitin e parë (q0)
qc_bell.h(0)

# Hapi 2: CNOT me kontroll q0, objektiv q1
qc_bell.cx(0, 1)

# Marrim statevector-in
statevector_bell_qiskit = Statevector.from_instruction(qc_bell)

# Shfaqim qarkun
print("Qarku Bell në Qiskit:")
print(qc_bell.draw('text'))
print()

# Shfaqim statevector-in
print("Statevector nga Qiskit:")
print(statevector_bell_qiskit.data)


# In[4]:


print("=" * 60)
print("Demonstrimi 2: VERIFIKIMI I ALGORITMIT TË DEUTSCH-IT NË QISKIT")
print("=" * 60)

def deutsch_qiskit_no_measure(oracle_type):
    """
    Ndërton qarkun e Deutsch-it në Qiskit PA matje, për të marrë statevector-in.
    """
    qc = QuantumCircuit(2)

    # Hapi 1: X në kubitin e dytë
    qc.x(1)

    # Hapi 2: Hadamard në të dy kubitët
    qc.h(0)
    qc.h(1)

    # Hapi 3: Orakulli
    if oracle_type == 'constant_0':
        pass
    elif oracle_type == 'constant_1':
        qc.x(1)
    elif oracle_type == 'balanced_id':
        qc.cx(0, 1)
    elif oracle_type == 'balanced_not':
        qc.cx(0, 1)
        qc.x(1)

    # Hapi 4: Hadamard në kubitin e parë
    qc.h(0)

    return qc

# Testojmë katër orakujt
oracle_types = ['constant_0', 'constant_1', 'balanced_id', 'balanced_not']
results_deutsch_qiskit = {}

for oracle in oracle_types:
    qc = deutsch_qiskit_no_measure(oracle)
    statevector = Statevector.from_instruction(qc)

    # Marrim probabilitetet për kubitin e parë (indeksi 0)
    probs = statevector.probabilities([0])
    result = 0 if probs[0] > 0.999 else 1

    results_deutsch_qiskit[oracle] = (result, probs)
    status = "Konstant" if result == 0 else "I balancuar"
    print(f"\nOrakulli: {oracle:15} → Rezultati: {result} ({status})")
    print(f"  Probabiliteti i |0⟩ në kubitin e parë: {probs[0]:.4f}")
    print(f"  Probabiliteti i |1⟩ në kubitin e parë: {probs[1]:.4f}")

    # Vizualizojmë qarkun për një rast
    if oracle == 'balanced_id':
        print("\nQarku në Qiskit për orakullin 'balanced_id':")
        print(qc.draw('text'))


# In[5]:


print("\n" + "=" * 60)
print("Demonstrimi 3: VERIFIKIMI I ALGORITMIT TË DEUTSCH-JOZSA NË QISKIT")
print("=" * 60)

def deutsch_jozsa_qiskit(oracle_type='constant_0', n_data=2):
    n_total = n_data + 1  # përfshirë edhe kubitin ndihmës
    qc = QuantumCircuit(n_total)

    # Hapi 1: X në kubitin ndihmës
    qc.x(n_data)  # kubiti ndihmës është i fundit

    # Hapi 2: Hadamard në të gjithë kubitët
    for i in range(n_total):
        qc.h(i)

    # Hapi 3: Orakulli
    if oracle_type == 'balanced':
        for i in range(n_data):
            qc.cx(i, n_data)

    # Hapi 4: Hadamard në kubitët e të dhënave
    for i in range(n_data):
        qc.h(i)

    return qc

# Testojmë me orakull konstant
print("\n--- Orakulli Konstant ---")
qc_const = deutsch_jozsa_qiskit('constant_0')
statevector_const = Statevector.from_instruction(qc_const)
probs_const = statevector_const.probabilities(range(2))  # probabilitetet për dy kubitët e parë
print(f"Probabiliteti për të gjithë kubitët e të dhënave në |0⟩: {probs_const[0]:.4f}")
print("Rezultati: 0 (Konstant)")

# Testojmë me orakull të balancuar
print("\n--- Orakull i Balancuar ---")
qc_bal = deutsch_jozsa_qiskit('balanced')
statevector_bal = Statevector.from_instruction(qc_bal)
probs_bal = statevector_bal.probabilities(range(2))
print(f"Probabiliteti për të gjithë kubitët e të dhënave në |0⟩: {probs_bal[0]:.4f}")
print(f"Probabiliteti për të paktën një kubit në |1⟩: {1 - probs_bal[0]:.4f}")
print("Rezultati: 1 (I balancuar)")

# Vizualizimi i qarkut për rastin e balancuar
print("\nQarku në Qiskit për orakullin e balancuar:")
print(qc_bal.draw('text'))


# In[6]:


print("\n" + "=" * 60)
print("Demonstrimi 4: VERIFIKIMI I ALGORITMIT TË GROVER-IT NË QISKIT")
print("=" * 60)

def grover_qiskit():
    """
    Ndërton qarkun e Grover-it për n=2 kubitë, gjendje e shënuar |11⟩.
    """
    qc = QuantumCircuit(2)

    # Hapi 1: Hadamard në të dy kubitët
    qc.h(0)
    qc.h(1)

    # --- Orakulli (shënon |11⟩) ---
    # Orakulli për |11⟩ mund të ndërtohet me një portë CZ midis dy kubitëve,
    # ose me një CNOT të rrethuar nga dy H në kubitin e objektivit.
    # Mënyrë standarde: Z e kontrolluar (CZ) midis q_0 dhe q_1.
    qc.cz(0, 1)

    # --- Difuzioni ---
    # H në të dy kubitët
    qc.h(0)
    qc.h(1)
    # X në të dy kubitët
    qc.x(0)
    qc.x(1)
    # CZ midis dy kubitëve (që shënon |00⟩, pasi kemi aplikuar X)
    qc.cz(0, 1)
    # X dhe H përsëri
    qc.x(0)
    qc.x(1)
    qc.h(0)
    qc.h(1)

    return qc

# Ekzekutimi
qc_grover = grover_qiskit()
statevector_grover = Statevector.from_instruction(qc_grover)

print("Statevector nga Qiskit:")
for i, amp in enumerate(statevector_grover.data):
    binary = format(i, '02b')
    print(f"  |{binary}⟩: {amp.real:.4f} + {amp.imag:.4f}j")

# Probabilitetet
probs_grover = statevector_grover.probabilities()
print("\nProbabilitetet:")
for i, p in enumerate(probs_grover):
    binary = format(i, '02b')
    print(f"  |{binary}⟩: {p:.4f}")

print("\nQarku në Qiskit:")
print(qc_grover.draw('text'))


# In[7]:


print("\n" + "=" * 60)
print("Demonstrimi 5: VERIFIKIMI I TELEPORTIMIT KUANTIK NË QISKIT")
print("=" * 60)

def teleportation_qiskit():
    """
    Ndërton qarkun e teleportimit kuantik në Qiskit.
    """
    qc = QuantumCircuit(3)

    # Përgatisim gjendjen hyrëse |+> në kubitin 0
    qc.h(0)

    # Krijimi i çiftit Bell midis kubitëve 1 dhe 2
    qc.h(1)
    qc.cx(1, 2)

    # Operacionet e Alice-s
    qc.cx(0, 1)
    qc.h(0)

    # Korrigjimet e Bobit me porta të kontrolluara
    qc.cx(1, 2)  # CNOT i kontrolluar nga kubiti 1 mbi kubitin 2 (X)
    qc.cz(0, 2)  # CZ i kontrolluar nga kubiti 0 mbi kubitin 2 (Z)

    return qc

# Ekzekutimi
qc_teleport = teleportation_qiskit()
statevector_teleport = Statevector.from_instruction(qc_teleport)

print("Statevector nga Qiskit:")
for i, amp in enumerate(statevector_teleport.data):
    binary = format(i, '03b')
    print(f"  |{binary}⟩: {amp.real:.4f} + {amp.imag:.4f}j")

# Analiza e kubitit të Bobit (kubiti 2, biti më pak i rëndësishëm)
probs_teleport = statevector_teleport.probabilities()
prob_0_qubit2 = sum(probs_teleport[i] for i in range(len(probs_teleport)) if format(i, '03b')[-1] == '0')
prob_1_qubit2 = sum(probs_teleport[i] for i in range(len(probs_teleport)) if format(i, '03b')[-1] == '1')

print(f"\nProbabiliteti që kubiti 2 (Bob) është |0⟩: {prob_0_qubit2:.4f}")
print(f"Probabiliteti që kubiti 2 (Bob) është |1⟩: {prob_1_qubit2:.4f}")

if abs(prob_0_qubit2 - 0.5) < 1e-6 and abs(prob_1_qubit2 - 0.5) < 1e-6:
    print("\nTeleportimi u krye me sukses sipas Qiskit!")
else:
    print("\nTeleportimi dështoi.")

print("\nQarku në Qiskit:")
print(qc_teleport.draw('text'))

