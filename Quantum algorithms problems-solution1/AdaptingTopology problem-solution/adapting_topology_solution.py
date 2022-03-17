
#! /usr/bin/python3

from cmath import cos, inf
import sys
from pennylane import numpy as np
import pennylane as qml

graph = {
    0: [1],
    1: [0, 2, 3, 4],
    2: [1],
    3: [1],
    4: [1, 5, 7, 8],
    5: [4, 6],
    6: [5, 7],
    7: [4, 6],
    8: [4],
}


def n_swaps(cnot):
    """Count the minimum number of swaps needed to create the equivalent CNOT.

    Args:
        - cnot (qml.Operation): A CNOT gate that needs to be implemented on the hardware
        You can find out the wires on which an operator works by asking for the 'wires' attribute: 'cnot.wires'

    Returns:
        - (int): minimum number of swaps
    """

    # QHACK #
    ## Find the minimum number of swaps by Dijkstra's algorithm

    control = cnot.control_wires[0]
    target  = cnot.wires[1]
    # print(control, target)

    costs = [len(graph.keys()) for _ in graph.keys()]
    # print("costs : "+str(costs))
    notDetermined = [j for j in graph.keys()]
    

    start = control
    costs[start] = 0
    notDetermined.remove(start)
    counterpartCosts = [costs[j] for j in notDetermined]
    result = inf
    while True:
        # print("start : "+str(start))
        # print("notDetermined : "+str(notDetermined))
        # print("counterpartCosts : "+str(counterpartCosts))
        # print("costs : "+str(costs))
        neighbours = graph[start]
        for neighbour in neighbours:
            if (costs[neighbour] > costs[start]+1):
                costs[neighbour] = costs[start]+1

        counterpartCosts = [costs[j] for j in notDetermined]
        start = notDetermined[np.argmin(counterpartCosts)]
        notDetermined.remove(start)
        counterpartCosts = [costs[j] for j in notDetermined]
        # counterpartCosts.pop(start)

        # print("start after : "+str(start))
        # print("notDetermined after : "+str(notDetermined))
        # print("counterpartCosts after : "+str(counterpartCosts))
        # print("costs after : "+str(costs))

        if start == target:
            result = costs[target]
            break

    return 2*(result-1)

    # QHACK #


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(",")
    output = n_swaps(qml.CNOT(wires=[int(i) for i in inputs]))
    print(f"{output}")

