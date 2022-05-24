from OthelloAlgorithm import OthelloAlgorithm
from HeuristicEvaluator import HeuristicEvaluator


class AlphaBetaAlgo(OthelloAlgorithm):
    def __init__(self):
        self.root = 0
        self.pruned = 0
        self.evaluator = HeuristicEvaluator()

    def set_evaluator(self):
        return self.evaluator

    def evaluate(self, branch, depth, alpha, beta):
        global tree

        i = 0

        for child in branch:
            if type(child) is list:
                (nalpha, nbeta) = self.evaluate(child, depth + 1, alpha, beta)
                if depth % 2 == 1:
                    beta = nalpha if nalpha < beta else beta
                else:
                    alpha = nbeta if nbeta > alpha else alpha

                branch[i] = alpha if depth % 2 == 0 else beta
                i += 1

            else:

                if depth % 2 == 0 and alpha < child:
                    alpha = child

                if depth % 2 == 1 and beta > child:
                    beta = child

                if alpha > beta:
                    self.pruned += 1
                    break

        if depth == self.root:
            tree = alpha if self.root == 0 else beta

        return (alpha, beta)

    def set_search_depth(self, tree, lower=-10000, upper=10000):
        start = self.root

        (alpha, beta) = self.evaluate(tree, start, lower, upper)

        choice = tree.index(alpha)

        return choice
