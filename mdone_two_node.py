"""Generate an M/D/1 system with two nodes and two different lambdas entering the network

"""
import random
import queueing_tool as qt
import matplotlib.pyplot as plt

# SERVICE TIME
def ser(t: float):
    """Define deterministic service time.\n
    Take the arrival time as t and add a constant.

    Args:
        t (float): current time
    """
    return t + 0.15

# AGENTS
ag_slow = qt.Agent()
ag_fast = qt.Agent(
    arrival_f = lambda t: t + random.expovariate(0.25)
)

# Prepare the one-node network
adja_list = {
    0: [1], 1: [2]
}
edge_list = {
    0: {1: 1},
    1: {2: 2}
}

g = qt.adjacency2graph(
    adjacency=adja_list,
    edge_type=edge_list
)

q_classes = { 1: qt.QueueServer, 2: qt.QueueServer }
q_args = {
    1: {
        'num_server': 1,
        'arrival_f': lambda t: t + random.expovariate(1.5),  # fast requests
        'service_f': ser
    },
    2: {
        'num_server': 1,
        'arrival_f': lambda t: t,
        'service_f': ser
    },
}
qn = qt.QueueNetwork(
    g = g,
    q_classes=q_classes,
    q_args=q_args
)