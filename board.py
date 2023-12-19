class Connect4:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        self.clear()
        
    def __repr__(self):
        s = ""

        for row in range(self.height):
            s += "|"
            for col in range(self.width):
                s += self.data[row][col] + "|"
            s += "\n"

        s += "-" + "--" * self.width
        s += "\n "

        for col in range(self.width):
            s += str(col % 10) + " "

        return s

    def addMove(self, col, ox):
        if self.allowsMove(col):
            for row in range(self.height):
                if self.data[row][col] != " ":
                    self.data[row-1][col] = ox
                    return
                if row == self.height-1:
                    self.data[row][col] = ox

    def delMove(self, col):
        for row in range(self.height):
            if self.data[row][col] != " ":
                self.data[row][col] = " "
                return

    def allowsMove(self, col):
        if 0 <= col < self.width and self.data[0][col] == " ":
            return True
        return False

    def getTopRow(self, col):
        for row in range(self.height):
            if self.data[row][col] != " ":
                return row

    def isFull(self):
        for col in range(self.width):
            if self.allowsMove(col):
                return False
        return True

    def clear(self):
        self.data = []
        for row in range(self.height):
            boardRow = []
            for col in range(self.width):
                boardRow += [' ']
            self.data += [boardRow]

    def winsFor(self, ox):
        if self.width >= 4:
            for row in range(self.height):
                for col in range(self.width-3):
                    if self.data[row][col] == ox and \
                        self.data[row][col+1] == ox and \
                        self.data[row][col+2] == ox and \
                        self.data[row][col+3] == ox:
                        return True

        if self.height >= 4:
            for row in range(self.height-3):
                for col in range(self.width):
                    if self.data[row][col] == ox and \
                        self.data[row+1][col] == ox and \
                        self.data[row+2][col] == ox and \
                        self.data[row+3][col] == ox:
                        return True

        if self.width >= 4 and self.height >=4:
            for row in range(self.height-3):
                for col in range(self.width-3):
                    if self.data[row][col] == ox and \
                        self.data[row+1][col+1] == ox and \
                        self.data[row+2][col+2] == ox and \
                        self.data[row+3][col+3] == ox:
                        return True

        if self.width >= 4 and self.height >=4:
            for row in range(self.height-3):
                for col in range(3-self.width, 0):
                    if self.data[row][col] == ox and \
                        self.data[row+1][col-1] == ox and \
                        self.data[row+2][col-2] == ox and \
                        self.data[row+3][col-3] == ox:
                        return True

        return False