# https://www.gymlibrary.dev/content/environment_creation/
# https://www.gymlibrary.dev/api/spaces/
# https://github.com/Farama-Foundation/gym-examples

import gym
from gym import spaces
import pygame
import numpy as np
import random

def encode_board(board, width, total_height): # 판을 하나의 정수로 저장
    res = 0
    for i in range(total_height):
        for j in range(width):
            res += board[i][j]
            res *= 2
    return res

def decode_board(res, width, total_height): # 정수를 판으로 복구
    board = [[None]*width for _ in range(total_height)]
    for i in range(total_height-1, -1, -1):
        for j in range(width-1, -1, -1):
            board[i][j] = res % 2
            res //= 2
    return board

class EsoTrisEnv():
    def __init__(self, width=9, height=14):
        self.width = width
        self.height = height
        self.total_height = height + 3 # 판 위쪽에 3줄의 공백이 있음

        self.reset()

        self.observation_space = spaces.Dict(
            {
                "encoded_board": spaces.Discrete(2**(self.width*self.total_height)), 
                "piece": spaces.Dict(
                    {
                        "type": spaces.Discrete(3), 
                        "x": spaces.Discrete(self.width), 
                        "y": spaces.Discrete(self.total_height, start=-3), 
                        "ori": spaces.Discrete(8), 
                    }
                ), 
            }
        )

        self.action_space = spaces.Discrete(7)
        self._action_to_key = ['k', 'j', 'l', 'n', '.', 'z', 'x']
    
    def push_piece(self):
        return {
            "type": random.randrange(0, 3),
            "x": 4, 
            "y": -2, 
            "ori": random.randrange(0, 8),
        }

    def reset(self): 
        self.board = [[None]*self.width for _ in range(self.total_height)]
        self.piece = self.push_piece()

    def step(self, action):
        key = self._action_to_key[action]
        if key == 'k':
            pass
        if key == 'j':
            pass
        if key == 'l':
            pass
        if key == 'n':
            pass
        if key == '.':
            pass
        if key == 'z':
            pass
        if key == 'x':
            pass
