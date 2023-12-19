from random import choice

class Player:
    def __init__(self, ox, tbt, ply):
        self.checker = ox
        self.otherChecker = ""
        self.tieBreakType = tbt
        self.ply = ply

        if self.checker == "o":
            self.otherChecker = "x"
        else:
            self.otherChecker = "o"

    def __repr__(self):
        return "Checker: {} / TieBreakType: {} / Ply: {}".format(
            self.checker, self.tieBreakType, self.ply)

    def nextMove(self, board):
        scores = [-1 for i in range(board.width)]

        for col in range(board.width):
            if board.allowsMove(col):
                board.addMove(col, self.checker)
                if board.winsFor(self.checker):
                    scores[col] = 150
                elif self.ply >= 2:
                    scores[col] = self.scoreFor(board, self.otherChecker, 1)
                else:
                    scores[col] = 50
                board.delMove(col)

        maxValue = max(scores)
        numMaxValues = scores.count(maxValue)
        bingo = 1

        if self.tieBreakType == "Left":
            return scores.index(maxValue)
        elif self.tieBreakType == "Random":
            bingo = choice(range(1, numMaxValues+1))

        for i in range(numMaxValues):
            if i == numMaxValues-bingo:
                return scores.index(maxValue)
            scores.insert(scores.index(maxValue), -100)
            scores.remove(maxValue)

    def scoreFor(self, board, ox, ply):
        scores = [0 for i in range(board.width)]

        if ply == self.ply and ox == self.checker:
            return 50 - board.winsFor(self.otherChecker)*50
        if ply == self.ply and ox == self.otherChecker:
            return 50 + board.winsFor(self.checker)*50
        outOfBounds = 0
        for col in range(board.width):
            if board.allowsMove(col):
                board.addMove(col, ox)
                if ox == self.checker:
                    if board.winsFor(ox):
                        board.delMove(col)
                        return 100
                    scores[col] = self.scoreFor(
                        board, self.otherChecker, ply+1)
                else:
                    if board.winsFor(ox):
                        board.delMove(col)
                        return 0
                    scores[col] = self.scoreFor(board, self.checker, ply+1)
                board.delMove(col)
            elif not board.isFull():
                outOfBounds += 1
            else:
                return 10
        return sum(scores)/(board.width-outOfBounds)