import os
import random
import sys
from tkinter import *


def deep_copy(lista: list):
	temp_list = []
	for x in lista:
		try:
			len(x)
			temp_list.append(deep_copy(x))
		except TypeError:
			temp_list.append(x)
	return temp_list

def resource_path(relative_path):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except AttributeError:
		base_path = os.path.abspath(".")
	return os.path.join(base_path, relative_path)

def round_rectangle(lokacija, x1, y1, x2, y2, radius, steps, **kwargs):
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

	return lokacija.create_polygon(points, **kwargs, smooth=True, splinesteps=steps)

def spawn_rnd(ploca):
	spawn_places = []
	for x in range(4):
		for y in range(4):
			if ploca[x][y] == 0:
				spawn_places.append((x, y))
	spawn_place = random.choice(spawn_places)

	ploca[spawn_place[0]][spawn_place[1]] = 2 if random.random() < 0.9 else 4

	return ploca

def victory(ploca):
	for i in ploca:
		if 2048 in i:
			pobjeda.place(x=120, y=120, width=200, height=50)
			return True
	return False

def game_over(ploca, klik_up, klik_down, klik_left, klik_right):
	global won
	if ploca == klik_left == klik_right == klik_up == klik_down:
		if not won:
			poraz.place(x=95, y=120, width=260, height=50)
		return True
	else:
		return False

def calc_moves(ploca):
	# up
	bodovi_up = 0
	stupci = []
	for i in range(4):
		stupac = []
		for j in range(4):
			stupac.append(ploca[j][i])
		stupci.append(stupac)
	for stupac in stupci:
		br_nula = stupac.count(0)
		izbrisano = 0
		for i in range(4):
			if stupac[i - izbrisano] == 0:
				stupac.pop(i - izbrisano)
				izbrisano += 1
		stupac.extend([0 for _ in range(br_nula)])
		for i in range(3):
			if stupac[i] != 0 and stupac[i] == stupac[i + 1]:
				bodovi_up += stupac[i] * 2
				stupac[i] *= 2
				stupac.pop(i + 1)
				stupac.append(0)
	ploca_up = []
	for i in range(4):
		red = []
		for j in range(4):
			red.append(stupci[j][i])
		ploca_up.append(red)
	# up - end

	# down
	bodovi_down = 0
	stupci = []
	for i in range(4):
		stupac = []
		for j in range(4):
			stupac.append(ploca[j][i])
		stupci.append(stupac)
	for stupac in stupci:
		br_nula = stupac.count(0)
		izbrisano = 0
		for i in range(4):
			if stupac[i - izbrisano] == 0:
				stupac.pop(i - izbrisano)
				izbrisano += 1
		for _ in range(br_nula):
			stupac.insert(0, 0)
		for i in range(-1, -4, -1):
			if stupac[i] != 0 and stupac[i] == stupac[i - 1]:
				bodovi_down += stupac[i] * 2
				stupac[i] *= 2
				stupac.pop(i - 1)
				stupac.insert(0, 0)
	ploca_down = []
	for i in range(4):
		red = []
		for j in range(4):
			red.append(stupci[j][i])
		ploca_down.append(red)
	# down - end

	# left
	bodovi_left = 0
	ploca_left = deep_copy(ploca)
	for red in ploca_left:
		br_nula = red.count(0)
		izbrisano = 0
		for i in range(4):
			if red[i - izbrisano] == 0:
				red.pop(i - izbrisano)
				izbrisano += 1
		red.extend([0 for _ in range(br_nula)])
		for i in range(3):
			if red[i] != 0 and red[i] == red[i + 1]:
				bodovi_left += red[i] * 2
				red[i] *= 2
				red.pop(i + 1)
				red.append(0)
	# left - end

	# right
	bodovi_right = 0
	ploca_right = deep_copy(ploca)
	for red in ploca_right:
		br_nula = red.count(0)
		izbrisano = 0
		for i in range(4):
			if red[i - izbrisano] == 0:
				red.pop(i - izbrisano)
				izbrisano += 1
		for _ in range(br_nula):
			red.insert(0, 0)
		for i in range(-1, -4, -1):
			if red[i] != 0 and red[i] == red[i - 1]:
				bodovi_right += red[i] * 2
				red[i] *= 2
				red.pop(i - 1)
				red.insert(0, 0)
	# right - end

	return ploca_up, ploca_down, ploca_left, ploca_right, bodovi_up, bodovi_down, bodovi_left, bodovi_right

