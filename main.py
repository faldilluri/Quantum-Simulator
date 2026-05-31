#!/usr/bin/env python
# coding: utf-8

# In[7]:


import numpy as np
import sys
import os
sys.path.append(os.getcwd())

from gates import hadamard, pauli_x, pauli_z, pauli_y, cnot, swap, cz, phase_s, phase_t, ry_gate, rz_gate

from simulator import initialize_state, apply_single_qubit_gate, apply_cnot, apply_two_qubit_gate, measure, get_probabilities
from algorithms import bell_state, deutsch, deutsch_jozsa, grover, teleportation_state, teleportation
from visualization import plot_probabilities, plot_probabilities_comparison, draw_circuit, plot_bloch_sphere


# Demonstrimi i Gjendjes Bell

# In[ ]:


from algorithms import bell_state

print("=" * 50)
print("DEMONSTRIMI 1: GJENDJA BELL")
print("=" * 50)

# Ndërtojmë dhe ekzekutojmë gjendjen Bell
state_bell = bell_state()

# Shfaqim vektorin e gjendjes
print("\nVektori i gjendjes |Φ⁺⟩:")
for i, amp in enumerate(state_bell):
    binary = format(i, '02b')
    print(f"  |{binary}⟩: {amp.real:.4f} + {amp.imag:.4f}i")

# Vizualizojmë qarkun
print("\nQarku i Gjendjes Bell:")
draw_circuit([
    ('H', 0, None),
    ('CNOT', 1, 0),
    ('M', 0, None),
    ('M', 1, None)
], n_qubits=2, title="Qarku i plotë për Gjendjen Bell |Φ⁺⟩ me matje")

# Shfaqim probabilitetet
plot_probabilities(state_bell, title="Gjendja Bell |Φ⁺⟩ - Probabilitetet e Matjes")

# Matja
collapsed, result = measure(state_bell.copy())
print(f"\nMatja: u mor gjendja |{format(result, '02b')}⟩")


# In[ ]:


print("=" * 50)
print("DEMONSTRIMI 2: ALGORITMI I DEUTSCH-IT")
print("=" * 50)

print("\nTest me orakull konstant (constant_0):")
result = deutsch(oracle_type='constant_0')
print(f"  Rezultati: {result} (0 = konstant, 1 = i balancuar)")

print("\nTest me orakull konstant (constant_1):")
result = deutsch(oracle_type='constant_1')
print(f"  Rezultati: {result} (0 = konstant, 1 = i balancuar)")

print("\nTest me orakull të balancuar (balanced_id):")
result = deutsch(oracle_type='balanced_id')
print(f"  Rezultati: {result} (0 = konstant, 1 = i balancuar)")

print("\nTest me orakull të balancuar (balanced_not):")
result = deutsch(oracle_type='balanced_not')
print(f"  Rezultati: {result} (0 = konstant, 1 = i balancuar)")

# Vizualizojmë qarkun për një rast (p.sh., balanced_id)
print("\nQarku i Deutsch-it për orakullin 'balanced_id':")
draw_circuit([
    ('X', 1, None),
    ('H', 0, None),
    ('H', 1, None),
    ('CNOT', 1, 0),
    ('H', 0, None),
    ('M', 0, None)
], n_qubits=2, title="Qarku i Deutsch-it (orakull i balancuar: id)")


# Demonstrimi i Algoritmit Deutsch-Jozsa

# In[ ]:


print("\n" + "=" * 50)
print("DEMONSTRIMI 3: ALGORITMI DEUTSCH-JOZSA")
print("=" * 50)

# Testojmë me orakull konstant
print("\nTest me orakull konstant (3 kubite):")
result = deutsch_jozsa(oracle_type='constant_0', n_qubits=3)
print(f"  Rezultati: {result} (0 = konstant, 1 = i balancuar)")

# Testojmë me orakull të balancuar
print("\nTest me orakull të balancuar (3 kubite):")
result = deutsch_jozsa(oracle_type='balanced', n_qubits=3)
print(f"  Rezultati: {result} (0 = konstant, 1 = i balancuar)")

# Vizualizojmë qarkun
print("\nQarku i Deutsch-Jozsa (3 kubite):")
draw_circuit([
    ('X', 2, None),
    ('H', 0, None),
    ('H', 1, None),
    ('H', 2, None),
    ('CNOT', 2, 0),
    ('CNOT', 2, 1),
    ('H', 0, None),
    ('H', 1, None),
    ('M', 0, None),
    ('M', 1, None)
], n_qubits=3, title="Qarku i Deutsch-Jozsa (3 kubite, orakull i balancuar)")


# 

# Demonstrimi i Algoritmit të Grover-it

# In[ ]:


print("\n" + "=" * 50)
print("DEMONSTRIMI 4: ALGORITMI I GROVER-IT")
print("=" * 50)

print("\nKërkim për gjendjen |11⟩ (indeksi 3) me 2 kubite:")
collapsed, result = grover(n_qubits=2, marked_item=3)
print(f"  Gjendja e gjetur: |{format(result, '02b')}⟩")

plot_probabilities(collapsed, title="Grover - Probabilitetet Pas Kërkimit")

