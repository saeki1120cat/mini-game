import tkinter as tk
import random

WINDOW_TITLE = "Snake"
BLOCK_SIZE = 10
MAP_WIDTH = 20
MAP_HEIGHT = 20
WIDTH = MAP_WIDTH * BLOCK_SIZE
HEIGHT = MAP_HEIGHT * BLOCK_SIZE
START_X = int(MAP_WIDTH / 2)
START_Y = int(MAP_HEIGHT / 2) - 1
KEY_LEFT = 37
KEY_UP = 38
KEY_RIGHT = 39
KEY_DOWN = 40
SPEED = 500
BG_COLOR = "#000000"
COLOR = "#7788ed"
FOOD_COLOR = "#ed779e"
START_TEXT = "Please press the \n up, down, left, or right keys \n on the keyboard to start game."
GAMEOVER_TEXT = "Game Over \n Press key to replay."

body = [[START_X, START_Y + 2], [START_X, START_Y + 1], [START_X, START_Y + 0]]
food = [random.randint(5, MAP_WIDTH - 5), random.randint(5, MAP_HEIGHT - 5)]
direction = 0
speed = 100
startGame = False
gameOver = False

#Initialize tkinter
root = tk.Tk()
root.title(WINDOW_TITLE)
root.maxsize(width=WIDTH, height=HEIGHT)
root.minsize(width=WIDTH, height=HEIGHT)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#Canvas initialize
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.grid(column=0, row=0)
canvas.config(bg=BG_COLOR)
canvas.focus_set()


def drawBlock(item, color = COLOR):
	x = item[0] * BLOCK_SIZE
	y = item[1] * BLOCK_SIZE
	canvas.create_rectangle(x, y, x + BLOCK_SIZE, y + BLOCK_SIZE, fill=color)
	pass


def gameUpdate():
	global direction, food, body
	#remove tail
	tail = body.pop()
	drawBlock(tail, color=BG_COLOR)
	#insert head
	head = [body[0][0], body[0][1]]
	body.insert(0, head)
	if direction == KEY_LEFT:
		head[0] -= 1
	elif direction == KEY_UP:
		head[1] -= 1
	elif direction == KEY_RIGHT:
		head[0] += 1
	elif direction == KEY_DOWN:
		head[1] += 1
	#draw body
	for item in body:
		drawBlock(item)
		pass
	#food control
	drawBlock(food, color=FOOD_COLOR)
	if head == food:
		levelUp()
		pass
	return head
	pass


def update():
	global body, gameOver
	if gameOver == False:
		head = gameUpdate()
		#gameover
		if head[0] < 0 or head[0] > MAP_WIDTH - 1:
			gameOver = True
		if head[1] < 0 or head[1] > MAP_HEIGHT - 1:
			gameOver = True
		if body.count(head) > 2:
			gameOver = True
		root.after(speed, update)
		pass
	else:
		overUpdate()
		pass
	pass


#Body move
def move(event) :
	global direction, gameOver, startGame, canvas
	if event.keycode == KEY_LEFT or event.keycode == KEY_UP or event.keycode == KEY_RIGHT or event.keycode == KEY_DOWN:
		if startGame == True:
			if direction == KEY_LEFT:
				if event.keycode == KEY_RIGHT:
					return
			elif direction == KEY_UP:
				if event.keycode == KEY_DOWN:
					return
			elif direction == KEY_RIGHT:
				if event.keycode == KEY_LEFT:
					return
			elif direction == KEY_DOWN:
				if event.keycode == KEY_UP:
					return
			else:
				return
			direction = event.keycode
		else:
			if gameOver == True:
				initialize()
				pass
			else:
				startGame = True
				direction = event.keycode
				canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill=BG_COLOR)
				update()
				pass
	pass


def levelUp():
	global food, body, speed
	body.insert(1, food)
	food = [random.randint(1, MAP_WIDTH - 2), random.randint(1, MAP_HEIGHT - 2)]
	if speed > 10:
		speed -= 10
		pass
	pass


def overUpdate():
	global canvas, startGame
	x = int(WIDTH / 2)
	y = int(HEIGHT / 2)
	canvas.create_text(x, y, fill="#ffffff", text=GAMEOVER_TEXT, justify=tk.CENTER)
	startGame = False
	pass


def initialize():
	global food, body, direction, speed, startGame, gameOver
	food = [random.randint(0, MAP_WIDTH - 1), random.randint(0, MAP_HEIGHT - 1)]
	body = [[START_X, START_Y + 2], [START_X, START_Y + 1], [START_X, START_Y + 0]]
	direction = 0
	speed = SPEED
	startGame = False
	gameOver = False
	canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill=BG_COLOR)
	for item in body:
		drawBlock(item)
		pass
	x = int(WIDTH / 2)
	y = int(HEIGHT / 2)
	canvas.create_text(x, y, fill="#ffffff", text=START_TEXT, justify=tk.CENTER)
	pass


initialize()

#set event
canvas.bind("<Key>", move)
root.mainloop()