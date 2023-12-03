"""Generate an M/D/1 system with two nodes and two different lambdas entering the network

"""
import random
import queueing_tool as qt
import pandas as pd

# SERVICE TIME
def ser_nodeone(t: float):
    """Define deterministic service time.\n
    Take the arrival time as t and add a constant.

    Args:
        t (float): current time
    """
    # return t + 892
    return t + 0.00112

def ser_nodetwo(t: float):
    """Define deterministic service time.\n
    Take the arrival time as t and add a constant.

    Args:
        t (float): current time
    """
    # return t + 892
    return t + 0.001313

# AGENTS
ag_slow = qt.Agent(
    arrival_f = lambda t: t + random.expovariate(lambd=125)
)
ag_mid = qt.Agent(
    arrival_f = lambda t: t + random.expovariate(lambd=300)
)
ag_fast = qt.Agent(
    arrival_f = lambda t: 1/(t + random.expovariate(lambd=500))
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
        'service_f': ser_nodeone
    },
    2: {
        'service_f': ser_nodetwo
    },
}

qn = qt.QueueNetwork(
    g = g,
    q_classes=q_classes,
    q_args=q_args
)

# init and accept agents
qn.initialize(nActive=3)
qn.start_collecting_data()

# SIMULATE
ag_slow.queue_action(queue=qn)
qn.simulate(n=5000)
slow_data = qn.get_agent_data(return_header=True)
cols = (slow_data[1]).split(',')

# inject the mid lambdas
ag_mid.queue_action(queue=qn)
qn.simulate(n=5000)
mid_data = qn.get_agent_data()

# inject the faster lambdas
ag_fast.queue_action(queue=qn)
qn.simulate(n=5000)

# Retrieve all data
all_data = qn.get_agent_data()

# remove items that did not leave the system
clean_data = [item for k, item in all_data.items() if len(item) > 1]

df_nodeone = pd.DataFrame(data=[item[0] for item in clean_data if item[0, -1] == 0.0], columns=cols)
df_nodeone['time_spent'] = [item[0, 2] - item[0, 0] for item in clean_data if item[0, -1] == 0.0]

df_nodetwo= pd.DataFrame(data=[item[1] for item in clean_data if item[1, -1] == 1.0], columns=cols)
df_nodetwo['time_spent'] = [item[1, 2] - item[1, 0] for item in clean_data if item[1, -1] == 1.0]

df_nodelast= pd.DataFrame(data=[item[1] for item in clean_data if item[1, -1] == 2.0], columns=cols)

'''
No need for a "all" column, since with the departure time from the node 2
we can calculate the overall time spent in the system
'''

frames = [df_nodeone, df_nodetwo, df_nodelast]
concat_frames = pd.concat(frames)

concat_frames.rename(columns={
    'num_queued': 'requests_before',
    'num_total': 'tot_requests_in_queue',
    'q_id': 'node'
}, inplace=True)

print('''
Various information from the system
Remember: 
    - service and departure time of node 2 are always 0. This is the exiting node.
      Here "arrival" means that the requests arrives at the exit, so there are no
      other service or departure.
''')
print(
    concat_frames.groupby(['node'])[['arrival']].describe()
)
print(
    concat_frames.groupby(['node'])[['service']].describe()
)
print(
    concat_frames.groupby(['node'])[['departure']].describe()
)
print(
    concat_frames.groupby(['node'])[['time_spent']].describe()
)

try:
    concat_frames.to_excel('mdone_two_node.xlsx', float_format='%.5f')
except Exception as e:
    print('Cannot save: ', e)
