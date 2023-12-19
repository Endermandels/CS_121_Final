from time import sleep
from tkinter import *
import board
import sys
import ai

class GUI:
	def __init__(self, window):
		self.window = window
		self.width = 900
		self.height = 800
		self.wBuffer = 0
		self.hBuffer = 100
		self.boardWidth = self.width - 2*self.wBuffer
		self.boardHeight = self.height - 2*self.hBuffer
		window.resizable(False, False)

		self.gamemode = "pvp"
		self.columns = 7
		self.rows = 6
		self.b = board.Connect4(self.columns, self.rows)
		self.ply = IntVar()
		self.tbtOptions = ["Left", "Random", "Right"]
		self.tbt = StringVar()
		self.tbt.set(self.tbtOptions[0])
		self.aiO = ai.Player("o", self.tbt.get(), int(self.ply.get()))
		self.aiX = ai.Player("x", self.tbt.get(), int(self.ply.get()))
		self.checker = "x"

		self.circles = []
		self.colors = ["#ff0000", "#d030df", "#000000"]
		self.selectCircle = None

		divisor = -1
		if self.columns > self.rows:
			divisor = self.columns
		else:
			divisor = self.rows
		if self.boardWidth < self.boardHeight:
			self.diameter = self.boardWidth / divisor - 40/self.columns
		else:
			self.diameter = self.boardHeight / divisor - 40/self.rows

		self.canvas = Canvas(window, height=self.height, width=self.width, \
			bg="#d030df")
		self.canvas.bind("<Button-1>", self.mouseInput)
		self.canvas.bind("<Motion>", self.mouseMotion)
		self.canvas.pack()
		self.createBoard()


		self.names = ["Orc", "Goblin", "Bard", "Knight", "Archer", "Thief", \
			"Sorcerer"]
		self.aiName = StringVar()
		self.aiName.set(self.names[0])

		self.quitBtn = Button(window, text="Quit", command=self.quitProgram)
		self.quitBtn.place(x=self.width-100, y=self.height-85)

		self.pvpBtn = Button(window, text="Player v Player", \
			command=lambda: self.restart("pvp"))
		self.pvpBtn.place(x=280, y=2)

		self.pvaBtn = Button(window, text="Player v {}".format(
			self.aiName.get()), command=lambda: self.restart("pva"))
		self.pvaBtn.place(x=280, y=35)

		self.avaBtn = Button(window, text="{} v {}".format(self.aiName.get(), \
			self.aiName.get()), command=lambda: self.restart("ava"))
		self.avaBtn.place(x=280, y=68)

		self.difficultySldr = Scale(window, label="Ply", \
			command=self.updatePly, orient=HORIZONTAL, to=6)
		self.difficultySldr.place(x=500, y=10)

		self.tbtSldr = Scale(
			window, label="Tie Break Type: Left, Random, Right", \
			command=self.updateTBT, orient=HORIZONTAL, to=2, length=220,\
			showvalue=False)
		self.tbtSldr.place(x=640, y=20)

		self.messageSize = 18
		self.message = self.canvas.create_text(
			self.messageSize, self.height-self.messageSize-30, \
			text="Welcome to Connect4! Click on a column\nto place" +
				" a chip.", anchor="w", font="Courier 24 bold")

		self.sideTxt = self.canvas.create_text(135, 45, text="Select game " +
			"type\n  to start a new game\nAI ranges from Orc to Sorcerer\n" +
			"AI's difficulty measured in ply\nAI defaults to tie break type", \
			font="Courier 10")

	def updateMessage(self, s):
		self.canvas.itemconfig(self.message, text=s)

	def switchChecker(self):
		if self.checker == "x":
		    self.checker = "o"
		else:
		    self.checker = "x"

	def determinePlayer(self, ox):
		if ox == "x":
			return "Red"
		return "Black"

	def determineColor(self, ox):
		if ox == "x":
			return self.colors[0]
		elif ox == "o":
			return self.colors[-1]
		else:
			return self.colors[1]

	def recolorCircle(self, col, ox):
		self.canvas.itemconfig(self.circles[self.b.getTopRow(col)][col], \
			fill=self.determineColor(ox))

	def updateSelectCircle(self, x, y, xBuffer=10, yBuffer=10):
		if self.selectCircle != None:
			self.canvas.delete(self.selectCircle)
		self.selectCircle = self.canvas.create_oval(
			x+xBuffer, y+yBuffer, x+xBuffer + self.diameter, \
			y+yBuffer + self.diameter, fill=self.determineColor(self.checker))

	def createBoard(self):
		self.circles = []
		self.canvas.create_rectangle(self.wBuffer, self.hBuffer, \
			self.width-self.wBuffer, self.height-self.hBuffer, fill="#0000ff")

		y = (self.boardHeight/self.rows - self.diameter)/2
		for row in range(self.rows):
			circleRow = []
			x = (self.boardWidth/self.columns - self.diameter)/2
			for col in range(self.columns):
				color = self.determineColor(self.b.data[row][col])
				circleRow += [self.canvas.create_oval(x + self.wBuffer, \
					y + self.hBuffer, x + self.wBuffer + self.diameter, \
					y + self.hBuffer + self.diameter, fill=color)]
				x += self.boardWidth/self.columns
			y += self.boardHeight/self.rows
			self.circles += [circleRow]

	def dropChip(self, col):
		self.b.addMove(col, self.checker)
		self.recolorCircle(col, self.checker)
		self.switchChecker()

	def checkEndGame(self, xName, oName):
		if self.b.winsFor("x"):
			self.updateMessage("Congratulations! {} Wins!".format(xName))
		elif self.b.winsFor("o"):
			self.updateMessage("Congratulations! {} Wins!".format(oName))
		elif self.b.isFull():
			self.updateMessage("Tie! The Board Is Full.")
		else:
			return
		self.gamemode = "choose"

	def mouseMotion(self, event):
		self.updateSelectCircle(event.x, event.y)

	def mouseInput(self, event):
		if self.gamemode == "pvp":
			if not event.x-self.wBuffer < 0:
				col = int((event.x-self.wBuffer)*self.columns/self.boardWidth)
			else:
				col = -1

			if self.b.allowsMove(col):
				self.dropChip(col)
				self.updateSelectCircle(event.x, event.y)
			else:
				self.updateMessage("Invalid move: Either the column is full" +
	                "\nor the input is outside the range of columns.")
				return
			
			self.updateMessage(
				"Player {}'s Turn".format(self.determinePlayer(self.checker)))
			self.checkEndGame("Player Red", "Player Black")

		elif self.gamemode == "pva":
			self.updateMessage("Player's Turn")
			
			if self.checker == "x":
				if not event.x-self.wBuffer < 0:
					col = int(
						(event.x-self.wBuffer)*self.columns/self.boardWidth)
				else:
					col = -1

				if self.b.allowsMove(col):
					self.dropChip(col)
					self.updateSelectCircle(event.x, event.y)
					self.window.update()
				else:
					self.updateMessage("Invalid move: Either the column is " +
		                "full\nor the input is outside the range of columns.")
					return
			
			self.updateMessage("{}'s Turn".format(self.aiName.get()))
			self.window.update()

			if self.checker == "o" and not self.b.winsFor("x") \
				and not self.b.isFull():
				self.dropChip(self.aiO.nextMove(self.b))
				self.canvas.itemconfig(self.selectCircle, \
					fill=self.determineColor(self.checker))
				sleep(0.1)

			self.updateMessage("Player's Turn")
			self.checkEndGame("Player", self.aiName.get())

	def ava(self):
		if self.checker == "x":
			self.updateMessage("{} Red's Turn".format(self.aiName.get()))
			self.window.update()
			self.dropChip(self.aiX.nextMove(self.b))
			self.canvas.itemconfig(self.selectCircle, \
				fill=self.determineColor(self.checker))
			sleep(0.1)
		else:
			self.updateMessage("{} Black's Turn".format(self.aiName.get()))
			self.window.update()
			self.dropChip(self.aiO.nextMove(self.b))
			self.canvas.itemconfig(self.selectCircle, \
				fill=self.determineColor(self.checker))
			sleep(0.1)

		self.checkEndGame(self.aiName.get() + " Red", self.aiName.get() +
			" Black")
		self.window.update()

	def updateTBT(self, value):
		self.tbt.set(self.tbtOptions[int(value)])
		self.aiO = ai.Player("o", self.tbt.get(), self.ply.get())
		self.aiX = ai.Player("x", self.tbt.get(), self.ply.get())

	def updatePly(self, value):
		self.ply.set(value)
		self.aiO = ai.Player("o", self.tbt.get(), self.ply.get())
		self.aiX = ai.Player("x", self.tbt.get(), self.ply.get())
		self.aiName.set(self.names[int(value)])
		self.pvaBtn.config(text="Player v {}".format(self.aiName.get()))
		self.avaBtn.config(
			text="{} v {}".format(self.aiName.get(), self.aiName.get()))

	def restart(self, gmd):
		self.b.clear()
		self.checker = "x"
		self.gamemode = gmd
		self.createBoard()
		if gmd == "pvp":
			self.updateMessage("Player Red's Turn")
		elif gmd == "pva":
			self.updateMessage("Player's Turn")
		while self.gamemode == "ava":
			self.ava()

	def quitProgram(self):
		self.window.destroy()

def main():
	sys.setrecursionlimit(10000)
	root = Tk()
	root.title("Connect 4")
	gui = GUI(root)
	root.mainloop()

if __name__ == '__main__':
	main()
