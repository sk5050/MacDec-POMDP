#!/usr/bin/env python

# author: Sungkweon Hong
# email: sk5050@mit.edu

import sys
from MIG_model import MIG_Model
from agent import *
import copy
import numpy as np

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
    
    macro_policy = [{repr([]):"TL"},
                    {repr([]):"TL"}]

    multi_agents = Multi_Agents(Model, [Agent(Model,"agent-1",(0,0)), Agent(Model,"agent-2",(2,2))], macro_policy)


    reward, joint_state = multi_agents.simulate([(0,0), (2,2)], 2)
