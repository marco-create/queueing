"""Generate an M/D/1 system with one node and two different lambdas entering the network

"""
import random
import queueing_tool as qt
import pandas as pd

# SERVICE TIME
def ser(t: float):
    """Define deterministic service time.\n
    Take the arrival time as t and add a constant.

    Args:
        t (float): current time
    """
    # return t + 892
    return t + 0.00112

# AGENTS
ag_slow = qt.Agent()
ag_fast = qt.Agent(
    arrival_f = lambda t: t + random.expovariate(lambd=500)
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
        'arrival_f': lambda t: t + random.expovariate(lambd=125),  # slow requests
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
qn.simulate(n=5000)
slow_data = qn.get_agent_data(return_header=True)
cols = (slow_data[1]).split(',')

# inject the faster lambdas
ag_fast.queue_action(queue=qn)
qn.simulate(n=5000)
fast_data = qn.get_agent_data()

df = pd.DataFrame(data=[item[0] for k, item in fast_data.items()], columns=cols)
df['time_spent'] = [item[0, 2] - item[0,0] if item[0, 2] - item[0,0] > 0 else pd.NA for k, item in fast_data.items()]

df.rename(columns={
    'num_queued': 'requests_before',
    'num_total': 'tot_requests_in_queue',
    'q_id': 'entry_node'
}, inplace=True)

print('''
Various information from the system.
''')
print(df.describe())
try:
    df.to_csv('mdone_one_node.csv', float_format='%.5f')
except Exception as e:
    print('Cannot save: ', e)
