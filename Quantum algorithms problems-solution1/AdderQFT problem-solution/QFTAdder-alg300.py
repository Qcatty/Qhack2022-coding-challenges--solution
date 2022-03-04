import sys
from pennylane import numpy as np
import pennylane as qml


def qfunc_adder(m, wires):
    """Quantum function capable of adding m units to a basic state given as input.
    Args:
        - m (int): units to add.
        - wires (list(int)): list of wires in which the function will be executed on.
    """

    qml.QFT(wires=wires)

    # QHACK #
    n = len(wires)
    for i in range(n, 0, -1):
        for j,bit in enumerate(binary_list(m,n)):
            l=n-j
            if n - 1 >= l - 1 and i-l+1>=0:
                if bit==1:
                    phi = 2 * np.pi / np.power(2, i-l+1)
                    qml.PhaseShift(phi, wires=wires[i-1])
    # QHACK #

    qml.QFT(wires=wires).inv()
    
def binary_list(m, n):
    ls = []
    b=[]
    a=[]
    # QHACK #
    for i in bin(m):
        if i!='b':
            b.append(int(i))
    b=b[1:]
    if n>len(b):
        for i in range(n-len(b)):
            a.append(0)
    ls=a+b
    # QHACK #
    return ls

if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(",")
    m = int(inputs[0])
    n_wires = int(inputs[1])
    wires = range(n_wires)

    dev = qml.device("default.qubit", wires=wires, shots=1)

    @qml.qnode(dev)
    def test_circuit():
        # Input:  |2^{N-1}>
        qml.PauliX(wires=0)

        qfunc_adder(m, wires)
        return qml.sample()

    output = test_circuit()
    print(*output, sep=",")