def klik(key):
	global ploca
	global bodovi
	global won, lost
	global futures
	global key_state

	if not lost:
		old_ploca = deep_copy(ploca)
		match key.keysym:
			case "Up":
				if not key_state["Up"]:
					ploca = futures[0]
					bodovi += futures[4]
					key_state["Up"] = True
			case "Down":
				if not key_state["Down"]:
					ploca = futures[1]
					bodovi += futures[5]
					key_state["Down"] = True
			case "Left":
				if not key_state["Left"]:
					ploca = futures[2]
					bodovi += futures[6]
					key_state["Left"] = True
			case "Right":
				if not key_state["Right"]:
					ploca = futures[3]
					bodovi += futures[7]
					key_state["Right"] = True
		if old_ploca != ploca:
			spawn_rnd(ploca)
		refresh_gui()
		futures = calc_moves(ploca)
		if not won:
			won = victory(ploca)
		lost = game_over(ploca, futures[0], futures[1], futures[2], futures[3])

def klik_release(key):
	global key_state
	match key.keysym:
		case "Up":
			key_state["Up"] = False
		case "Down":
			key_state["Down"] = False
		case "Left":
			key_state["Left"] = False
		case "Right":
			key_state["Right"] = False

def refresh_gui():
	global ploca
	global bodovi
	global kocke_polja
	global tekst_polja
	global field_font
	global field_color
	global field_font_color
	global crtanje_polja

	for i in range(4):
		for j in range(4):
			try:
				boja = field_color[ploca[i][j]]
			except KeyError:
				boja = field_color[4096]
			crtanje_polja.itemconfig(kocke_polja[i][j], fill=boja)
			if ploca[i][j] != 0:
				try:
					boja_fonta = field_font_color[ploca[i][j]]
				except KeyError:
					boja_fonta = field_font_color[4096]
				try:
					font = field_font[ploca[i][j]]
				except KeyError:
					font = field_font[max(field_font.keys())]
				crtanje_polja.itemconfig(tekst_polja[i][j], text=ploca[i][j], font=font, fill=boja_fonta)
			else:
				crtanje_polja.itemconfig(tekst_polja[i][j], text="")
	score.itemconfig(bodovi_natpis, text=str(bodovi))

def new(event=None):
	global bodovi
	global ploca
	global won, lost
	global futures

	bodovi = 0
	won = False
	lost = False
	ploca = spawn_rnd(spawn_rnd([[0 for _ in range(4)] for _ in range(4)]))

	futures = calc_moves(ploca)
	pobjeda.place_forget()
	poraz.place_forget()
	refresh_gui()

