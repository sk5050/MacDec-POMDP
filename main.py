#!/usr/bin/env python

# author: Sungkweon Hong
# email: sk5050@mit.edu

import sys
from MIG_model import MIG_Model
from agent import *
import copy
# import numpy as np
import time

# Now you can give command line cc argument after filename
if __name__ == '__main__':
    Model = MIG_Model()

    # print(Model.state_list)
    # print(Model.obs_list)
    # print(Model.action_list)
    
    S0 = Model.state_list[0]
    # print(S0)

    # print("------------------------------")
    # print(Model.state_transitions(S0, Model.actions(S0)[0]))
    # print("------------------------------")
    # print(Model.observations(S0))
    
    # macro_policy = [{repr([]):"TL"},
    #                 {repr([]):"TL"}]

    macro_policy = [{repr([]):"TL",
                     repr([(0,0)]):"BR",repr([(0,1)]):"BR",repr([(0,2)]):"BR",repr([(1,0)]):"BR",repr([(1,1)]):"BR",repr([(1,2)]):"BR",repr([(2,0)]):"BR",repr([(2,1)]):"BR",repr([(2,2)]):"BR"},
                    {repr([]):"TL",
                     repr([(0,0)]):"BR",repr([(0,1)]):"BR",repr([(0,2)]):"BR",repr([(1,0)]):"BR",repr([(1,1)]):"BR",repr([(1,2)]):"BR",repr([(2,0)]):"BR",repr([(2,1)]):"BR",repr([(2,2)]):"BR"}]

    multi_agents = Multi_Agents(Model, [Agent(Model,"agent-1",(0,0)), Agent(Model,"agent-2",(2,2))], macro_policy)


    risk_list = []
    # t = time.time()
    for i in range(200):
        reward = multi_agents.simulate([(0,0), (2,2)], 3, 26500)
        risk_list.append(reward)
    # print("elapsed time: " + str(time.time() - t))

    # print(reward)
    print(risk_list)

    print("--------------------")

    mean = sum(risk_list) / len(risk_list)

    print("mean: " + str(mean))
    count = 0
    for i in risk_list:
        if abs(i - mean) > 0.01:
            count += 1

    print count
