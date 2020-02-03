#!/usr/bin/env python

# author: Sungkweon Hong
# email: sk5050@mit.edu

import math

class MIG_Model(object):

    def __init__(self, size=(3,3), prob_right_transition=0.6, prob_right_observation=1.0):


        self.prob_right_transition = prob_right_transition
        self.prob_right_observation = prob_right_observation
        self.size = size
        self.state_list = []
        self.obs_list = []
        self.macro_obs_list = []

        for i in range(size[0]):
            for j in range(size[1]):
                self.state_list.append((i,j))
                self.obs_list.append((i,j))
                self.macro_obs_list.append((i,j))

        self.action_list = ["U","L","R","D","S"]

        self.option_list = [Option("TL"), Option("BR")]

        self.option_list[0].option_policy = {(0,0):'U',
                                             (0,1):'U',
                                             (0,2):'S',
                                             (1,0):'U',
                                             (1,1):'U',
                                             (1,2):'L',
                                             (2,0):'U',
                                             (2,1):'U',
                                             (2,2):'L'}


        self.option_list[1].option_policy = {(0,0):'R',
                                             (0,1):'R',
                                             (0,2):'R',
                                             (1,0):'R',
                                             (1,1):'R',
                                             (1,2):'R',
                                             (2,0):'S',
                                             (2,1):'D',
                                             (2,2):'D'}


        self.option_list[0].termination_cond = {(0,0):0.0,
                                             (0,1):0.0,
                                             (0,2):1.0,
                                             (1,0):0.0,
                                             (1,1):0.0,
                                             (1,2):0.0,
                                             (2,0):0.0,
                                             (2,1):0.0,
                                             (2,2):0.0}


        self.option_list[1].termination_cond = {(0,0):0.0,
                                             (0,1):0.0,
                                             (0,2):0.0,
                                             (1,0):0.0,
                                             (1,1):0.0,
                                             (1,2):0.0,
                                             (2,0):1.0,
                                             (2,1):0.0,
                                             (2,2):0.0}

        self.option_dict = {"TL":self.option_list[0], "BR":self.option_list[1]}

        


    def actions(self, state):
        return self.action_list

    def state_transitions(self, state, action):
        if action=="U":
            new_states_temp = [[(state[0],state[1]+1), self.prob_right_transition],
                               [(state[0]+1,state[1]), (1-self.prob_right_transition)/2],
                               [(state[0]-1,state[1]), (1-self.prob_right_transition)/2]]

        elif action=="D":
            new_states_temp = [[(state[0],state[1]-1), self.prob_right_transition],
                               [(state[0]+1,state[1]), (1-self.prob_right_transition)/2],
                               [(state[0]-1,state[1]), (1-self.prob_right_transition)/2]]

        elif action=="L":
            new_states_temp = [[(state[0]-1,state[1]), self.prob_right_transition],
                               [(state[0],state[1]+1), (1-self.prob_right_transition)/2],
                               [(state[0],state[1]-1), (1-self.prob_right_transition)/2]]

        elif action=="R":
            new_states_temp = [[(state[0]+1,state[1]), self.prob_right_transition],
                               [(state[0],state[1]+1), (1-self.prob_right_transition)/2],
                               [(state[0],state[1]-1), (1-self.prob_right_transition)/2]]

            
        elif action=="S":
            new_states_temp = [[(state[0],state[1]), 1.0]]

        prob_stay = 0
        new_states = []
        for new_state in new_states_temp:
            if new_state[0] not in self.state_list:
                prob_stay = prob_stay + new_state[1]
            else:
                new_states.append(new_state)

        if prob_stay > 0:
            new_states.append([state, prob_stay])

        return new_states


    def observations(self, state,action=None):
        obs_dist = []

        for obs in self.obs_list:
            if obs == state:
                obs_dist.append([obs, 1.0])
            else:
                obs_dist.append([obs, 0.0])

        return obs_dist





class Option(object):

    def __init__(self, option_name, initiation_set=[], termination_cond=dict(), option_policy=dict()):

        self.option_name = option_name
        self.initiation_set = initiation_set
        self.termination_cond = termination_cond
        self.option_policy = option_policy


    def is_available(self, state):
        if self.initiation_set is empty:
            return True

        else:
            return state in self.initiation_set


    def termination_prob(self, state):
        return self.termination_cond[state]

    def action_by_option(self, obs):
        ## this option policy should take input as local history. current implementation is only for simple 3x3 meeting in grid.
        return self.option_policy[option][obs]
        
    def macro_observations(self, state):
        obs_dist = []

        for obs in self.obs_list:
            if obs == state:
                obs_dist.append([obs, 1.0])
            else:
                obs_dist.append([obs, 0.0])

        return obs_dist
