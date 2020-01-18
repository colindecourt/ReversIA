from players import myPlayerUCTSearch, myPlayerBasic, myPlayerAlphaBeta
from localGame import run_local_game
import seaborn as sb
import matplotlib.pyplot as plt
import numpy as np

NUM_PARTY = 10
_BLACK = 1 # Black
_WHITE = 2 # White


def random_vs_uct(ai1 =myPlayerBasic, ai2 =myPlayerUCTSearch):
    # contain vector [is_win, num_tiles, time]
    victory_random = []
    victory_uct = []
    for party in range(NUM_PARTY):
        winner, nb_white, nb_black, time = run_local_game(ai1, ai2)
        if winner == _BLACK:
            victory_random.append([True, nb_black, time[0]])
            victory_uct.append([False, nb_white, time[1]])
        elif winner == _WHITE:
            victory_random.append([False, nb_black, time[0]])
            victory_uct.append([True, nb_white, time[1]])
        else:
            print('Deuce')
    plt.figure(1)
    sb.set_style('darkgrid')
    plt.bar([0,1], [np.sum([victory_random[i][0] for i in range(len(victory_random))]),
                    np.sum([victory_uct[i][0] for i in range(len(victory_uct))])],
                    color='r')
    plt.xticks([0, 1], ('Random moves', 'UCT Search'))
    plt.title('Number of games won')
    plt.show()

    plt.figure(2)
    sb.set_style('darkgrid')
    plt.plot([victory_random[i][1] for i in range(len(victory_random))], label='Random method tiles')
    plt.plot([victory_uct[i][1] for i in range(len(victory_uct))], label='UCT Search method tiles')
    plt.title('Number of tile per party for each method')
    plt.show()

    plt.figure(3)
    sb.set_style('darkgrid')
    plt.plot([victory_random[i][2] for i in range(len(victory_random))], label='Time to play random method')
    plt.plot([victory_uct[i][2] for i in range(len(victory_uct))], label='Time to play UCT Search method')
    plt.title('Move time per method per party')
    plt.show()


def random_vs_heuristic(ai1 =myPlayerBasic, ai2 =myPlayerAlphaBeta):
    # contain vector [is_win, num_tiles, time]
    victory_random = []
    victory_alpha_beta = []
    for party in range(NUM_PARTY):
        winner, nb_white, nb_black, time = run_local_game(ai1, ai2)
        if winner == _BLACK:
            victory_random.append([True, nb_black, time[0]])
            victory_alpha_beta.append([False, nb_white, time[1]])
        else:
            victory_random.append([False, nb_black, time[0]])
            victory_alpha_beta.append([True, nb_white, time[1]])
    plt.figure(1)
    sb.set_style('darkgrid')
    plt.bar([0,1], [np.sum([victory_random[i][0] for i in range(len(victory_random))]),
                    np.sum([victory_alpha_beta[i][0] for i in range(len(victory_alpha_beta))])],
                    color='r')
    plt.xticks([0, 1], ('Random moves', 'AlphaBeta with Memory'))
    plt.title('Number of games won')
    plt.show()

    plt.figure(2)
    sb.set_style('darkgrid')
    plt.plot([victory_random[i][1] for i in range(len(victory_random))], label='Random method tiles')
    plt.plot([victory_alpha_beta[i][1] for i in range(len(victory_alpha_beta))], label='AlphaBeta method tiles')
    plt.title('Number of tile per party for each method')
    plt.show()

    plt.figure(3)
    sb.set_style('darkgrid')
    plt.plot([victory_random[i][2] for i in range(len(victory_random))], label='Time to play random method')
    plt.plot([victory_alpha_beta[i][2] for i in range(len(victory_alpha_beta))], label='Time to play AlphaBeta method')
    plt.title('Move time per method per party')
    plt.show()


def alpha_beta_vs_uct(ai1 =myPlayerAlphaBeta, ai2 =myPlayerUCTSearch):
    # contain vector [is_win, num_tiles, time]
    victory_alpha_beta = []
    victory_uct = []
    for party in range(NUM_PARTY):
        winner, nb_white, nb_black, time = run_local_game(ai2, ai1)
        if winner == _WHITE:
            victory_alpha_beta.append([True, nb_black, time[0]])
            victory_uct.append([False, nb_white, time[1]])
        else:
            victory_alpha_beta.append([False, nb_black, time[0]])
            victory_uct.append([True, nb_white, time[1]])
    plt.figure(1)
    sb.set_style('darkgrid')
    plt.bar([0,1], [np.sum([victory_alpha_beta[i][0] for i in range(len(victory_alpha_beta))]),
                    np.sum([victory_uct[i][0] for i in range(len(victory_uct))])],
                    color='r')
    plt.xticks([0, 1], ('AlphaBeta with Memory', 'UCT Search'))
    plt.title('Number of games won')
    plt.show()

    plt.figure(2)
    sb.set_style('darkgrid')
    plt.plot([victory_alpha_beta[i][1] for i in range(len(victory_alpha_beta))], label='Alpha Beta method tiles')
    plt.plot([victory_uct[i][1] for i in range(len(victory_uct))], label='UCT Search method tiles')
    plt.title('Number of tile per party for each method')
    plt.legend()
    plt.show()

    plt.figure(3)
    sb.set_style('darkgrid')
    plt.plot([victory_alpha_beta[i][2] for i in range(len(victory_alpha_beta))], label='Time to play AlphaBeta method')
    plt.plot([victory_uct[i][2] for i in range(len(victory_uct))], label='Time to play UCT Search method')
    plt.title('Move time per method per party')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    random_vs_heuristic()
    random_vs_uct()
    alpha_beta_vs_uct()