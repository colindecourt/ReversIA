# -*- coding: utf-8 -*-

import time
import Reversi
from random import randint, choice
import numpy as np

def RandomMove(b):
    return choice(list(b.legal_moves(b._nextPlayer)))

def deroulementRandom(b):
    print("----------")
    print(b)
    if b.is_game_over():
        return
    move = RandomMove(b) 
    b.push(move)
    deroulementRandom(b)
    b.pop()


def heuristique(b, blanc, heur_type):
    return b.heuristique(heur_type=heur_type)

def estimeFin(b, blanc, heur_type):
    val = None
    if b.is_game_over():
        (nbwhite, nbblack) = b.get_nb_pieces()
        if nbwhite == nbblack:
            val = 0
        elif nbwhite > nbblack:
            val = 1000 if blanc else -1000
        else:
            val = -1000 if blanc else 1000
    else:
         val = heuristique(b, blanc, heur_type= heur_type)
    return (val, None)

def negaMax(b, heur_type, blanc=True, horizon=10):

    if horizon == 0 or b.is_game_over():
        return estimeFin(b, blanc, heur_type=heur_type)

    meilleur = None
    meilleurCoup = None
    for m in b.legal_moves():
        b.push(m)
        (nm, _) = negaMax(b, heur_type, not blanc, horizon - 1)
        nm = -nm
        if meilleur is None or nm > meilleur:
            meilleur = nm
            meilleurCoup = m
        b.pop()

    return (meilleur, meilleurCoup)

# Neg Alpha Beta avec version d'echec
def negAlphaBeta(b, heur_type, alpha, beta, blanc=True, horizon=10):

    if horizon == 0 or b.is_game_over():
        return estimeFin(b, blanc, heur_type=heur_type)

    meilleur = None
    meilleurCoup = None
    for m in b.legal_moves():
        b.push(m)
        (nm, _) = negAlphaBeta(b, heur_type, -beta, -alpha, not blanc, horizon - 1)
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

def alphaBetaAvecMemoire(b, memoire, heur_type, alpha, beta, blanc=True, horizon=10):

    hashtable_board = str(b._board)
    if hashtable_board in memoire:
        pos = memoire[hashtable_board]

        if pos[0] >= beta:
            return pos[0]
        if pos[1] <= alpha:
            return pos[1]
        alpha = max(alpha, pos[0])
        beta = min(beta, pos[1])

    if board.is_game_over() or horizon==0:
        return estimeFin(b, blanc, heur_type=heur_type)

    a = alpha
    meilleurCoup = None
    meilleur = -np.inf
    for m in b.legal_moves():
        b.push(m)
        (nm, _) = negAlphaBeta(b, heur_type, -beta, -a, not blanc, horizon-1)
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


def MTDF(b, memoire, heur_type, blanc=True, horizon=10, init_g = 0):
    g = init_g
    upperbound = np.inf
    lowerbound = -np.inf
    while(1):
        if g == lowerbound:
            beta = g+1
        else:
            beta = g
        (g, meilleurCoup) = alphaBetaAvecMemoire(b, memoire, heur_type, beta-1, beta, not blanc, horizon)
        if g < beta:
            upperbound = g
        else:
            lowerbound = g

        if upperbound == lowerbound:
            break
        del memoire[str(board._board)]
        print("Meilleur coup :", meilleurCoup)
        return (None, meilleurCoup)



board = Reversi.Board(8)
memoire = {} # liste des meilleurs coups possible
# Problème : quand on est en fin de partie, le ID est relancé des millieurs de fois avec une profondeur max très grande
while not board.is_game_over():
    tt = time.perf_counter()
    (_, coup) = MTDF(board, memoire, 'corner_occupancy', True, 5)
    print("AlphaBetaAvecMemoire joue " + str(coup) + " en " + str(time.perf_counter()-tt))
    #assert(board.is_valid_move(coup))
    board.push(coup)

    tt = time.perf_counter()
    (_, coup) = negaMax(board,'count', False, 5)  # Profondeur donnée en nombre de coups
    print("negaMax " + str(coup) + " en " + str(time.perf_counter()-tt))
    board.push(coup)
    print(board)

