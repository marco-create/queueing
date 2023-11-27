"""Generate an M/D/1 system with two nodes and two different lambdas entering the network

"""
import random
import pandas as pd
import queueing_tool as qt

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
qn.simulate(n=10)
slow_data = qn.get_agent_data(return_header=True)
cols = (slow_data[1]).split(',')

# inject the faster lambdas
ag_fast.queue_action(queue=qn)
qn.simulate(n=10)
fast_data = qn.get_agent_data()

# remove items that did not leave the system
clean_data = [item for k, item in fast_data.items() if len(item) > 1]

df_nodeone= pd.DataFrame(data=[item[0] for item in clean_data if item[0, -1] == 0.0], columns=cols)
df_nodeone['time_spent'] = [item[0, 2] - item[0, 0] for item in clean_data if item[0, -1] == 0.0]
df_nodeone['rho (arr/ser)'] = [item[0, 0] / item[0, 1] for item in clean_data if item[0, -1] == 0.0]
df_nodeone['nodes'] = 'first'

df_nodetwo= pd.DataFrame(data=[item[1] for item in clean_data if item[1, -1] == 1.0], columns=cols)
df_nodetwo['time_spent'] = [item[1, 2] - item[1, 0] for item in clean_data if item[1, -1] == 1.0]
df_nodetwo['rho (arr/ser)'] = [item[1, 0] / item[1, 1] for item in clean_data if item[1, -1] == 1.0]
df_nodetwo['nodes'] = 'second'

df_nodeall= pd.DataFrame(data=[item[2] for item in clean_data if len(item) >2], columns=cols)
df_nodeall['time_spent'] = [item[1, 2] - item[0, 0] for item in clean_data if len(item) >2]
df_nodeall['rho (arr/ser)'] = [item[0, 0] / item[1, 1] for item in clean_data if len(item) >2]
df_nodeall['nodes'] = 'tot'

frames = [df_nodeone, df_nodetwo, df_nodeall]
concat_frames = pd.concat(frames)

concat_frames.to_excel('mdone_two_node.xlsx')
