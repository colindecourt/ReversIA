# -*- coding: utf-8 -*-

import time
import Reversi
from random import randint
from playerInterface import *
import numpy as np 


''' 
Plusieurs critères de tri des coups sont généralement utilisés à Othello:

1.  En fonction du type de case. On joue d’abord les coins et en dernier les cases C et X.

2.  Tri du plus rapide d’abord. On joue en premier les coups qui minimisent la mobilité (le nombre de coups) de l’adversaire.
    En procédant ainsi, on aura un plus petit nombre de coups à examiner en premier lieu et cela ira donc plus vite. 
    Cette technique est très efficace, particulièrement vers la fin de la partie.

3.  Tri par recherche courte. Avant de ce lancer dans une recherche longue, on évalue le score de chaque coup par une recherche 
    à quelques coups de profondeur (généralement 1 ou 2, parfois plus si la recherche à effectuer est très profonde). 
    Les coups sont ensuite triés depuis le meilleur score jusqu’au plus mauvais.

4.  Coup meurtrier. On essaie en premier une réponse habituelle au coup précédent. Pour cela on maintient un tableau des fréquences 
    des réponses à chaque coup et l’on jouera la réponse la plus fréquente. Par exemple après g2, la réponse la plus fréquente est h1, 
    on essaiera donc ce coup en premier.

5.  Coup mémorisé. On regarde dans la table de transposition si cette position a déjà été joué et, en cas de réponse positive, on recommence 
    avec le meilleur coup trouvé précédemment. Couplé avec l’approfondissement itératif ou une succession de recherche de moins en moins 
    sélective, cette technique est très efficace. La question subsidiaire est de savoir quels tris effectuer et quand. Effectuer tous les tris 
    dans l’ordre indiqué ci-dessus est une possibilité, mais certaines techniques sont coûteuses en temps (tri par recherche courte, tri du plus 
    rapide d’abord, …) et l’on a intérêt à les réserver au positions proche de la racine. L’utilisation optimale de ces techniques est un 
    problème de réglage qui dépend de chaque programme, de ses qualités intrinsèques et des ressources disponibles.
'''

'''
D'après :   http://www.ffothello.org/othello/principes-strategiques/ 
            https://kartikkukreja.wordpress.com/2013/03/30/heuristic-function-for-reversiothello/

Idée : créer un tableau de poids de manière à pondérer certains endroits :
    1.  Par exemple les angles sont les meilleurs endroits pour gagner on mettra donc des poids plus importants au niveau des angles que 
        au centre du plateau. 
    2.  Il faut eviter d'être proche des angles (cases noté X et C) car cela peut entraîner la défaite car on donne un coin à l'adversaire 
        et donc on peut perdre beaucoup de pions. 
    3.  Etre sur les côtés (or cases X et C) peut permettre de prendre des pions à l'adversaire : donc plus de poids ici. 

'''
def estimeFin(board, player, blanc):
    val = None
    if board.is_game_over():
        (nbwhite, nbblack) = board.get_nb_pieces()
        if nbwhite == nbblack:
            val = 0
        elif nbwhite > nbblack:
            val = 1000 if blanc else -1000
        else:
            val = -1000 if blanc else 1000
    else:
        val = heuristique(board, player)
    return (val, None)

'''
Ici : définir les différentes heuristiques en fonction des moments
'''

WEIGHT_BOARD_10_10 = [[20, -3, 11, 8, 6, 6, 8, 11, -3, 20],
                [-3, 7, -4, 1, 1, 1, 1, -4, -7, -3],
                [-1, 5, -2, 1, 1, 1, 1, -2, 5, -1],
                [11, -4, 3, 2, 2, 2, 2, 3, -4, 11],
                [8, 1, 2, -3, -3, -3, -3, 2, 1, 8],
                [8, 1, 2, -3, -3, -3, -3, 2, 1, 8],
                [11, -4, 3, 2, 2, 2, 2, 3, -4, 11],
                [-1, 5, -2, 1, 1, 1, 1, -2, 5, -1],
                [-3, 7, -4, 1, 1, 1, 1, -4, -7, -3],
                [20, -3, 11, 8, 6, 6, 8, 11, -3, 20]]


