import sys
import pennylane as qml
from pennylane import numpy as np
from pennylane import hf


def ground_state_VQE(H):
    """Perform VQE to find the ground state of the H2 Hamiltonian.

    Args:
        - H (qml.Hamiltonian): The Hydrogen (H2) Hamiltonian

    Returns:
        - (float): The ground state energy
        - (np.ndarray): The ground state calculated through your optimization routine
    """

    # QHACK #
    qubits = 4
    dev = qml.device("default.qubit", wires=qubits)
    hf_state = np.array([1, 1, 0, 0])

    def circuit(param, wires):
        qml.BasisState(hf_state, wires=wires)
        qml.DoubleExcitation(param, wires=[0, 1, 2, 3])

    @qml.qnode(dev)
    def cost_fn(param):
        circuit(param, wires=range(qubits))
        return qml.expval(H)

    @qml.qnode(dev)
    def ground_state(param):
        circuit(param, wires=range(qubits))
        return qml.state()

    opt = qml.AdamOptimizer(stepsize=0.4)
    theta = np.array(0.0, requires_grad=True)
    max_iterations = 100

    for n in range(max_iterations):
        theta = opt.step(cost_fn, theta)

    E0 = cost_fn(theta) 
    state = ground_state(theta)
    return (E0,state)
    # QHACK #


def create_H1(ground_state, beta, H):
    """Create the H1 matrix, then use `qml.Hermitian(matrix)` to return an observable-form of H1.

    Args:
        - ground_state (np.ndarray): from the ground state VQE calculation
        - beta (float): the prefactor for the ground state projector term
        - H (qml.Hamiltonian): the result of hf.generate_hamiltonian(mol)()

    Returns:
        - (qml.Observable): The result of qml.Hermitian(H1_matrix)
    """

    # QHACK #
    add_term = np.reshape(beta*np.kron(ground_state,ground_state),(len(ground_state),len(ground_state)))
    obs, coeff = qml.utils.decompose_hamiltonian(add_term)
    return H+qml.Hamiltonian(obs, coeff)
    # QHACK #


def excited_state_VQE(H1):
    """Perform VQE using the "excited state" Hamiltonian.

    Args:
        - H1 (qml.Observable): result of create_H1

    Returns:
        - (float): The excited state energy
    """

    # QHACK #
    qubits = 4
    dev = qml.device("default.qubit", wires=qubits)
    hf_state = np.array([0, 1, 0 , 1])

    def circuit(param, wires):
        qml.BasisState(hf_state, wires=wires)
        qml.DoubleExcitation(param, wires=[0, 1, 2, 3]) 

    @qml.qnode(dev)
    def cost_fn(param):
        circuit(param, wires=range(qubits))
        return qml.expval(H1)

    opt = qml.AdamOptimizer(stepsize=0.4)
    theta = np.array(0.0, requires_grad=True)
    max_iterations = 100

    for n in range(max_iterations):
        theta = opt.step(cost_fn, theta)

    E1 = cost_fn(theta) 
    return E1
    # QHACK #


if __name__ == "__main__":
    coord = float(sys.stdin.read())
    symbols = ["H", "H"]
    geometry = np.array([[0.0, 0.0, -coord], [0.0, 0.0, coord]], requires_grad=False)
    mol = hf.Molecule(symbols, geometry)

    H = hf.generate_hamiltonian(mol)()
    E0, ground_state = ground_state_VQE(H)

    beta = 15.0
    H1 = create_H1(ground_state, beta, H)
    E1 = excited_state_VQE(H1)

    answer = [np.real(E0), E1]
    print(*answer, sep=",")
