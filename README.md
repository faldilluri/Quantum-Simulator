# Quantum Circuit Simulator

A basic quantum circuit simulator implemented entirely in Python, with a focus on educational purposes and understanding fundamental quantum computing mechanisms.

## Overview

This project implements a lightweight quantum simulator using the state-vector simulation method. It includes:

- **Single-qubit gates**: Pauli (X, Y, Z), Hadamard (H), Phase (S, T), rotation gates (Ry, Rz)
- **Multi-qubit gates**: CNOT, SWAP, CZ
- **Qubit-wise multiplication** for efficient single-qubit gate application
- **Optimal gate decomposition** according to Vatan & Williams (2004)
- **Five fundamental quantum algorithms**:
  - Bell State Generation
  - Deutsch's Algorithm
  - Deutsch-Jozsa Algorithm
  - Grover's Search Algorithm
  - Quantum Teleportation
- **Visualization tools**: Probability histograms, circuit diagrams, Bloch sphere
- **Verification against IBM's Qiskit** with quantitative metrics (fidelity, amplitude error, probability MSE)

## Requirements

- Python 3.14.2 or higher
- NumPy >= 1.26.0
- Matplotlib >= 3.8.0
- Qiskit >= 1.0.0 (for verification and Bloch sphere visualization)

## Installation

```bash
# Clone the repository
git clone https://github.com/SaimirC/Quantum-Simulator.git
cd Quantum-Simulator

# Create and activate a virtual environment (recommended)
python -m venv quantum_env
source quantum_env/bin/activate   # On Windows: quantum_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
Usage
Run all demonstrations
bash
python main.py
Run verification against Qiskit
bash
python VerifyQiskit.py
Example: Bell State Generation
python
from algorithms import bell_state
from visualization import plot_probabilities

state = bell_state()
plot_probabilities(state, title="Bell State |Φ⁺⟩")
Project Structure
text
quantum_simulator/
├── gates.py              # Quantum gate library
├── simulator.py          # Simulation engine (state vector, gate application, measurement)
├── algorithms.py         # Implementation of five quantum algorithms
├── visualization.py      # Visualization tools (histograms, circuits, Bloch sphere)
├── VerifyQiskit.py       # Verification against IBM's Qiskit
├── main.py               # Main execution script
├── requirements.txt      # Python dependencies
└── README.md             # This file
Verification Results
The simulator was verified against IBM's Qiskit platform. All algorithms achieved:

Fidelity: 1.000000000000000 (perfect agreement)

Amplitude Error: < 1e-15

Probability MSE: < 1e-30

License
This project is open-source and available for educational and research purposes.

Author
Saimir Çiraku – Master's student at "Aleksandër Moisiu" University, Durrës

Email: sciraku@gmail.com

GitHub: SaimirC

Acknowledgments
Supervisor: Dr. [Emri i drejtuesit]

Inspired by the tutorial of McGuffin, Robert, and Ikeda (2025)

Optimal gate decomposition based on Vatan & Williams (2004)

References
Nielsen, M. A., & Chuang, I. L. (2010). Quantum Computation and Quantum Information.

Vatan, F., & Williams, C. (2004). Optimal quantum circuits for general two-qubit gates.

McGuffin, M. J., Robert, J.-M., & Ikeda, K. (2025). How to Write a Simulator for Quantum Circuits from Scratch.