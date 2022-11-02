from Agent import Agent


class PVSAgent(Agent):
    def algorithm(self, depth, alpha, beta):
        if depth == self.maxDepth:
            return self.evaluate()
        bSearchPv = True
        for move in self.board.legal_moves:
            self.board.push(move)
            if (bSearchPv):
                score = -self.algorithm(depth+1, -beta, -alpha)
            else:
                score = -self.algorithm(depth+1, -alpha-1, -alpha)
                if score > alpha:
                    score = -self.algorithm(depth+1, -beta, -alpha)
            self.board.pop()
            
            if score>=beta:
                return beta
            if score>alpha:
                alpha=score
                bSearchPv = False

        return alpha
        