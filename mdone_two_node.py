"""Generate an M/D/1 system with two nodes and two different lambdas entering the network

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
    return t + 0.00112

# AGENTS
ag_slow = qt.Agent(
    arrival_f = lambda t: t + random.expovariate(125)
)
ag_fast = qt.Agent(
    arrival_f = lambda t: t + random.expovariate(500)
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
        'service_f': ser
    },
    2: {
        'service_f': ser
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
qn.simulate(n=50000)
slow_data = qn.get_agent_data(return_header=True)
cols = (slow_data[1]).split(',')

# inject the faster lambdas
ag_fast.queue_action(queue=qn)
qn.simulate(n=50000)
fast_data = qn.get_agent_data()

# remove items that did not leave the system
clean_data = [item for k, item in fast_data.items() if len(item) > 1]

df_nodeone= pd.DataFrame(data=[item[0] for item in clean_data if item[0, -1] == 0.0], columns=cols)
df_nodeone['nodes'] = '1'

df_nodetwo= pd.DataFrame(data=[item[1] for item in clean_data if item[1, -1] == 1.0], columns=cols)
df_nodetwo['nodes'] = '2'

df_nodeall= pd.DataFrame(data=[item[2] for item in clean_data if len(item) >2], columns=cols)
df_nodeall['nodes'] = 'all'

frames = [df_nodeone, df_nodetwo, df_nodeall]
concat_frames = pd.concat(frames)

concat_frames.to_excel('mdone_two_node.xlsx')


concat_frames.rename(columns={
    'arrival': 'arrival_time',
    'service': 'service_start_time',
    'departure': 'departure_time',
    'num_queued': 'len_queue_before_this_request',
    'num_total': 'tot_requests_in_queue',
    'q_id': 'entry_node'
}, inplace=True)

print(concat_frames)