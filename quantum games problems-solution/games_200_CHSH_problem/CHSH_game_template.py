#! /usr/bin/python3

import sys
import pennylane as qml
from pennylane import numpy as np


dev = qml.device("default.qubit", wires=2)


def prepare_entangled(alpha, beta):
    """Construct a circuit that prepares the (not necessarily maximally) entangled state in terms of alpha and beta
    Do not forget to normalize.

    Args:
        - alpha (float): real coefficient of |00>
        - beta (float): real coefficient of |11>
    """

    # QHACK #
    norm_beta = beta/np.sqrt(alpha**2+beta**2)
    qml.RY(2*np.arcsin(norm_beta),wires=0)
    qml.CNOT(wires=[0,1])
    # QHACK #

@qml.qnode(dev)
def chsh_circuit(theta_A0, theta_A1, theta_B0, theta_B1, x, y, alpha, beta):
    """Construct a circuit that implements Alice's and Bob's measurements in the rotated bases

    Args:
        - theta_A0 (float): angle that Alice chooses when she receives x=0
        - theta_A1 (float): angle that Alice chooses when she receives x=1
        - theta_B0 (float): angle that Bob chooses when he receives x=0
        - theta_B1 (float): angle that Bob chooses when he receives x=1
        - x (int): bit received by Alice
        - y (int): bit received by Bob
        - alpha (float): real coefficient of |00>
        - beta (float): real coefficient of |11>

    Returns:
        - (np.tensor): Probabilities of each basis state
    """

    prepare_entangled(alpha, beta)

    # QHACK #

    if x:
        qml.RY(theta_A1,wires=0)
    else:
        qml.RY(theta_A0,wires=0)
    if y:
        qml.RY(theta_B1,wires=1)
    else:
        qml.RY(theta_B0,wires=1)
    # QHACK #

    return qml.probs(wires=[0, 1])
    

def winning_prob(params, alpha, beta):
    """Define a function that returns the probability of Alice and Bob winning the game.

    Args:
        - params (list(float)): List containing [theta_A0,theta_A1,theta_B0,theta_B1]
        - alpha (float): real coefficient of |00>
        - beta (float): real coefficient of |11>

    Returns:
        - (float): Probability of winning the game
    """

    # QHACK #
    p00 = chsh_circuit(params[0], params[1], params[2], params[3], 0, 0, alpha, beta)
    p01 = chsh_circuit(params[0], params[1], params[2], params[3], 0, 1, alpha, beta)
    p10 = chsh_circuit(params[0], params[1], params[2], params[3], 1, 0, alpha, beta)
    p11 = chsh_circuit(params[0], params[1], params[2], params[3], 1, 1, alpha, beta)
    return (p00[0]+p00[3]+p01[0]+p01[3]+p10[0]+p10[3]+p11[1]+p11[2])/4
    # QHACK #
    

def optimize(alpha, beta):
    """Define a function that optimizes theta_A0, theta_A1, theta_B0, theta_B1 to maximize the probability of winning the game

    Args:
        - alpha (float): real coefficient of |00>
        - beta (float): real coefficient of |11>

    Returns:
        - (float): Probability of winning
    """

    def cost(params):
        """Define a cost function that only depends on params, given alpha and beta fixed"""

    # QHACK #
        return 1-winning_prob(params,alpha,beta)

    #Initialize parameters, choose an optimization method and number of steps
    init_params = np.array([np.random.random()*np.pi for i in range(4)], requires_grad=True)
    opt = qml.AdamOptimizer(stepsize=0.8)
    steps = 250

    # QHACK #
    
    # set the initial parameter values
    params = init_params

    for i in range(steps):
        # update the circuit parameters 
        # QHACK #
        params = opt.step(cost, params)
        # QHACK #

    return winning_prob(params, alpha, beta)


if __name__ == '__main__':
    inputs = sys.stdin.read().split(",")
    output = optimize(float(inputs[0]), float(inputs[1]))
    print(f"{output}")