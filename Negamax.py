from Agent import Agent


class NegamaxAgent(Agent):
    def algorithm(self, depth):
        if depth == self.maxDepth:
            return self.evaluate()
        bestScore = float('-inf')
        for move in self.board.legal_moves:
            self.board.push(move)
            score = -self.algorithm(depth-1)
            self.board.pop()
            if score > bestScore:
                bestScore = score
        return bestScore 