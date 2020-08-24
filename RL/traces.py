# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 11:56:17 2020

@author: huyue
"""
import numpy as np


class traces:

    def __init__(self, memory_size, n_tilings, n_actions):

        self.MAX_NONZERO_TRACES = 100000
        self.N_ACTIONS = n_actions
        self.N_TILINGS = n_tilings
        self.tolerance = 0.01
        self.nonzero_traces_inverse = np.zeros(memory_size)
        self.eligibility = np.zeros(memory_size)
        self.n_nonzero_traces = 0
        self.nonzero_traces = np.zeros(self.MAX_NONZERO_TRACES)

    def decay(self, rate):

        for loc in range(self.n_nonzero_traces - 1, -1, -1):  # 这里有点疑问的呢
            f = self.nonzero_traces[loc]
            self.eligibility[f] *= rate

            if (self.eligibility[f] < self.tolerance):
                self.clear_existing(f, loc)

    def update(self, state, action):

        for a in range(0, self.N_ACTIONS):
            features = state.getFeatures(a)

            if(a != action):
                for t in range(0, self.N_TILINGS):
                    self.clear(features[t])
            else:
                for t in range(0, self.N_TILINGS):
                    self.set_(features[t], 1.0)

    def begin(self):

        return self.nonzero_traces

    def end(self):

        return self.nonzero_traces[self.n_nonzero_traces]

    def get(self, feature):

        return self.eligibility[feature]

    def set_(self, feature, value):

        if(self.eligibility[feature] >= self.tolerance):
            self.eligibility[feature] = value
        else:
            while(self.n_nonzero_traces >= self.MAX_NONZERO_TRACES):
                self.increase_tolerance()

            self.eligibility[feature] = value
            self.nonzero_traces[self.n_nonzero_traces] = feature
            self.nonzero_traces_inverse[feature] = self.n_nonzero_traces
            self.n_nonzero_traces += 1

    def clear(self, feature):

        if (self.eligibility[feature] != 0.0):
            self.clear_existing(feature, self.nonzero_traces_inverse[feature])

    def clear_existing(self, feature, loc):

        self.eligibility[feature] = 0.0
        self.n_nonzero_traces -= 1
        self.nonzero_traces[loc] = self.nonzero_traces[self.n_nonzero_traces]
        self.nonzero_traces_inverse[self.nonzero_traces[loc]] = loc

    def increase_tolerance(self):

        self.tolerance *= 1.1
        for loc in range(self.n_nonzero_traces - 1, -1, -1):
            f = self.nonzero_traces[loc]

            if (self.eligibility[f] < self.tolerance):
                self.clear_existing(f, loc)