print("\nQarku i Grover-it (2 kubite):")
draw_circuit([
    ('H', 0, None),
    ('H', 1, None),
    ('Orakull', 0, None),
    ('Difuzion', 1, None)
], n_qubits=2, title="Qarku i Grover-it (2 kubite)")


#  Demonstrimi i Teleportimit Kuantik

# In[ ]:


print("\n" + "=" * 50)
print("DEMONSTRIMI 5: TELEPORTIMI KUANTIK")
print("=" * 50)

# PJESA 1: Demonstrimi i plotë (me matje)
print("\n--- Ekzekutimi i plotë (me matje) ---")
collapsed, alice_result = teleportation()
print(f"Rezultati i matjes përfundimtare (të tre kubitët): |{format(alice_result, '03b')}⟩")
print("Gjendja e kolapsuar pas matjes:")
print(collapsed)

# PJESA 2: Vërtetimi matematikor (pa matje)
print("\n--- Vërtetimi i teleportimit (pa matje) ---")
state_before_measure = teleportation_state()
probs = get_probabilities(state_before_measure)

print("Probabilitetet e gjendjes përfundimtare (përpara matjes):")
for i, p in enumerate(probs):
    if p > 0.001:
        print(f"  |{format(i, '03b')}⟩: {p:.4f}")

prob_0_qubit2 = sum(probs[i] for i in range(len(probs)) if format(i, '03b')[-1] == '0')
prob_1_qubit2 = sum(probs[i] for i in range(len(probs)) if format(i, '03b')[-1] == '1')
print(f"\nProbabiliteti që kubiti 2 (Bob) është |0⟩: {prob_0_qubit2:.4f}")
print(f"Probabiliteti që kubiti 2 (Bob) është |1⟩: {prob_1_qubit2:.4f}")

if abs(prob_0_qubit2 - 0.5) < 1e-6 and abs(prob_1_qubit2 - 0.5) < 1e-6:
    print("Teleportimi u krye me sukses! Gjendja |+⟩ u transferua te Bob.")
else:
    print("Teleportimi dështoi.")

# PJESA 3: Vizualizimi i qarkut
print("\nQarku i Teleportimit Kuantik:")
draw_circuit([
    ('H', 0, None),      # Gjendja |+>
    ('H', 1, None),      # Krijimi i çiftit Bell
    ('CNOT', 2, 1),
    ('CNOT', 1, 0),      # Operacionet e Alice
    ('H', 0, None),
    ('M', 0, None),      # Matjet e Alice
    ('M', 1, None)
], n_qubits=3, title="Qarku i Teleportimit Kuantik (pa korrigjimet e Bobit)")


# Demonstrim i Portave të Veçanta
# 

# In[10]:


from simulator import initialize_state, apply_single_qubit_gate
from gates import hadamard, rz_gate
from visualization import plot_probabilities_comparison

print("\n" + "=" * 50)
print("DEMONSTRIMI SHTESË: EFEKTI I PORTAVE TË VEÇANTA")
print("=" * 50)

# Inicializojmë |0⟩
state = initialize_state(1)
print("\nGjendja fillestare |0⟩:", state)

# Aplikojmë Hadamard
state_h = apply_single_qubit_gate(state.copy(), hadamard(), target=0, n_qubits=1)
print("\nPas Hadamard (|+⟩):", state_h)

# Krahasojmë probabilitetet
plot_probabilities_comparison(
    state, state_h,
    title_before="|0⟩", title_after="|+⟩",
    main_title="Efekti i Portës Hadamard mbi |0⟩"
)

# Aplikojmë Rz(π/2) mbi |+⟩
state_plus = apply_single_qubit_gate(state.copy(), hadamard(), target=0, n_qubits=1)
state_i = apply_single_qubit_gate(state_plus.copy(), rz_gate(np.pi/2), target=0, n_qubits=1)
print("\nPas Rz(π/2) mbi |+⟩ (|i⟩):", state_i)

plot_probabilities_comparison(
    state_plus, state_i,
    title_before="|+⟩", title_after="|i⟩",
    main_title="Efekti i Rrotullimit Rz(π/2) mbi |+⟩"
)


# 7: Demonstrim Shtesë i Portave të Veçanta

# In[9]:


print("\n" + "=" * 50)
print("DEMONSTRIMI SHTESË: EFEKTI I PORTAVE TË VEÇANTA")
print("=" * 50)

state = initialize_state(1)
print("\nGjendja fillestare |0⟩:", state)

state_h = apply_single_qubit_gate(state.copy(), hadamard(), target=0, n_qubits=1)
print("\nPas Hadamard (|+⟩):", state_h)

plot_probabilities_comparison(
    state, state_h,
    title_before="|0⟩", title_after="|+⟩",
    main_title="Efekti i Portës Hadamard"
)

state_plus = apply_single_qubit_gate(state.copy(), hadamard(), target=0, n_qubits=1)
state_i = apply_single_qubit_gate(state_plus.copy(), rz_gate(np.pi/2), target=0, n_qubits=1)
print("\nPas Rz(π/2) mbi |+⟩ (|i⟩):", state_i)

plot_probabilities_comparison(
    state_plus, state_i,
    title_before="|+⟩", title_after="|i⟩",
    main_title="Efekti i Rrotullimit Rz(π/2)"
)

