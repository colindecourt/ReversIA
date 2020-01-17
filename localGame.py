import Reversi
import myPlayerAlphaBeta
import myPlayerBasic
import  myPlayerUCTSearch
import time
from io import StringIO
import sys


def run_local_game(ai1, ai2, board_size = 10):
    '''

    :param ai1: first AI type
    :param ai2: second AI type
    :param board_size: Size of de board - Default is 10x10
    :return: Winner, number of white and black tiles
    '''
    b = Reversi.Board(board_size)

    players = []
    player1 = ai1.myPlayer()
    print('Player 1 uses', player1._my_ai)
    # player1 = myPlayer.myPlayer()
    player1.newGame(b._BLACK)
    players.append(player1)
    player2 = ai2.myPlayer()
    print('Player 2 uses', player2._my_ai)
    player2.newGame(b._WHITE)
    players.append(player2)

    totalTime = [0, 0] # total real time for each player
    nextplayer = 0
    nextplayercolor = b._BLACK
    nbmoves = 1

    outputs = ["", ""]
    sysstdout= sys.stdout
    stringio = StringIO()

    print(b.legal_moves())
    while not b.is_game_over():
        print("Referee Board:")
        print(b)
        print("Before move", nbmoves)
        print("Legal Moves: ", b.legal_moves())
        nbmoves += 1
        otherplayer = (nextplayer + 1) % 2
        othercolor = b._BLACK if nextplayercolor == b._WHITE else b._WHITE

        currentTime = time.time()
        #sys.stdout = stringio
        move = players[nextplayer].getPlayerMove()
        sys.stdout = sysstdout
        playeroutput = "\r" + stringio.getvalue()
        stringio.truncate(0)
        print(("[Player "+str(nextplayer) + "] ").join(playeroutput.splitlines(True)))
        outputs[nextplayer] += playeroutput
        totalTime[nextplayer] += time.time() - currentTime
        print("Player ", nextplayercolor, players[nextplayer].getPlayerName(), "plays" + str(move))
        (x,y) = move
        if not b.is_valid_move(nextplayercolor,x,y):
            print(otherplayer, nextplayer, nextplayercolor)
            print("Problem: illegal move")
            break
        b.push([nextplayercolor, x, y])
        players[otherplayer].playOpponentMove(x,y)

        nextplayer = otherplayer
        nextplayercolor = othercolor

        print(b)

    print("The game is over")
    print(b)

    (nbwhites, nbblacks) = b.get_nb_pieces()
    print("Time:", totalTime)
    print("Winner: ", end="")
    if nbwhites > nbblacks:
        print("WHITE")
        winner = b._WHITE
    elif nbblacks > nbwhites:
        print("BLACK")
        winner = b._BLACK
    else:
        print("DEUCE")
        winner = 0
    player2.endGame(winner)

    return winner, nbwhites, nbblacks, totalTime

if __name__ == '__main__':
    run_local_game(myPlayerUCTSearch, myPlayerAlphaBeta)