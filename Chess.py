import chess
import random as rd
from constants import pawntable, knightstable, bishopstable, bookstable, rookstable, queenstable, kingstable

class AIEngine:

    def __init__(self, board: chess.Board, maxDepth, color):
        self.board = board
        self.maxDepth = maxDepth
        self.color = color

    def evaluate(self):
        board = self.board
        if board.is_checkmate():
            if board.turn:
                return -9999
            else:
                return 9999
        if board.is_stalemate():
            return 0
        if board.is_insufficient_material():
            return 0
        
        wp = len(board.pieces(chess.PAWN, chess.WHITE))
        bp = len(board.pieces(chess.PAWN, chess.BLACK))
        wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
        bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
        wb = len(board.pieces(chess.BISHOP, chess.WHITE))
        bb = len(board.pieces(chess.BISHOP, chess.BLACK))
        wr = len(board.pieces(chess.ROOK, chess.WHITE))
        br = len(board.pieces(chess.ROOK, chess.BLACK))
        wq = len(board.pieces(chess.QUEEN, chess.WHITE))
        bq = len(board.pieces(chess.QUEEN, chess.BLACK))
        
        material = 100*(wp-bp)+320*(wn-bn)+330*(wb-bb)+500*(wr-br)+900*(wq-bq)
        
        pawnsq = sum([pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
        pawnsq= pawnsq + sum([-pawntable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.PAWN, chess.BLACK)])
        knightsq = sum([knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
        knightsq = knightsq + sum([-knightstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.KNIGHT, chess.BLACK)])
        bishopsq= sum([bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
        bishopsq= bishopsq + sum([-bishopstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.BISHOP, chess.BLACK)])
        rooksq = sum([rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)]) 
        rooksq = rooksq + sum([-rookstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.ROOK, chess.BLACK)])
        queensq = sum([queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)]) 
        queensq = queensq + sum([-queenstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.QUEEN, chess.BLACK)])
        kingsq = sum([kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)]) 
        kingsq = kingsq + sum([-kingstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.KING, chess.BLACK)])
    
        eval = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq

        if board.turn:
            return eval
        else:
            return -eval

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
        print(self.board)
        print("WHITE WINS" if turn==chess.BLACK else "BLACK WINS")
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
