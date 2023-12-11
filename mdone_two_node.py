"""Generate an M/D/1 system with two nodes and two different lambdas entering the network

"""
import random
import numpy as np
import queueing_tool as qt
import pandas as pd

# SERVICE TIME
def ser(t: float):
    """Define deterministic service time.\n
    Take the arrival time as t and add a constant.

    Args:
        t (float): current time
    """
    return t + 0.000012

def ser_nodetwo(t: float):
    """Define deterministic service time.\n
    Take the arrival time as t and add a constant.

    Args:
        t (float): current time
    """
    return t + 0.001313

def identity(t: float):
    """Handler function for returning the current time

    Args:
        t (float): current time

    Returns:
        (float): current time
    """
    return t

# ARRIVAL FUNCTIONS
slow = 333.33333
fast = 63333.3334
slow_rate = lambda t:  t + random.expovariate(lambd=1.0/slow)
fast_rate = lambda t: t + random.expovariate(lambd=1.0/fast)

# AGENTS
class FastAgent(qt.Agent):
    def __init__(self, agent_id=(0, 0)):
        super().__init__(agent_id)
        self.agent_id = (agent_id[0], agent_id[1], 'fast')
        
class SlowAgent(qt.Agent):
    def __init__(self, agent_id=(0, 0)):
        super().__init__(agent_id)
        self.agent_id = (agent_id[0], agent_id[1], 'slow')

# Prepare the one-node network
q_classes = { 1: qt.QueueServer, 2: qt.QueueServer, 2: qt.QueueServer }

adja_list = {
    0: [2],
    1: [2],
    2: [3],
    3: [4]
}

edge_list = {
    0: {2: 1},
    1: {2: 2},
    2: {3: 3},
    3: {4: 4}
}

g = qt.adjacency2graph(
    adjacency=adja_list,
    edge_type=edge_list
)

q_args = {
    1: {
        'arrival_f': lambda t: qt.poisson_random_measure(t, slow_rate, slow),
        'service_f': identity,
        'AgentFactory': SlowAgent,
    },
    2: {
        'arrival_f': lambda t: qt.poisson_random_measure(t, fast_rate, fast),
        'service_f': identity,
        'AgentFactory': FastAgent,
    },
    3: {
        'service_f': ser,
    },
    4: {
        'service_f': ser_nodetwo,
    },
}
qn = qt.QueueNetwork(
    g = g,
    q_classes=q_classes,
    q_args=q_args
)

# init and accept agents
qn.initialize(edge_type=[1, 2])
qn.start_collecting_data()

# SIMULATE
qn.simulate(n=20000)
dat = qn.get_agent_data(return_header=True)
cols = (dat[1]).split(',')
cols.insert(0, 'agent_id')

prepare = [item for k, item in dat[0].items() if len(item) > 2 and k[2] == 'slow']
clean_data = [[n] + list(item) for n, req in enumerate(prepare) for item in req]

df = pd.DataFrame(data=[req for req in clean_data], columns=[cols])

times = []
for count, req in enumerate(clean_data):
    if req[2] != 0.0 and req[-1] in [0, 1, 2]:   # the leaving node
        times.append(pd.NA)
    if req[-1] == 3.0:
        times.append(req[1] - clean_data[count-2][1])
    if req[-1] == 4.0:
            times.append(req[1] - clean_data[count-3][1])
        
df['time_spent'] = [*times]
pd.options.display.float_format = '{:,.9f}'.format

slow_d = {k[1:3]: v for k, v in dat[0].items() if len(v) > 2 and k[2] == 'slow'}
times_slow = [v for k, v in slow_d.items()]
low = []
for req in times_slow:
    low.append(req[2, 0] - req[0, 0])
print('Average time spent within first node: ', format(float(np.average(low)), '.9f'))

for req in times_slow:
    low.append(req[3, 0] - req[0, 0])
print('Average time spent within whole system: ', format(float(np.average(low)), '.9f'))

print(df.describe())
try:
    df.to_excel('mdone_two_node.xlsx', float_format='%.5f')
except Exception as e:
    print('Cannot save: ', e)