def piece_diff_heur(board, player):
    weights = WEIGHT_BOARD_10_10.copy()
    b = board._board
    d = 0
    my_tiles = 0
    opp_tiles = 0
    my_frontier_tiles = 0
    opp_frontier_tiles = 0

    '''
    X and Y are used to find the indices of the eight neighboring cells of a given cell. Moor neighborhood. 
    '''
    X = [-1, -1, 0, 1, 1, 1, 0, -1]
    Y = [0, 1, 1, 1, 0, -1, -1, -1]
    for i in range(board._boardsize):
        for j in range(board._boardsize):
            if b[i][j] is player._mycolor:
                d += weights[i][j]
                my_tiles += 1
            elif b[i][j] is player._opponent:
                d -= weights[i][j]
                opp_tiles += 1

            if b[i][j] is not board._EMPTY:
                for k in range(len(X)):
                    x = i + X[k]
                    y = j + Y[k]
                    if x >=0 and x < board._boardsize and y >=0 and y < board._boardsize and b[x][y] is board._EMPTY:
                        if (b[i][j] is player._mycolor):
                            my_frontier_tiles += 1
                        else:
                            opp_frontier_tiles += 1
                        break
    if my_tiles > opp_tiles:
        p = (100 * my_tiles)/(my_tiles + opp_tiles)
    elif my_tiles < opp_tiles:
        p = -(100 * opp_tiles)/(my_tiles + opp_tiles)
    else:
        p = 0

    if my_frontier_tiles > opp_frontier_tiles:
        f = -(100 * my_frontier_tiles)/(my_frontier_tiles + opp_frontier_tiles)
    elif my_frontier_tiles < opp_frontier_tiles:
        f = (100 * opp_frontier_tiles)/(my_frontier_tiles + opp_frontier_tiles)
    else:
        f = 0
    return p, f, d


# Retourne la mobilité immédiate
def mobility_heur(board, player):
    my_moves = board.count_legal_moves(player)
    opponent_moves = board.count_legal_moves(board._flip(player))
    if my_moves > opponent_moves:
        m = (100 * my_moves)/(my_moves + opponent_moves)
    elif my_moves < opponent_moves:
        m = -(100 * opponent_moves)/(my_moves + opponent_moves)
    else:
        m = 0
    return m

'''
Retourne 1 si MON joueur joue en dernier donc possède un léger avantage, retourne -1 sinon :
Exemple :   Si aucun joueur ne passe son tour durant la partie, il y a un nombre pair de cases vides
            quand Noir a le trait, (c’est-à-dire quand c’est à lui de jouer). Quand Blanc a le trait, 
            il reste un nombre impair de cases. Conclusion ? Blanc joue le dernier coup de la partie et
            possède donc un léger avantage, puisque le pion qu’il pose alors et ceux qu’il retourne 
            sont évidemment définitifs.
'''
def coin_parity_heur(board, player):
    if (board._boardsize**2)-(board._nbBLACK+board._nbWHITE) %2 == 1:
        return 1
    else: 
        return -1


    
def corner_occupancy_heur(board, player):
    my_tiles = 0 
    opp_tiles = 0
    # Count tile in corners
    for i in [0, board._boardsize-1]:
        for j in [0, board._boardsize-1]:
            if board._board[i][j] is player._mycolor:
                my_tiles += 1
            elif board._board[i][j] is player._opponent:
                opp_tiles +=1
    return 25*(my_tiles-opp_tiles)       


def corner_closeness_heur(board, player):
    lh_corner = (0,0)
    rh_corner = (0, board._boardsize-1)
    ll_corner = (board._boardsize-1, 0)
    rl_corner = (board._boardsize-1, board._boardsize-1)

    bc_tiles = 0
    wc_tiles = 0
    if board._board[lh_corner[0]][lh_corner[1]] is board._EMPTY:
        if board._board[0][1] is board._BLACK:
            bc_tiles += 1
        elif board._board[0][1] is board._WHITE:
            wc_tiles += 1
        if board._board[1][1] is board._BLACK:
            bc_tiles += 1
        elif board._board[1][1] is board._WHITE:
            wc_tiles += 1
        if board._board[1][0] is board._BLACK:
            bc_tiles += 1
        elif board._board[1][0] is board._WHITE:
            wc_tiles += 1

    if board._board[rh_corner[0]][rh_corner[1]] is board._EMPTY:
        if board._board[0][board._boardsize-2] is board._BLACK:
            bc_tiles += 1
        elif board._board[0][board._boardsize-2] is board._WHITE:
            wc_tiles += 1
        if board._board[1][board._boardsize-2] is board._BLACK:
            bc_tiles += 1
        elif board._board[1][board._boardsize-2] is board._WHITE:
            wc_tiles += 1
        if board._board[1][board._boardsize-1] is board._BLACK:
            bc_tiles += 1
        elif board._board[1][board._boardsize-1] is board._WHITE:
            wc_tiles += 1

    if board._board[ll_corner[0]][ll_corner[1]] is board._EMPTY:
        if board._board[board._boardsize-1][1] is board._BLACK:
            bc_tiles += 1
        elif board._board[board._boardsize-1][1] is board._WHITE:
            wc_tiles += 1
        if board._board[board._boardsize-2][1] is board._BLACK:
            bc_tiles += 1
        elif board._board[board._boardsize-2][1] is board._WHITE:
            wc_tiles += 1
        if board._board[board._boardsize-2][0] is board._BLACK:
            bc_tiles += 1
        elif board._board[board._boardsize-2][0] is board._WHITE:
            wc_tiles += 1
    if board._board[rl_corner[0]][rl_corner[1]] is board._EMPTY:
        if board._board[board._boardsize-2][board._boardsize-1] is board._BLACK:
            bc_tiles += 1
        elif board._board[board._boardsize-2][board._boardsize-1] is board._WHITE:
            wc_tiles += 1
        if board._board[board._boardsize-2][board._boardsize-2] is board._BLACK:
            bc_tiles += 1
        elif board._board[board._boardsize-2][board._boardsize-2] is board._WHITE:
            wc_tiles += 1
        if board._board[board._boardsize-1][board._boardsize-2] is board._BLACK:
            bc_tiles += 1
        elif board._board[board._boardsize-1][board._boardsize-2] is board._WHITE:
            wc_tiles += 1

    if player._mycolor is board._WHITE:
        return -12.5*(wc_tiles - bc_tiles) 
    else:
        return -12.5*(bc_tiles - wc_tiles)      


