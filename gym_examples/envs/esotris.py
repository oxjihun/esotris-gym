# https://www.gymlibrary.dev/content/environment_creation/
# https://www.gymlibrary.dev/api/spaces/
# https://github.com/Farama-Foundation/gym-examples

import gym
from gym import spaces
import pygame
import numpy as np
import random

class EsoTrisEnv():
    def encode_board(self): # 판을 하나의 정수로 저장하는 함수, observation에 들어갈 것이다. 
        res = 0
        for i in range(-3, self.height):
            for j in range(self.width):
                res += self.board[i][j]
                res *= 2
        return res

    def push_piece(self): # Port of pushPiece from .js, 랜덤한 '움직일 조각'을 반환하는 함수. type는 조각의 모양을, x와 y는 좌표를, ori는 회전된 각도를 의미한다. 
        return {
            "type": random.randrange(0, 3),
            "x": 4, 
            "y": -2, 
            "ori": random.randrange(0, 8),
        }
    
    def check_occupy(self): # Port of checkOccupy from .js, 조각이 차지하는 칸 3개를 반환한다. 
        angle = [self.piece.ori % 8, (4 - self.piece.type + self.piece.ori) % 8]
        delta = [[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1],[0,1],[1,1]]
        return [[self.piece.x, self.piece.y], [self.piece.x + delta[angle[0]][0], self.piece.y + delta[angle[0]][1]], [self.piece.x + delta[angle[1]][0], self.piece.y + delta[angle[1]][1]], angle]

    def available(self): # Port of available from .js, 조각이 판에 놓일 수 있는지를 확인한다. 
        occupy_data = self.check_occupy()
        for i in range(3):
            x = occupy_data[i][0]
            y = occupy_data[i][1]
            if not ((0 <= x < self.width) and (-3 <= y < self.height))
                return False
            if self.board[y][x] != -1:
                return False
        return True
    
    def move(self, direction): # 가능한 경우에만 조각을 direction 방향으로 이동시킨다. 
        self.piece.x += direction.x
        self.piece.y += direction.y
        if self.available():
            return True
        self.piece.x -= direction.x
        self.piece.y -= direction.y
        return False
    
    def rotate(self, do): # Port of rotate from .js, do 는 delta Orientation
        place_to_move = [[0,0],[-do,0],[do,0],[0,1],[-do,1],[do,1],[0,-1],[-do,-1],[do,-1]]
        self.piece.ori = (self.piece.ori + do) % 8
        for i in range(9):
            self.piece.x += place_to_move[i][0]
            self.piece.y += place_to_move[i][1]
            if self.available():
                return True
            self.piece.x -= place_to_move[i][0]
            self.piece.y -= place_to_move[i][1]
        self.piece.ori = (self.piece.ori - do) % 8
        return False

    def __init__(self, width=9, height=14):
        self.width = width
        self.height = height
        self.total_height = height + 3 # 판 위쪽에 3줄의 공백이 있다. 
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
    
    def _get_obs(self):
        return {"encoded_board": self.encode_board(self.board, self.width, self.total_height), "piece": self.piece}

    def reset(self): 
        super().reset()
        self.board = [[None]*self.width for _ in range(self.total_height)]
        self.piece = self.push_piece()

    def step(self, action):
        key = self._action_to_key[action]
        if key == 'k': self.move({"x": 0, "y": 1})
        if key == 'j': self.move({"x": -1, "y": 0})
        if key == 'l': self.move({"x": 1, "y": 0})
        if key == 'n': self.move({"x": -1, "y": 1})
        if key == '.': self.move({"x": 1, "y": 1})
        if key == 'z': self.rotate(1)
        if key == 'x': self.rotate(-1)

        # check if game ended
        # check if we can erase line