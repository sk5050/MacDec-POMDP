#!/usr/bin/env python

# author: Sungkweon Hong
# email: sk5050@mit.edu

import math
import random

class Multi_Agents(object):

    def __init__(self, model, agents_list, macro_policy):

        self.model = model
        self.agents_list = agents_list
        self.macro_policy = macro_policy


    def simulate(self, initial_states, horizon, repetition=1):


        total_reward = 0
        for it in range(repetition):

            joint_state = initial_states
            joint_obs = initial_states
            joint_termination = [False, False]

            for agent in self.agents_list:
                agent.macro_history = []

            reward = 0
            for t in range(horizon):

                new_joint_state = []
                new_joint_obs = []
                new_joint_termination = []
                for i in range(len(self.agents_list)):

                    agent = self.agents_list[i]

                    macro_history = agent.macro_history

                    # print(macro_history)


                    if repr(macro_history) not in self.macro_policy[i]:
                        raise ValueError("policy not sufficient for horizon")

                    option = self.macro_policy[i][repr(macro_history)]

                    # if joint_termination[i] == True:
                    #     agent.macro_history.append(option)


                    new_state, new_obs, termination  = agent.execute_action(\
                                                           joint_state[i],joint_obs[i], self.model.option_dict[option])

                    new_joint_state.append(new_state)
                    new_joint_obs.append(new_obs)
                    new_joint_termination.append(termination)

                joint_state = new_joint_state
                joint_obs = new_joint_obs
                joint_termination = new_joint_termination

                # print("t : " + str(t))
                # print(joint_state)
                # print(reward)



                reward += self.reward(joint_state)

                if joint_state[0]==joint_state[1]:
                    break

            total_reward += reward

        total_reward = float(total_reward) / float(repetition)
        


        return total_reward


    def reward(self, joint_state):

        if joint_state[0]==joint_state[1]:
            return 1
        else:
            return 0

                         
        


        

class Agent(object):

    def __init__(self, model, agent_name, init_state):

        self.agent_name = agent_name
        self.macro_history = []
        self.model = model



    def execute_action(self, state, obs, option):
        action = option.option_policy[obs]

        rand = random.random()
        new_state_dist = self.model.state_transitions(state, action)  ## need to sample from distribution

        prob = 0
        for s in new_state_dist:
            prob += s[1]
            if rand <= prob:
                new_state = s[0]
                break


        rand = random.random()
        new_obs_dist = self.model.observations(state)  ## need to sample from distribution

        prob = 0
        for o in new_obs_dist:
            prob += o[1]
            if rand <= prob:
                new_obs = o[0]
                break


        rand = random.random()
        termination_prob = option.termination_cond[new_obs]  ## need to sample from distribution
        if rand <= termination_prob:
            is_terminated = True
        else:
            is_terminated = False
            
        if is_terminated:
            self.macro_history.append(new_obs)

        return new_state, new_obs, is_terminated
