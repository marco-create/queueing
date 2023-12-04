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
    arrival_f = lambda t: t + random.expovariate(lambd=500)
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
        'service_f': ser_nodeone,
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

# Store requests
dat = [[n] + list(item) for n, req in enumerate(clean_data) for item in req]

cols.insert(0, 'agent_id')
df = pd.DataFrame(data=[req for req in dat], columns=cols)

times = []
for count, req in enumerate(dat):
    if req[3] - req[1] > 0:
        times.append(req[3]-req[1])
    else:
        if req[0] == dat[count-2][0]: # 2 nodes + 1
            times.append(req[1]-dat[count-2][1])
        if req[0] == dat[count-1][0] and req[0] != dat[count-2][0]:
            times.append(req[1]-dat[count-1][1])
            

df['time_spent'] = [*times]
# df['time_spent'] = [req[3] - req[1] if req[3]-req[1]>0 else req[1] for req in dat]

# nodes_info = []
# for idx, req in all_data.items():
#     if len(req) == 3:
#         first = req[0, 2] - req[0, 0]
#         second = req[len(req)-2, 2] - req[len(req)-2, 0]
#         third = req[len(req)-1, 0] - req[0, 0]
#         nodes_info.append(
#             {
#                 f'req: {idx[1]}': {
#                     'time_node_one': req[0, 2] - req[0, 0],
#                     'time_node_two': req[len(req)-2, 2] - req[0, 0],
#                     'time_overall': req[len(req)-1, 0] - req[0, 0]
#                 }
#             }
#         )
#     if len(req) == 2:
#         first = req[0, 2] - req[0, 0]
#         third = req[len(req)-1, 0] - req[0, 0]
#         nodes_info.append(
#             {
#                 f'req: {idx[1]}': {
#                     'time_node_one': req[0, 2] - req[0, 0],
#                     'time_node_two': pd.NA,
#                     'time_overall': req[len(req)-1, 0] - req[0, 0]
#                 }
#             }
#         )

# handle_dict = {}
# for item in nodes_info:
#     for key, value in item.items():
#         req_number = key.split(': ')[1]
#         handle_dict[req_number] = value
        
# info = pd.DataFrame(data=handle_dict).T
try:
    df.to_excel('mdone_two_node.xlsx')
    # info.to_excel('two_node_info.xlsx', float_format='%.4f')
except Exception as e:
    print('Cannot save: ', e)
    
print('done check excel file.')