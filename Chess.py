import chess
import random as rd

class AIEngine:

    def __init__(self, board: chess.Board, maxDepth, color):
        self.board = board
        self.maxDepth = maxDepth
        self.color = color

    def estimatePieceCost(self, square):
        pieceCost = 0
        pieceType = self.board.piece_type_at(square)
        if (pieceType == chess.PAWN):
            pieceCost = 1
        if (pieceType == chess.ROOK):
            pieceCost = 5.1
        if (pieceType == chess.BISHOP):
            pieceCost = 3.33
        if (pieceType == chess.KNIGHT):
            pieceCost = 3.2
        if (pieceType == chess.QUEEN):
            pieceCost = 8.8

        if (self.board.color_at(square)!=self.color):
            return -pieceCost
        return pieceCost

    def evaluate(self):
        compt = 0
        #Sums up the material values
        for i in range(64):
            compt+=self.estimatePieceCost(chess.SQUARES[i])
        compt += self.mateOpportunity() + self.openning() + 0.001*rd.random()
        return compt

    def negaMax(self, depth):
        bestMove = chess.Move.null()
        bestValue = float('-inf')
        if (depth == self.maxDepth):
            return [self.evaluate()]
        for move in self.board.legal_moves:
            self.board.push(move)
            result = self.negaMax(depth + 1)
            boardValue = -result[0]
            if boardValue > bestValue:
                bestValue = boardValue
                bestMove = move
            self.board.pop()
        return [bestValue, bestMove]
    
    def negaScout(self, depth, alpha, beta):
        bestMove = chess.Move.null()
        bestValue = float('-inf')
        if (depth == self.maxDepth):
            return [self.evaluate()]
        for move in self.board.legal_moves:
            self.board.push(move)
            result = self.negaScout(depth + 1, -(alpha+1), -alpha)
            boardValue = -result[0]
            if (boardValue > alpha and boardValue < beta and depth != self.maxDepth-1):
                result2 = self.negaScout(depth+1, -beta, -boardValue)
                boardValue = max(boardValue, -result2[0])
            if boardValue > bestValue:
                bestValue = boardValue
                bestMove = move
            self.board.pop()
        return [bestValue, bestMove]

    def pvs(self, depth, alpha, beta):
        bestMove = chess.Move.null()
        bestValue = float('-inf')
        if (depth == self.maxDepth):
            return [self.evaluate()]
        for move in self.board.legal_moves:
            self.board.push(move)
            result = self.pvs(depth + 1, -(alpha+1), -alpha)
            boardValue = -result[0]
            if (boardValue > alpha and boardValue < beta):
                result2 = self.pvs(depth+1, -beta, -alpha)
                boardValue = -result2[0]
            if boardValue > bestValue:
                bestValue = boardValue
                bestMove = move
            self.board.pop()
        return [bestValue, bestMove]

    def mateOpportunity(self):
        if (self.board.legal_moves.count()==0):
            if (self.board.turn == self.color):
                return -999
            else:
                return 999
        else:
            return 0

    #to make the engine developp in the first moves
    def openning(self):
        if (self.board.fullmove_number<10):
            if (self.board.turn == self.color):
                return 1/30 * self.board.legal_moves.count()
            else:
                return -1/30 * self.board.legal_moves.count()
        else:
            return 0

class GameEngine:
    def __init__(self, board: chess.Board):
        self.board = board

    def playHumanMove(self):
        print("Possible moves: ", self.board.legal_moves)
        play = input("Enter your move: ")
        
        self.board.push_san(play)

    def playAIMove(self, maxDepth, color, method, alpha, beta):
        engine = AIEngine(self.board, maxDepth, color)
        if(method=='negamax'):
            bestMove = engine.negaMax(0)[1]
        elif(method=='negascout'):
            bestMove = engine.negaScout(0, alpha, beta)[1]
        else:
            bestMove = engine.pvs(0, alpha, beta)[1]
            
            
        print('BEST MOVE', bestMove)
        self.board.push(bestMove)
        return

    def startGame(self, method):
        aiColor = chess.BLACK
        print("The game started!")
        print("You play WHITE!")
        maxDepth = 3
        alpha = float('-inf')
        beta = float('inf')
        turn = chess.WHITE
        while (not self.board.is_checkmate()):
            print(self.board)
            if turn == chess.WHITE:
                print('\n\nWhite move\n\n')
                self.playHumanMove()
                turn = chess.BLACK
                continue
            if turn == chess.BLACK:
                print('\n\nBlack move\n\n')
                self.playAIMove(maxDepth, aiColor, method, alpha, beta)
                turn = chess.WHITE
                continue
        return

    

game = GameEngine(chess.Board())
print("Possible methods: negamax, negascout, pvs. negamax is default")
method = input("Choose method: ")
method = method if method else "negamax"
if method != "negamax" and method != "negascout" and method != "pvs":
    print("Wrong method")
    exit()
print("You choosed method", method)
game.startGame(method)
