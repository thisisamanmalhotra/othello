import numpy as np
from OthelloAction import OthelloAction


class OthelloPosition(object):
    """
    This class is used to represent game positions. It uses a 2-dimensional char array for the board
    and a Boolean to keep track of which player has the move.

    Author: Ola Ringdahl
    """
    def __init__(self, board_str):
        """
        Creates a new position according to str. If str is not given all squares are set to E (empty)
        :param board_str: A string of length 65 representing the board. The first character is W or B, indicating which
        player is to move. The remaining characters should be E (for empty), O (for white markers), or X (for black
        markers).
        """
        self.BOARD_SIZE = 8
        self.maxPlayer = True
        self.board = np.array([['E' for col in range(self.BOARD_SIZE + 2)] for row in range(self.BOARD_SIZE + 2)])

        if len(list(board_str)) >= 65:
            if board_str[0] == 'W':
                self.maxPlayer = True
            else:
                self.maxPlayer = False
            for i in range(1, len(list(board_str))):
                col = ((i - 1) % 8) + 1
                row = (i - 1) // 8 + 1
                # For convenience we use W and B in the board instead of X and O:
                if board_str[i] == 'X':
                    self.board[row][col] = 'B'
                elif board_str[i] == 'O':
                    self.board[row][col] = 'W'

    def initialize(self):
        """
        Initializes the position by placing four markers in the middle of the board.
        :return: Nothing
        """
        self.board[self.BOARD_SIZE // 2][self.BOARD_SIZE // 2] = 'W'
        self.board[self.BOARD_SIZE // 2 + 1][self.BOARD_SIZE // 2 + 1] = 'W'
        self.board[self.BOARD_SIZE // 2][self.BOARD_SIZE // 2 + 1] = 'B'
        self.board[self.BOARD_SIZE // 2 + 1][self.BOARD_SIZE // 2] = 'B'
        self.maxPlayer = True

    def show_moves(self, moves, i):
        self.board[moves[0], moves[1]] = i

    def make_move(self, action, coord, evaluate):
        """
        Perform the move suggested by the OhelloAction action and return the new position. Observe that this also
        changes the player to move next.
        :param action: The move to make as an OthelloAction
        :return: The OthelloPosition resulting from making the move action in the current position.
        """
        score = -1000

        player = self.to_move()

        self.board[action[0], action[1]] = player

        for coords in coord[1]:
            coordX = action[0]
            coordY = action[1]

            if coords == 1:
                while coordX - 1 > 0 and self.__is_opponent_square(coordX - 1, coordY):
                    coordX -= 1
                    self.board[coordX, coordY] = player

            if coords == 2:
                while coordX - 1 > 0 and coordY + 1 < self.BOARD_SIZE and self.__is_opponent_square(coordX - 1, coordY + 1):
                    coordX -= 1
                    coordY += 1
                    self.board[coordX, coordY] = player

            if coords == 3:
                while coordY + 1 < self.BOARD_SIZE and self.__is_opponent_square(coordX, coordY + 1):
                    coordY += 1
                    self.board[coordX, coordY] = player

            if coords == 4:
                while coordX + 1 < self.BOARD_SIZE and coordY + 1 < self.BOARD_SIZE and self.__is_opponent_square(coordX + 1,
                                                                                                            coordY + 1):
                    coordX += 1
                    coordY += 1
                    self.board[coordX, coordY] = player

            if coords == 5:
                while coordX + 1 < self.BOARD_SIZE and self.__is_opponent_square(coordX + 1, coordY):
                    coordX += 1
                    self.board[coordX, coordY] = player

            if coords == 6:
                while coordX + 1 < self.BOARD_SIZE and coordY - 1 > 0 and self.__is_opponent_square(coordX + 1, coordY - 1):
                    coordX += 1
                    coordY -= 1
                    self.board[coordX, coordY] = player

            if coords == 7:
                while coordY - 1 > 0 and self.__is_opponent_square(coordX, coordY - 1):
                    coordY -= 1
                    self.board[coordX, coordY] = player

            if coords == 8:
                while coordX - 1 > 0 and coordY - 1 > 0 and self.__is_opponent_square(coordX - 1, coordY - 1):
                    coordX -= 1
                    coordY -= 1
                    self.board[coordX, coordY] = player

        if evaluate != 0 and evaluate != 'X':
            score = evaluate.evaluate(self)

        return score

    def get_moves(self):
        """
        Get all possible moves for the current position
        :return: A list of OthelloAction representing all possible moves in the position. If the
        list is empty, there are no legal moves for the player who has the move.
        """
        moves = []
        coord = []
        appmove = moves.append
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                if self.__is_candidate(i + 1, j + 1) and self.__is_move(i + 1, j + 1):
                    appmove(OthelloAction(i + 1, j + 1))
                    coord.append(self.__is_move(i + 1, j + 1))

        return moves, coord

    def __is_candidate(self, row, col):
        """
        Check if a position is a candidate for a move (not empty and has a neighbour)
        :param row: The row of the board position
        :param col: The column of the board position
        :return: True if it is a candidate
        """
        if self.board[row][col] != 'E':
            return False
        if self.__has_neighbour(row, col):
            return True
        return False

    def __is_move(self, row, col):
        """
        Check if it is possible to do a move from this position
        :param row: The row of the board position
        :param col: The column of the board position
        :return: True if it is possible to do a move
        """
        
        check =  False
        poss = []

        
        if row < 1 or row > self.BOARD_SIZE or col < 1 or col > self.BOARD_SIZE:
            return False
        if self.__check_north(row, col):
            check = True
            poss.append(1)
        if self.__check_north_east(row, col):
            check = True
            poss.append(2)
        if self.__check_east(row, col):
            check = True
            poss.append(3)
        if self.__check_south_east(row, col):
            check = True
            poss.append(4)
        if self.__check_south(row, col):
            check = True
            poss.append(5)
        if self.__check_south_west(row, col):
            check = True
            poss.append(6)
        if self.__check_west(row, col):
            check = True
            poss.append(7)
        if self.__check_north_west(row, col):
            check = True
            poss.append(8)

        if check is True:
            return check, poss

    def __check_north(self, row, col):
        """
        Check if it is possible to do a move to the north from this position
        :param row: The row of the board position
        :param col: The column of the board position
        :return: True if it is possible to do a move
        """
        if not self.__is_opponent_square(row - 1, col):
            return False
        i = row - 2
        while i > 0:
            if self.board[i][col] == 'E':
                return False
            if self.__is_own_square(i, col):
                return True
            i -= 1
        return False

    def __check_north_east(self, row, col):
        """
        Check if it is possible to do a move to the north east from this position
        :param row: The row of the board position
        :param col: The column of the board position
        :return: True if it is possible to do a move
        """
        if not self.__is_opponent_square(row - 1, col + 1):
            return False
        i = 2
        while row - i > 0 and col + i <= self.BOARD_SIZE:
            if self.board[row - i][col + i] == 'E':
                return False
            if self.__is_own_square(row - i, col + i):
                return True
            i += 1
        return False

    def __check_north_west(self, row, col):
        """
        Check if it is possible to do a move to the north west from this position
        :param row: The row of the board position
        :param col: The column of the board position
        :return: True if it is possible to do a move
        """
        if not self.__is_opponent_square(row - 1, col - 1):
            return False
        i = 2
        while row - i > 0 and col - i > 0:
            if self.board[row - i][col - i] == 'E':
                return False
            if self.__is_own_square(row - i, col - i):
                return True
            i += 1
        return False

    def __check_south(self, row, col):
        """
        Check if it is possible to do a move to the south from this position
        :param row: The row of the board position
        :param col: The column of the board position
        :return: True if it is possible to do a move
        """
        if not self.__is_opponent_square(row + 1, col):
            return False
        i = row + 2
        while i <= self.BOARD_SIZE:
            if self.board[i][col] == 'E':
                return False
            if self.__is_own_square(i, col):
                return True
            i += 1
        return False

    def __check_south_east(self, row, col):
        """
        Check if it is possible to do a move to the south east from this position
        :param row: The row of the board position
        :param col: The column of the board position
        :return: True if it is possible to do a move
        """
        if not self.__is_opponent_square(row + 1, col + 1):
            return False
        i = 2
        while row + i <= self.BOARD_SIZE and col + i <= self.BOARD_SIZE:
            if self.board[row + i][col + i] == 'E':
                return False
            if self.__is_own_square(row + i, col + i):
                return True
            i += 1
        return False

    def __check_south_west(self, row, col):
        """
        Check if it is possible to do a move to the south west from this position
        :param row: The row of the board position
        :param col: The column of the board position
        :return: True if it is possible to do a move
        """
        if not self.__is_opponent_square(row + 1, col - 1):
            return False
        i = 2
        while row + i <= self.BOARD_SIZE and col - i > 0:
            if self.board[row + i][col - i] == 'E':
                return False
            if self.__is_own_square(row + i, col - i):
                return True
            i += 1
        return False

    def __check_west(self, row, col):
        """
        Check if it is possible to do a move to the west from this position
        :param row: The row of the board position
        :param col: The column of the board position
        :return: True if it is possible to do a move
        """
        if not self.__is_opponent_square(row, col - 1):
            return False
        i = col - 2
        while i > 0:
            if self.board[row][i] == 'E':
                return False
            if self.__is_own_square(row, i):
                return True
            i -= 1
        return False

    def __check_east(self, row, col):
        """
        Check if it is possible to do a move to the east from this position
        :param row: The row of the board position
        :param col: The column of the board position
        :return: True if it is possible to do a move
        """
        if not self.__is_opponent_square(row, col + 1):
            return False
        i = col + 2
        while i <= self.BOARD_SIZE:
            if self.board[row][i] == 'E':
                return False
            if self.__is_own_square(row, i):
                return True
            i += 1
        return False

    def __is_opponent_square(self, row, col):
        """
        Check if the position is occupied by the opponent
        :param row: The row of the board position
        :param col: The column of the board position
        :return: True if opponent square
        """
        if self.maxPlayer and self.board[row][col] == 'B':
            return True
        if not self.maxPlayer and self.board[row][col] == 'W':
            return True
        return False

    def __is_own_square(self, row, col):
        """
        Check if the position is occupied by the player
        :param row: The row of the board position
        :param col: The column of the board position
        :return: True if it's your own square
        """
        if not self.maxPlayer and self.board[row][col] == 'B':
            return True
        if self.maxPlayer and self.board[row][col] == 'W':
            return True
        return False

    def __has_neighbour(self, row, col):
        """
        Check if the position has any non-empty squares
        :param row: The row of the board position
        :param col: The column of the board position
        :return: True if has neighbours
        """
        if self.board[row - 1][col] != 'E':
            return True
        if self.board[row - 1, col + 1] != 'E':
            return True
        if self.board[row - 1][col - 1] != 'E':
            return True
        if self.board[row][col - 1] != 'E':
            return True
        if self.board[row][col + 1] != 'E':
            return True
        if self.board[row + 1][col - 1] != 'E':
            return True
        if self.board[row + 1][col + 1] != 'E':
            return True
        if self.board[row + 1][col] != 'E':
            return True
        return False

    def to_move(self):
        """
        Check which player's turn it is
        :return: True if the first player (white) has the move, otherwise False
        """

        player = self.maxPlayer
        if player is True:
            player = 'W'
        else:
            player = 'B'

        return player

    def clone(self):
        """
        Copy the current position
        :return: A new OthelloPosition, identical to the current one.
        """
        ot = OthelloPosition("")
        ot.board = np.copy(self.board)
        ot.maxPlayer = self.maxPlayer
        return ot

    def print_board(self):
        """
        Prints the current board. Do not use when running othellostart (it will crash)
        :return: Nothing
        """
        print(" ___ ___ ___ ___ ___ ___ ___ ___ ")
        for row in range(1, self.BOARD_SIZE+1):
            print("|   |   |   |   |   |   |   |   |")
            for col in range(0, self.BOARD_SIZE+1):
                if col == 0:
                    a = 1
                else:
                    if self.board[row][col] == 'E':
                        print("|   ", end='')
                    elif self.board[row][col] == 'W':
                        print("| W ", end='')
                    elif self.board[row][col] == 'B':
                        print("| B ", end='')
                    else:
                        print("| {} ".format(self.board[row][col]), end='')
                    if col == self.BOARD_SIZE:
                        print("|")

            print("|___|___|___|___|___|___|___|___|")

    def change_player(self):
        """
        Changes the player at each round
        :return: Nothing
        """
        if self.maxPlayer is True:
            self.maxPlayer = False

        else:
            self.maxPlayer = True

    def win(self):
        black_squares = 0
        white_squares = 0
        for row in self.board:
            for item in row:
                if item == 'W':
                    white_squares += 1
                if item == 'B':
                    black_squares += 1

        if white_squares + black_squares == 64 or white_squares == 0 or black_squares == 0:
            if white_squares - black_squares > 0:
                print("The white player wins !!")
            elif white_squares - black_squares == 0:
                print("Egality")
            else:
                print("The black player wins !!")

            print("score is : {}W to {}B ".format(white_squares, black_squares))

            return 1

        print("score is : {}W to {}B ".format(white_squares, black_squares))