def heuristique(board, player=None):
    p, f, d = piece_diff_heur(board, player)
    l = corner_closeness_heur(board, player)
    c = corner_occupancy_heur(board, player)
    m = mobility_heur(board, player)
    cp = coin_parity_heur(board, player)
    return (10*p) + (100*cp) + (801.724 * c) + (382.026 * l) + (78.922 * m) + (74.396 * f) + (10 * d)


def negAlphaBeta(b, color, alpha, beta, blanc, horizon=10):

    if horizon == 0 or b.is_game_over():
        return estimeFin(b, color, blanc)

    meilleur = None
    meilleurCoup = None
    for m in b.legal_moves():
        b.push(m)
        (nm, _) = negAlphaBeta(b, color, -beta, -alpha, not blanc, horizon - 1)
        nm = -nm
        if meilleur is None or nm > meilleur:
            meilleur = nm
            meilleurCoup = m
            if meilleur > alpha:
                alpha = meilleur
                if alpha > beta: # Coupure
                    b.pop()
                    return (meilleur, meilleurCoup)
        b.pop()

    return (meilleur, meilleurCoup)


''' 
Code de alpha beta avec mémoire inspiré de : http://www.ffothello.org/informatique/algorithmes/
Idée : implémenter MTDF
'''

def alphaBetaAvecMemoire(b, memoire, color, alpha, beta, blanc, horizon=10):

    hashtable_board = str(b._board)
    if hashtable_board in memoire:
        pos = memoire[hashtable_board]

        if pos[0] >= beta:
            return pos[0]
        if pos[1] <= alpha:
            return pos[1]
        alpha = max(alpha, pos[0])
        beta = min(beta, pos[1])

    if b.is_game_over() or horizon==0:
        return estimeFin(b, color, blanc)

    a = alpha
    meilleurCoup = None
    meilleur = -np.inf
    for m in b.legal_moves():
        b.push(m)
        (nm, _) = negAlphaBeta(b, color, -beta, -a, not blanc, horizon-1)
        b.pop()
        if nm >= meilleur:
            meilleur = nm
            meilleurCoup = m
            if nm >= a:
                a = nm
                if nm >= beta:
                    break

    # On stock les meilleurs 
    pos = [-np.inf, np.inf]
    if meilleur <= alpha:
        pos[1] = meilleur
    if meilleur > alpha and meilleur < beta:
        pos = [meilleur, meilleur]
    if meilleur >= beta:
        pos[0] = meilleur
    memoire[hashtable_board] = pos

    return (meilleur, meilleurCoup)


def MTDF(b, memoire, color, blanc, horizon=10, init_g = 0):
    g = init_g
    upperbound = np.inf
    lowerbound = -np.inf
    while(1):
        if g == lowerbound:
            beta = g+1
        else:
            beta = g
        (g, meilleurCoup) = alphaBetaAvecMemoire(b, memoire, color, beta-1, beta, not blanc, horizon)
        if g < beta:
            upperbound = g
        else:
            lowerbound = g

        if upperbound == lowerbound:
            break
        del memoire[str(b._board)]
        print("Meilleur coup :", meilleurCoup)
        return (None, meilleurCoup)


class myPlayer(PlayerInterface):


    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None
        self._memoire = {}
        self._my_ai = 'AlphaBeta with Memory'

    def getPlayerName(self):
        return "AlphaBeta"


    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1,-1)

        moves = [m for m in self._board.legal_moves()]
        #move = moves[randint(0,len(moves)-1)]
        (_, move) = MTDF(self._board, self._memoire, self, self._blanc, 5)
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



