from constants import pawntable, knightstable, bishopstable, bookstable, rookstable, queenstable, kingstable
import chess

class Agent():
    def __init__(self, board: chess.Board, color: chess.Color, maxDepth: int):
        self.board = board
        self.color = color
        self.maxDepth = maxDepth

    def getMove(self):
        bestMove = chess.Move.null
        bestScore = float('-inf')
        for move in self.board.legal_moves:
            self.board.push(move)
            score = -self.algorithm(self.maxDepth)
            self.board.pop()

            if score > bestScore:
                bestScore = score
                bestMove = move

        return bestMove

    def getMoveAB(self):
        bestMove = chess.Move.null
        bestScore = float('-inf')
        for move in self.board.legal_moves:
            self.board.push(move)
            score = -self.algorithm(self.maxDepth, float('-inf'), float('inf'))
            self.board.pop()

            if score > bestScore:
                bestScore = score
                bestMove = move

        return bestMove

    def algorithm():
        print('NOT IMPLEMENTED')

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