import pdb
import tkinter
from collections import namedtuple

# TODO: learn how to use frame.after !!!


class Game:
    def __init__(self, frame, height=300, width=300):
        self.height = height
        self.width = width
        self.frame = frame


class Paddle:
    def __init__(self, cavas, game, x0=0, y0=0, x1=10, y1=30, speed=10, color='red'):
        self.id = None
        self.canvas = cavas
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.speed = speed
        self.color = color
        self.game = game

    def draw(self):
        self.id = myCanvas.create_rectangle(
            self.x0,
            self.y0,
            self.x1,
            self.y1,
            fill=self.color
        )

    def set_id(self, _id):
        self.id = _id

    def get_coords(self):
        Coords = namedtuple("cords", "x0 y0 x1 y1")
        _coords = self.canvas.coords(self.id)

        return Coords(_coords[0], _coords[1], _coords[2], _coords[3])

    def move_up(self):
        coords = self.get_coords()
        if 0 <= coords.y0 - self.speed:
            self.canvas.move(self.id, 0, -self.speed)

    def move_down(self):
        coords = self.get_coords()
        if self.game.height >= coords.y1 + self.speed:
            self.canvas.move(self.id, 0, self.speed)


class Ball:
    def __init__(self, cavas, game, x0=70, y0=70, x1=100, y1=100, speed=10, color='blue'):
        self.id = None
        self.canvas = cavas
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.speed = speed
        self.color = color
        self.game = game

    def draw(self):
        self.id = myCanvas.create_oval(
            self.x0,
            self.y0,
            self.x1,
            self.y1,
            fill=self.color
        )

    def move(self):
        self.canvas.move(self.id, 0, self.speed)
        self.game.frame.after(1000, self.move)

# init tk
root = tkinter.Tk()

game = Game(frame=root)

# create canvas
myCanvas = tkinter.Canvas(root, bg="white", height=300, width=300)

# draw rect
paddle = Paddle(myCanvas, game=game)
paddle.draw()

# draw ball
ball = Ball(myCanvas, game=game)
ball.draw()


# add to window and show
myCanvas.pack()


def key_event(key):
    if key.keysym == "Down":
        paddle.move_down()

    if key.keysym == "Up":
        paddle.move_up()
        print(myCanvas.coords(paddle.id))

    print(f"{key}")

#pdb.set_trace()

root.bind('<Key>', key_event)


root.after(1000, ball.move)
root.mainloop()