def main():
	global pobjeda
	global poraz
	global ploca
	global bodovi
	global won, lost
	global futures
	global key_state
	global kocke_polja
	global tekst_polja
	global field_font
	global field_color
	global field_font_color
	global crtanje_polja
	global score, bodovi_natpis

	field_color = {0: "#CDC1B4",
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
	               4096: "#3C3A31"}
	field_font = {2: "Helvetica 40 bold",
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
	              262144: "Helvetica 17 bold",
	              524288: "Helvetica 17 bold",
	              1048576: "Helvetica 15 bold",
	              2097152: "Helvetica 15 bold",
	              4194304: "Helvetica 15 bold",
	              8388608: "Helvetica 15 bold",
	              16777216: "Helvetica 13 bold",
	              33554432: "Helvetica 13 bold",
	              67108864: "Helvetica 13 bold",
	              134217728: "Helvetica 12 bold",
	              268435456: "Helvetica 12 bold",
	              536870912: "Helvetica 12 bold",
	              1073741824: "Helvetica 11 bold",
	              2147483648: "Helvetica 11 bold",
	              4294967296: "Helvetica 11 bold",
	              8589934592: "Helvetica 11 bold",
	              17179869184: "Helvetica 10 bold",
	              34359738368: "Helvetica 10 bold",
	              68719476736: "Helvetica 10 bold",
	              137438953472: "Helvetica 10 bold",
	              274877906944: "Helvetica 10 bold",
	              549755813888: "Helvetica 10 bold",
	              1099511627776: "Helvetica 9 bold",
	              2199023255552: "Helvetica 9 bold",
	              4398046511104: "Helvetica 9 bold",
	              8796093022208: "Helvetica 9 bold",
	              17592186044416: "Helvetica 8 bold",
	              35184372088832: "Helvetica 8 bold",
	              70368744177664: "Helvetica 8 bold",
	              140737488355328: "Helvetica 8 bold",
	              281474976710656: "Helvetica 8 bold",
	              562949953421312: "Helvetica 8 bold"}
	field_font_color = {2: "#776E65",
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
	                    4096: "#F9F6F2"}

	root = Tk()
	root.config(background="#FAF8EF")
	width = 550
	height = 700
	root.geometry(f"{width}x{height}+{(root.winfo_screenwidth() // 2) - (width // 2)}+{(root.winfo_screenheight() // 2) - (height // 2)}")
	root.resizable(False, False)
	root.iconbitmap(resource_path("data/2048-icon.ico"))
	root.title("2048")

	crtanje_polja = Canvas(root, width=550, height=550, background="#FAF8EF", highlightthickness=0)
	crtanje_polja.place(x=0, y=150, width=550, height=550)

	score = Canvas(root, width=150, height=75, background="#FAF8EF", highlightthickness=0)
	score.place(x=375, y=20, width=150, height=100)
	round_rectangle(score, 5, 5, 145, 70, radius=15, steps=100, fill="#BBADA0")
	score.create_text(75, 25, fill="#EDE4DA", font="Helvetica 11 bold", text="SCORE", anchor="center")
	bodovi_natpis = score.create_text(75, 50, fill="#FFFFFF", font="Helvetica 22 bold", text="0", anchor="center")

	nova_igra = Canvas(root, width=150, height=50, background="#FAF8EF", highlightthickness=0)
	nova_igra.place(x=375, y=105, width=150, height=50)
	round_rectangle(nova_igra, 5, 5, 145, 45, radius=15, steps=100, fill="#8F7A66")
	nova_igra.create_text(75, 25, fill="#F9F6F2", font="Helvetica 14 bold", text="New Game", anchor="center")

	nova_igra.bind("<ButtonRelease-1>", new)
	root.bind("<Key>", klik)
	root.bind("<KeyRelease>", klik_release)
	key_state = {"Up": False,
	             "Down": False,
	             "Left": False,
	             "Right": False}

	pobjeda = Label(root, anchor="center", text="VICTORY!", font="Helvetica 30 bold", background="#FAF8EF", foreground="#ff0000", highlightthickness=0)

	poraz = Label(root, anchor="center", text="GAME OVER!", font="Helvetica 30 bold", background="#FAF8EF", foreground="#ff0000", highlightthickness=0)

	naslov = Label(root, anchor="center", text="2048", font="Helvetica 70 bold", background="#FAF8EF", foreground="#776E65", highlightthickness=0)
	naslov.place(x=25, y=35, width=220, height=80)

	round_rectangle(crtanje_polja, 25, 25, 525, 525, radius=15, steps=100, fill="#BBADA0")

	kocke_polja = []
	for i in range(41, 404 + 1, 121):
		red = []
		for j in range(41, 404 + 1, 121):
			red.append(round_rectangle(crtanje_polja, j, i, j + 105, i + 105, radius=8, steps=100, fill="#CDC1B4"))
		kocke_polja.append(red)

	tekst_polja = []
	for i in range(41, 404 + 1, 121):
		red = []
		for j in range(41, 404 + 1, 121):
			red.append(crtanje_polja.create_text(j + 52, i + 53, fill="darkblue", font="Helvetica 40 bold", text="2", anchor="center"))
		tekst_polja.append(red)

	new()

	root.mainloop()


if __name__ == '__main__':
	main()
