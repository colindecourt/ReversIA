import numpy as np
import copy

CP = 1/np.sqrt(2)

_BLACK = 1
_WHITE = 2

'''
UCT search based from : 
https://www.labri.fr/perso/lsimon/ia-2019/App-Alphago/MCTS-survey.pdf
page 6-7-8-9
'''
class Node:

    def __init__(self, parent, board):
        self.incoming_action = None
        self.total_sim_reward = 0
        self.visit_count = 0
        self.parent = parent
        self.board = board
        self.children = []

    def choose_untried_action(self):
        """
        Choose randomly a move among legal moves
        :return: a new board with the new move
        """
        legal_moves = self.board.legal_moves()
        random_move = np.random.randint(0, len(legal_moves))
        move = legal_moves[random_move]
        new_board = copy.deepcopy(self.board)
        new_board.push(move)
        return new_board, move


def tree_policy(v):
    """
        Get tree policy
    :param v: a node
    :return: a node
    """

    while not v.board.is_game_over():
        if len(v.children) == 0:
            return expand(v)
        else:
            v = best_child(v, CP)
    return v


def expand(v):
    """
        Chose an action among all possible action and return un new node
    :param v: a node
    :return: the new node
    """
    # False : use the state associated to know node (incoming action variable)
    new_board, action = v.choose_untried_action()
    vp = Node(v, new_board)
    print('New node', vp)
    # Add new node to v
    vp.incoming_action = action
    v.children.append(vp)
    return vp


def best_child(v, c=CP):
    """
        Return the move associate to the best child
    :param v: node
    :param c: exploitation parameter = 1/sqrt(2)
    :return: best move
    """
    max_score = -np.inf
    best_node = None
    for vp in v.children:
        score = (vp.total_sim_reward/vp.visit_count)+c*np.sqrt((2*np.log(v.visit_count))/vp.visit_count)
        if score > max_score:
            max_score = score
            best_node = vp
            #print("Best score : ", max_score)
    return best_node

def default_policy(s, color):
    """
    :param s: a state
    :return: reward for state s
    """
    # Use all the possible state
    while not s.is_game_over():
        legal_moves = s.legal_moves()
        random_move = np.random.randint(0, len(legal_moves))
        move = legal_moves[random_move]
        s.push(move)
    score = s.get_nb_pieces()[0] - s.get_nb_pieces()[1]
    return score if color == _BLACK else -score


def backup(v, delta):
    """
        Backpropagation function
    :param v: a node
    :param delta:
    :return: parent of node v
    """
    while v is not None:
        v.visit_count += 1
        v.total_sim_reward = v.total_sim_reward + delta
        v = v.parent


def uct_search(board, color=_WHITE, computational_budget = 100):
    v0 = Node(None, board)
    while computational_budget > 0:
        vl = tree_policy(v0)
        delta = default_policy(vl.board, color)
        backup(vl, delta)
        computational_budget -= 1
    print(v0.children)
    return best_child(v0, 0).incoming_action
