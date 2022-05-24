from OthelloEvaluator import OthelloEvaluator


class HeuristicEvaluator(OthelloEvaluator):
    def __init__(self):
        SQUARE_WEIGHTS = [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 120, -20, 20, 10, 10, 20, -20, 120, 0,
            0, -20, -25, -5, -5, -5, -5, -25, -20, 0,
            0, 20, -5, 15, 3, 3, 15, -5, 20, 0,
            0, 10, -5, 3, 3, 3, 3, -5, 10, 0,
            0, 10, -5, 3, 3, 3, 3, -5, 10, 0,
            0, 20, -5, 15, 3, 3, 15, -5, 20, 0,
            0, -20, -25, -5, -5, -5, -5, -25, -20, 0,
            0, 120, -20, 20, 10, 10, 20, -20, 120, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        ]

        self.tab = []
        i = 0
        j = 10
        for k in range(10):
            self.tab.append(SQUARE_WEIGHTS[i:j])
            i += 10
            j += 10

    def evaluate(self, othello):
        player = othello.to_move()
        opp = str
        if player == 'W':
            opp = 'B'
        else:
            opp = 'W'

        board = othello.board
        total = 0
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == player:
                    total += self.tab[i][j]
                elif board[i][j] == opp:
                    total -= self.tab[i][j]

        return total

    def squares(self):
        return [i for i in range(11, 89) if 1 <= (i % 10) <= 8]