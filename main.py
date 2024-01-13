import os
import sys
import tkinter as tk
import tools_2048


class App2048:
	TILE_COLOR = {
		0: "#CDC1B4",
		2: "#EEE4DA",
		4: "#EDE1C9",
		8: "#F3B27A",
		16: "#F69664",
		32: "#F77C5F",
		64: "#F75F3B",
		128: "#EDD074",
		256: "#EDCC62",
		512: "#EDC94F",
		1024: "#EDC541",
		2048: "#EEC22E",
		4096: "#3C3A31",
		8192: "#3C3A31",
		16384: "#3C3A31",
		32768: "#3C3A31",
		65536: "#3C3A31",
		131072: "#3C3A31",
	}
	TILE_FONT = {
		0: "Helvetica 40 bold",
		2: "Helvetica 40 bold",
		4: "Helvetica 40 bold",
		8: "Helvetica 40 bold",
		16: "Helvetica 40 bold",
		32: "Helvetica 40 bold",
		64: "Helvetica 40 bold",
		128: "Helvetica 35 bold",
		256: "Helvetica 35 bold",
		512: "Helvetica 35 bold",
		1024: "Helvetica 25 bold",
		2048: "Helvetica 25 bold",
		4096: "Helvetica 25 bold",
		8192: "Helvetica 25 bold",
		16384: "Helvetica 20 bold",
		32768: "Helvetica 20 bold",
		65536: "Helvetica 20 bold",
		131072: "Helvetica 17 bold",
	}
	TILE_FONT_COLOR = {
		0: "#776E65",
		2: "#776E65",
		4: "#776E65",
		8: "#F9F6F2",
		16: "#F9F6F2",
		32: "#F9F6F2",
		64: "#F9F6F2",
		128: "#F9F6F2",
		256: "#F9F6F2",
		512: "#F9F6F2",
		1024: "#F9F6F2",
		2048: "#F9F6F2",
		4096: "#F9F6F2",
		8192: "#F9F6F2",
		16384: "#F9F6F2",
		32768: "#F9F6F2",
		65536: "#F9F6F2",
		131072: "#F9F6F2",
	}

	def __init__(self):
		self.width = 550
		self.height = 700

		self.game = tools_2048.Game2048(4)

		self.root = tk.Tk()
		self.root.title("2048")
		self.root.config(background="#FAF8EF")
		self.root.geometry(f"{self.width}x{self.height}"
		                   f"+{(self.root.winfo_screenwidth() // 2) - (self.width // 2)}"
		                   f"+{(self.root.winfo_screenheight() // 2) - (self.height // 2)}")
		self.root.resizable(False, False)
		self.root.iconbitmap(self.resource_path("resources/2048-icon.ico"))

		self.title_lbl = tk.Label(self.root, anchor="center", text="2048", font="Helvetica 70 bold",
		                          background="#FAF8EF", foreground="#776E65", highlightthickness=0)
		self.title_lbl.place(x=25, y=35, width=220, height=80)

		self.score_cnv = tk.Canvas(self.root, width=150, height=75, background="#FAF8EF", highlightthickness=0)
		self.score_cnv.place(x=375, y=20, width=150, height=100)
		self.round_rectangle(self.score_cnv, 5, 5, 145, 70, radius=15, steps=100, fill="#BBADA0")
		self.score_cnv.create_text(75, 25, fill="#EDE4DA", font="Helvetica 11 bold", text="SCORE", anchor="center")
		self.score_text = self.score_cnv.create_text(75, 50, fill="#FFFFFF", font="Helvetica 22 bold", text="0", anchor="center")

		self.new_game_cnv = tk.Canvas(self.root, width=150, height=50, background="#FAF8EF", highlightthickness=0, cursor="hand2")
		self.new_game_cnv.place(x=375, y=105, width=150, height=50)
		self.round_rectangle(self.new_game_cnv, 5, 5, 145, 45, radius=15, steps=100, fill="#8F7A66")
		self.new_game_cnv.create_text(75, 25, fill="#F9F6F2", font="Helvetica 14 bold", text="New Game", anchor="center")
		self.new_game_cnv.bind("<ButtonRelease-1>", lambda event: self.new_game())

		self.root.bind("<Key>", self.key_press)
		self.root.bind("<KeyRelease>", self.key_release)
		self.key_state = {
			"Up": False,
			"Down": False,
			"Left": False,
			"Right": False,
		}

		self.field_cnv = tk.Canvas(self.root, background="#FAF8EF", highlightthickness=0)
		self.field_cnv.place(x=0, y=150, width=550, height=550)
		# big rectangle
		self.round_rectangle(self.field_cnv, 25, 25, 525, 525, radius=15, steps=100, fill="#BBADA0")
		# tiles
		self.tiles = []  # (tile_rectangle, tile_text)
		for i in range(41, 404 + 1, 121):
			red = []
			for j in range(41, 404 + 1, 121):
				red.append((
					self.round_rectangle(self.field_cnv, j, i, j + 105, i + 105, radius=8, steps=100, fill="#CDC1B4"),
					self.field_cnv.create_text(j + 52, i + 53, fill="white", font="Helvetica 40 bold", text="", anchor="center"),
				))
			self.tiles.append(red)

		self.status_lbl = tk.Label(self.root, anchor="center", text="", font="Helvetica 30 bold",
		                           background="#FAF8EF", foreground="#ff0000", highlightthickness=0)
		self.status_lbl.place(x=90, y=120, width=260, height=50)

		self.ai_desc = tk.Label(self.root, text="Press space for auto play", font="Helvetica 10 bold",
		                        background="#FAF8EF", foreground="#776E65", highlightthickness=0, anchor="center")
		self.ai_desc.place(x=0, y=self.height - 25, width=self.width, height=25)

		self.update_gui()
		self.root.mainloop()

	def new_game(self):
		self.game = tools_2048.Game2048(4)
		self.update_gui()

	def update_gui(self):
		# update status label
		if self.game.state() == 1:  # game over
			self.status_lbl.config(text="GAME OVER!")
		elif self.game.result() == 1:  # game won
			self.status_lbl.config(text="VICTORY!")
		else:
			self.status_lbl.config(text="")

		# update tiles
		board = self.game.board()
		for i in range(4):
			for j in range(4):
				color = self.TILE_COLOR[board[i][j]]
				self.field_cnv.itemconfig(self.tiles[i][j][0], fill=color)

				if board[i][j] != 0:
					font = self.TILE_FONT[board[i][j]]
					font_color = self.TILE_FONT_COLOR[board[i][j]]
					self.field_cnv.itemconfig(self.tiles[i][j][1], text=str(board[i][j]), font=font, fill=font_color)
				else:
					self.field_cnv.itemconfig(self.tiles[i][j][1], text="")

		# update score
		self.score_cnv.itemconfig(self.score_text, text=str(self.game.score()))

		self.root.update_idletasks()

	def key_press(self, key):
		# 0: left, 1: right, 2: up, 3: down
		if self.game.state() != 1:  # game not over
			move_success = False
			match key.keysym:
				case "Up":
					if not self.key_state["Up"]:
						self.key_state["Up"] = True
						move_success = self.game.make_move(2)
				case "Down":
					if not self.key_state["Down"]:
						self.key_state["Down"] = True
						move_success = self.game.make_move(3)
				case "Left":
					if not self.key_state["Left"]:
						self.key_state["Left"] = True
						move_success = self.game.make_move(0)
				case "Right":
					if not self.key_state["Right"]:
						self.key_state["Right"] = True
						move_success = self.game.make_move(1)
				case "space":
					move_success = self.game.make_move(self.game.find_best_move(10_000))
			if move_success:
				self.update_gui()

	def key_release(self, key):
		match key.keysym:
			case "Up":
				self.key_state["Up"] = False
			case "Down":
				self.key_state["Down"] = False
			case "Left":
				self.key_state["Left"] = False
			case "Right":
				self.key_state["Right"] = False

	@staticmethod
	def resource_path(relative_path):
		""" Get absolute path to resource, works for dev and for PyInstaller """
		try:
			# PyInstaller creates a temp folder and stores path in _MEIPASS
			base_path = sys._MEIPASS
		except AttributeError:
			base_path = os.path.abspath(".")
		return os.path.join(base_path, relative_path)

	@staticmethod
	def round_rectangle(canvas, x1, y1, x2, y2, radius, steps, **kwargs):
		points = [x1 + radius, y1,
		          x2 - radius, y1,
		          x2, y1,
		          x2, y1 + radius,
		          x2, y2 - radius,
		          x2, y2,
		          x2 - radius, y2,
		          x1 + radius, y2,
		          x1, y2,
		          x1, y2 - radius,
		          x1, y1 + radius,
		          x1, y1]

		return canvas.create_polygon(points, **kwargs, smooth=True, splinesteps=steps)


def main():
	App2048()


if __name__ == '__main__':
	main()
