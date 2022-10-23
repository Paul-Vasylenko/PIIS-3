import chess

class AIEngine:

    def __init__(self, board: chess.Board, maxDepth, color, method):
        self.board = board
        self.maxDepth = maxDepth
        self.color = color
        if method == "negamax":
            self.getBestMove = self.negaMax

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
        return compt

    def negaMax(self, depth):
        bestMove = chess.Move.null()
        bestValue = float('-inf')
        if (depth == self.maxDepth):
            return self.evaluate()
        for move in self.board.legal_moves:
            self.board.push(move)
            boardValue = -self.minimax(depth + 1)
            if boardValue > bestValue:
                bestValue = boardValue
                bestMove = move
            self.board.pop()
        return bestMove

    def minimax(self, depth):
        bestscore = float('-inf')
        if (depth == self.maxDepth):
            return self.evaluate()
        for move in self.board.legal_moves:
            self.board.push(move)
            score = -self.minimax(depth + 1)
            self.board.pop()
            if (score > bestscore):
                bestscore = score
        return bestscore

class GameEngine:
    def __init__(self, board: chess.Board):
        self.board = board

    def playHumanMove(self):
        print("Possible moves: ", self.board.legal_moves)
        play = input("Enter your move: ")
        
        self.board.push_san(play)

    def playAIMove(self, maxDepth, color, method):
        engine = AIEngine(self.board, maxDepth, color, method)
        bestMove = engine.getBestMove(0)
        print('BEST MOVE', bestMove)
        self.board.push(bestMove)
        return

    def startGame(self, method):
        aiColor = chess.BLACK
        print("The game started!")
        print("You play WHITE!")
        maxDepth = 3
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
                self.playAIMove(maxDepth, aiColor, method)
                turn = chess.WHITE
                continue
        return

game = GameEngine(chess.Board())
print("Possible methods: negamax, negascout, vps. negamax is default")
method = input("Choose method: ")
method = method if method else "negamax"
if method != "negamax" and method != "negascout" and method != "vps":
    print("Wrong method")
    exit()
print("You choosed method", method)
game.startGame(method)
