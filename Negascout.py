from Agent import Agent


class NegascoutAgent(Agent):
    def algorithm(self, depth, alpha, beta):
        a = None
        b = None
        t  = None
        i = None
        if depth == self.maxDepth:
            return self.evaluate()

        a = alpha
        b = beta
        i = 1
        for move in self.board.legal_moves:
            self.board.push(move)
            t = - self.algorithm(depth+1, -b, -a)
            self.board.pop()
            if t > a and t < b and i > 1 and depth < self.maxDepth - 1:
                a = -self.algorithm(depth+1, -beta, -t)
            a = max(a, t)
            if a >= beta:
                return a
            b = a + 1
            i = i + 1