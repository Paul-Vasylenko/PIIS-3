import chess
from Negamax import NegamaxAgent
from Negascout import NegascoutAgent
from PVS import PVSAgent


class GameEngine:
    def __init__(self, board: chess.Board):
        self.board = board

    def playHumanMove(self):
        print("Possible moves: ", self.board.legal_moves)
        play = input("Enter your move: ")
        
        self.board.push_san(play)

    def playAIMove(self, maxDepth, color, method):
        if(method=='negamax'):
            negamax = NegamaxAgent(self.board, color, maxDepth)
            bestMove = negamax.getMove()
        elif(method=='negascout'):
            negascout = NegascoutAgent(self.board, color, maxDepth)
            bestMove = negascout.getMoveAB()
        else:
            pvs = PVSAgent(self.board, color, maxDepth)
            bestMove = pvs.getMoveAB()
            
            
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
