# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 18:05:41 2021

@author: Andre
"""

    
import numpy as np
from collections import deque
import random

from tensorflow.keras import Model, Sequential, Input
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
        self._gamma = 0.98
        self._epsilon = 1.0
        self._batch_size = 32
        self._tau = 0.1 #0.001
        
        # Build networks
        self.q_network = self.build_compile_model()
        self.target_network = self.build_compile_model()
        self.alighn_target_model()
        
        self.q_network.summary()
    
    
    def receive_action(self, input_data):
        if np.random.rand() <= self._epsilon:
            if np.random.rand() < 0.9:
                return Action(ActionType.HOLD)
            elif np.random.rand() < 0.5:
                return Action(ActionType.BUYALL)
            else:
                return Action(ActionType.SELLALL)
            #return np.random.choice(self.__action_list, 1)[0]
        else:
            x_train = np.reshape(input_data.processed_data(), (1, 3))       
            action_values = self.q_network.predict(x_train)[0,:]
            index = np.argmax(action_values)
            return self.__action_list[index]

    
    def update(self, state, action, reward, next_state):
         self._expirience_replay.append((state, action, reward, next_state))


    def epsilon(self, epsilon):
        self._epsilon = epsilon
    
    def train(self):
        minibatch = random.sample(self._expirience_replay, self._batch_size)

        #training_batch_state = np.zeros([self._batch_size, self._state_size])
        training_batch_state = []
        training_batch_action = []
        training_batch_reward = []
        training_batch_next_state = []
        
        for state, action, reward, next_state in minibatch:
            
            #x_state = np.reshape(state, (1, 3)) 
            training_batch_state.append(state)
            #state_array=np.array(state)
            #numpy_array = np.vstack([training_batch_state, state_array])
            
            #np.append(training_batch_state, np.array(state), axis=0)
            #training_batch_state.append(np.array([state]))
            
            #x_next_state = np.reshape(next_state, (1, 3))
            training_batch_next_state.append(next_state)
            #training_batch_next_state.append(np.array([next_state]))
            
            
            training_batch_reward.append(reward)
            
            action_number = 0
            if action.get_action_type() is ActionType.HOLD:
                action_number = 0
            if action.get_action_type() is ActionType.BUYALL:
                action_number = 1
            if action.get_action_type() is ActionType.SELLALL:
                action_number = 2
                
            training_batch_action.append(action_number)
            
              
        batch_array_state = np.array([training_batch_state])[0]
        target = self.q_network.predict(batch_array_state, batch_size=self._batch_size)

        batch_array_next_state = np.array([training_batch_next_state])[0]
        t = self.target_network.predict(batch_array_next_state, batch_size=self._batch_size)
        new_target = np.amax(t, axis=1)
        
        for i in range(self._batch_size):
            target[i][training_batch_action[i]] = training_batch_reward[i] + self._gamma * new_target[i]
            
        #y_train = np.reshape(target, (1, 3))

        #self.q_network.fit(x_state, y_train, epochs=1, verbose=0)
        self.q_network.fit(batch_array_state, target, batch_size=64, verbose=True)
    
    
    def update_target_weights(self):
        network_weights = self.q_network.get_weights()
        network_target_weights = self.target_network.get_weights()
        for w_i in range(len(network_weights)):
            network_target_weights[w_i] = self._tau * network_weights[w_i] + (1 - self._tau)* network_target_weights[w_i]
        self.target_network.set_weights(network_target_weights)
        
    
    def create_strategy(self):
        self.__action_list = np.empty(3, dtype=Action)
        self.__action_list[0] = Action(ActionType.HOLD)
        self.__action_list[1] = Action(ActionType.BUYALL)
        self.__action_list[2] = Action(ActionType.SELLALL)
        
        
    def build_compile_model(self):
        model = Sequential()
    #     # model.add(Embedding(self._state_size, 10, input_length=1))
    #     # model.add(Reshape((10,)))
    #     # model.add(Dense(50, activation='relu'))
    #     # model.add(Dense(50, activation='relu'))
    #     # model.add(Dense(self._action_size, activation='linear'))
        
        model.add(Dense(10, input_dim=self._state_size, activation='tanh'))
        #model.add(Dense(10, input_shape=(64,self._state_size), activation='relu'))
        model.add(Dense(10, activation='tanh'))
        model.add(Dense(self._action_size, activation='linear'))

        model.compile(loss='mse', optimizer=self._optimizer)
        return model
    
    
    # def create_network(self):
    #     input_state = Input(shape=[self._state_size], name='input_state')  
        
    #     hidden_1 = Dense(50, activation='tanh')(input_state)
    #     hidden_2 = Dense(50, activation='tanh')(hidden_1)
    #     action_value = Dense(self._action_size, activation='tanh')(hidden_2)
        
    #     actor_model = Model(inputs=input_state,outputs=action_value)
    #     actor_model.compile(loss='mse', optimizer=self._optimizer)
    #     return actor_model
    
    def alighn_target_model(self):
        self.target_network.set_weights(self.q_network.get_weights())