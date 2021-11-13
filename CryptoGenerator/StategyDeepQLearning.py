# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 18:05:41 2021

@author: Andre
"""

    
import numpy as np
from collections import deque
import random

from tensorflow.keras import Model, Sequential
from tensorflow.keras.layers import Dense, Embedding, Reshape
from tensorflow.keras.optimizers import Adam

from CryptoGenerator.Action import Action
from CryptoGenerator.Action import ActionType

from CryptoGenerator.Strategy import Strategy


class StategyDeepQLearning(Strategy):
    
    
    def __init__(self):
        self.create_strategy()
        self._state_size = 3
        self._action_size = 3
        self._optimizer = Adam(learning_rate=0.01)
        self._expirience_replay = deque(maxlen=2000)
        self._gamma = 0.6
        self._epsilon = 1.0
        self._batch_size = 32
        
        # Build networks
        self.q_network = self._build_compile_model()
        self.target_network = self._build_compile_model()
        self.alighn_target_model()
        
        self.q_network.summary()
    
    
    def receive_action(self, input_data):
        if np.random.rand() <= self._epsilon:
            return np.random.choice(self.__action_list, 1)[0]
        else:
            q_values = self.q_network.predict(input_data.processed_data())
            return np.argmax(q_values[0])

        
    
    
    def update(self, state, action, reward, next_state):
         self._expirience_replay.append((state, action, reward, next_state))
    
    
    def train(self):
        minibatch = random.sample(self._expirience_replay, self._batch_size)

        for state, action, reward, next_state in minibatch:

            target = self.q_network.predict(state)

            t = self.target_network.predict(next_state)
            target[0][action] = reward + self.gamma * np.amax(t)

            self.q_network.fit(state, target, epochs=1, verbose=0)
    
    
    def create_strategy(self):
        self.__action_list = np.empty(3, dtype=Action)
        self.__action_list[0] = Action(ActionType.BUYALL)
        self.__action_list[1] = Action(ActionType.HOLD)
        self.__action_list[2] = Action(ActionType.SELLALL)
        
        
    def _build_compile_model(self):
        model = Sequential()
        model.add(Embedding(self._state_size, 10, input_length=1))
        model.add(Reshape((10,)))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(self._action_size, activation='linear'))

        model.compile(loss='mse', optimizer=self._optimizer)
        return model
    
    def alighn_target_model(self):
        self.target_network.set_weights(self.q_network.get_weights())