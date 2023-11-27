"""Generate an M/D/1 system with one node and two different lambdas entering the network

"""
import random
import queueing_tool as qt
import pandas as pd
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
    0: [1]
}
edge_list = {
    0: {1: 1}
}

g = qt.adjacency2graph(
    adjacency=adja_list,
    edge_type=edge_list
)

q_classes = { 1: qt.QueueServer }
q_args = {
    1: {
        'num_server': 1,
        'arrival_f': lambda t: t + random.expovariate(1.5),  # fast requests
        'service_f': ser
    },
}
qn = qt.QueueNetwork(
    g = g,
    q_classes=q_classes,
    q_args=q_args
)

# init and accept agents from outside
qn.initialize()
qn.start_collecting_data()

# SIMULATE
ag_slow.queue_action(queue=qn)
qn.simulate(n=10)
slow_data = qn.get_agent_data(return_header=True)
cols = (slow_data[1]).split(',')

# inject the faster lambdas
ag_fast.queue_action(queue=qn)
qn.simulate(n=10)
fast_data = qn.get_agent_data()

df = pd.DataFrame(data=[item[0] for k, item in fast_data.items()], columns=cols)
df['q_id_exit'] = [item[1,-1] for k, item in fast_data.items()]
df['time_spent'] = [item[0, 2] - item[0, 0] for k, item in fast_data.items()]


try:
    df['rho (arr/ser)'] = [item[0, 0] / item[0, 1] for k, item in fast_data.items()]
except Exception as e:
    print('Run again.')
    # for now force it (need to find a better solution)
    df['rho (arr/ser)'] = [item[0, 0] / item[0, 1] for k, item in fast_data.items()]
    
try:
    df.to_excel('mdone_one_node.xlsx')
except Exception as e:
    print('Cannot save: ', e)
