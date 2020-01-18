# -*- coding: utf-8 -*-

from utils import Reversi
from players.playerInterface import *
from utils.UCTSearch import *

class myPlayer(PlayerInterface):

    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None
        self._memoire = {}
        self._my_ai = 'UCT Search algorithm'

    def getPlayerName(self):
        return "MCTS - UCT Search"


    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1,-1)

        # moves = [m for m in self._board.legal_moves()]
        #move = moves[randint(0,len(moves)-1)]
        move = uct_search(self._board, self._mycolor)
        self._board.push(move)
        print("I am playing ", move)
        (c,x,y) = move
        assert(c==self._mycolor)
        print("My current board :")
        print(self._board)
        return (x,y) 

    def playOpponentMove(self, x,y):
        assert(self._board.is_valid_move(self._opponent, x, y))
        print("Opponent played ", (x,y))
        self._board.push([self._opponent, x, y])

    def newGame(self, color):
        self._mycolor = color
        self._opponent = 1 if color == 2 else 2
        if self._mycolor is self._board._WHITE:
            self._blanc = True
        else:
            self._blanc = False

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")



