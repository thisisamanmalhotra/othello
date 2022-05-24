from OthelloPosition import OthelloPosition
from AlphaBetaAlgo import *
import time
import sys


def othel(limit, board):
    global depth, othello, AlphaBeta        # initializing global variables

    othello = OthelloPosition(board)        # declaration of an othello instance with the board

    AlphaBeta = AlphaBetaAlgo()             # declaration of an AlphaBetaAlgo instance

    game = 1                                # game mode : 1 for itchy server mode, 2 for console mode 

    limit = limit/2                         # time limit divided by 2 to get smoother results

    if board == '':                         # if the board is empty we initialize one with default values
        othello.initialize()

    ok = True                               # game variable, goes to false after the player is done.

    while ok is True:
        listmv = []                         # list for the available moves

        moves, coord = othello.get_moves()              # we are getting every available moves for the player with the actual board

        for i in moves:
            listmv.append(i.print_move())               # append all those moves into the list

        if len(listmv) == 0:                            # if the list is empty the player can't play then he passes on
            print("pass")
            othello.change_player()
            ok = False

        else:
            if othello.to_move() == 'B' or game == 1:       # if game mode 1 or if game mode 2 and it is the Computer's turn (computer plays as black)
                
                start_time = time.time()                    # get the start time of the play

                final = 0                                   # variable to check the time
                depth = 0                                   # variable to check the depth
                choice = 0                                  # variable to get the final choice
                tree = 0                                    # variable to get the iterative tree

                if len(listmv) > 1:                         # if we have several moves available
                    
                    check = True                            # boolean to check if we went over the time limit
                    
                    while check is True:                    # loop for iterative search with varaible depth every time
                        tree = iterative_search(depth, othello, start_time, limit)       # go in the itertive search at depth 
                        depth += 1                                                      # add another depth for next search to go deeper
                        final = (round(time.time(), 1)) - (round(start_time, 1))        # check the actual time after search
                       
                        if final > limit:                           # if we don't have more time
                            check = False                           # check is flase and we leave the loop

                    choice = AlphaBeta.set_search_depth(tree)       # we then send the tree into AlphaBetaAlgo to get the choice             
                
                finalmove = listmv[choice]                          # we choose the final choice

                print('({},{})'.format(finalmove[0], finalmove[1]))     # we print it so that the server bash understands it

                othello.change_player()                             # we change the player

                if game == 1:
                    ok = False                                  # we get out of the main loop if game mode 1

                else:                                           # if game mode 2 we check if the player won
                    if othello.win() == 1:                              
                        ok = False

            else:                                       # if game mode 2 (it a human playing than)
                start_time = time.time()                # get the start time of the play

                clone = othello.clone()                 # we clone the game to manipulate it

                for i in range(len(listmv)):            # we can display the available moves on the board for the human to play 
                    print(i + 1, ' : ', listmv[i])
                    nb = '{}'.format(i + 1)
                    clone.show_moves(listmv[i], nb)

                clone.print_board()                     # we then print the clone board

                check = False                           # variable to check if the selected move is available

                while check is False:
                    c = int(input("Please select your play according to the available mooves : "))      # input the desired move
                    c = c - 1

                    if listmv[c]:
                        check = True

                finalmove = listmv[c]

                othello.make_move([finalmove[0], finalmove[1]], coord[c], 0)

                final = (round(time.time(), 1)) - (round(start_time, 1))

                print('the {} player plays on {} in less than {} seconds'.format(othello.to_move(), finalmove, final))

                othello.print_board()

                othello.change_player()

        # if othello.win() == 1:
        #     ok = False


def iterative_search(dth, othel, start_time, limit):
    global score                        # global variable score 
    listmv = []                         # list of moves
    tabscore = []                       # array for the iterative tree
    moves, coord = othel.get_moves()    # getting the availabole moves with the given board

    for j in moves:
        listmv.append(j.print_move())   # append moves to list

    if len(listmv) >= 1:                # if 1 move or more 
        for i in range(len(listmv)):                # loop in the list of moves
            if dth > 0:                             # if depth is higher than 0 (0 being last depth)
                tmpoth = othel.clone()              # clone the board
                move = listmv[i]                    
                tmpoth.make_move(move, coord[i], 0) # make the move on the cloned board with no evaluator
                tmpoth.change_player()              # change player

                dth = dth - 1                       # go down one depth

                tabsc = iterative_search(dth, tmpoth, start_time, limit)    # call again the iterative search with new board

                if len(tabsc) != 0:             # if return different from 0 
                    tabscore.append(tabsc)      # append array to tabscore
                else:
                    score = tmpoth.make_move(move, coord[i], AlphaBeta.set_evaluator()) # get score of the move with evaluator
                    tabscore.append(score)      # append score to tabscore

                dth = dth + 1                   # go up one depth

            elif dth == 0:                      # when reached last depth 
                tmpoth = othel.clone()          # clone board
                move = listmv[i]
                score = tmpoth.make_move(move, coord[i], AlphaBeta.set_evaluator()) # get score of the move with evaluator
                tabscore.append(score)          # append score to tab score

    return tabscore             # return tabscore

if __name__ == "__main__":                      # main calling the function
    othel(float(sys.argv[2]), sys.argv[1])      # call of othel with given parameters