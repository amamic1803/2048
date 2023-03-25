# Previously used 2048 game logic in pure Python.
# unused after 2048 logic rewrite in Rust (v7.0.0)
# only calc_moves function has some value, but it's not used in the game

import random

def deep_copy(lista: list):
	temp_list = []
	for x in lista:
		try:
			len(x)
			temp_list.append(deep_copy(x))
		except TypeError:
			temp_list.append(x)
	return temp_list

def spawn_rnd(ploca):
	spawn_places = []
	for x in range(4):
		for y in range(4):
			if ploca[x][y] == 0:
				spawn_places.append((x, y))
	spawn_place = random.choice(spawn_places)

	ploca[spawn_place[0]][spawn_place[1]] = 2 if random.random() < 0.9 else 4

	return ploca

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
