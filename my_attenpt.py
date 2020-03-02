import pdb
import tkinter
from collections import namedtuple

# TODO: learn how to use frame.after !!!


class Game:
    def __init__(self, frame, height=300, width=300):
        self.height = height
        self.width = width
        self.frame = frame
        self.ball = None

    def add_ball(self):
        # draw ball
        center_x0 = self.width // 2 - 10
        center_x1 = self.width // 2 + 10

        self.ball = Ball(myCanvas, game=game, x0=center_x0, x1=center_x1)
        self.ball.draw()



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


class CPUPaddle(Paddle):
    def move(self):
        coords = self.get_coords()
        ball_coords = self.game.ball.get_coords()

        print(f"cpu: {coords}")

        if self.game.ball.direction_y == "down":
            # Move down
            self.canvas.move(self.id, 0, self.speed)

        elif self.game.ball.direction_y == "up":
            # move up
            self.canvas.move(self.id, 0, -self.speed)

        # register the callback
        self.game.frame.after(200, self.move)

class Ball:
    def __init__(self, cavas, game, x0=60, y0=0, x1=80, y1=20, speed=10, color='blue'):
        self.id = None
        self.canvas = cavas
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.speed = speed
        self.speedx = speed
        self.color = color
        self.game = game
        self.direction_y = "down"
        self.direction_x = "right"
        self.previous_coords = None

    def draw(self):
        self.id = myCanvas.create_oval(
            self.x0,
            self.y0,
            self.x1,
            self.y1,
            fill=self.color
        )

    def get_coords(self):
        Coords = namedtuple("cords", "x0 y0 x1 y1")
        _coords = self.canvas.coords(self.id)

        return Coords(_coords[0], _coords[1], _coords[2], _coords[3])

    def move(self):
        speed = self.speed
        speedx = self.speedx
        coords = self.get_coords()
        if self.previous_coords:
            # lets find the direction for UP and Down
            if self.previous_coords.y0 < coords.y0:
                #Down
                speed = abs(speed)
                self.direction_y = "down"
            elif self.previous_coords.y0 > coords.y0:
                # up
                speed = -abs(speed)
                self.direction_y = "up"

            elif self.previous_coords.y0 == coords.y0:
                if self.direction_y == "down":
                    # go up
                    speed = -abs(speed)
                    self.direction_y = "up"
                else:
                    # go down
                    speed = abs(speed)
                    self.direction_y = "down"

            # Lets find the direction for left and right
            if self.previous_coords.x0 < coords.x0:
                # go right
                speedx = abs(speedx)
                self.direction_x = "right"

            elif self.previous_coords.x0 > coords.x0:
                # Go left
                speedx = -abs(speedx)
                self.direction_x = "left"

            elif self.previous_coords.x0 == coords.x0:
                if self.direction_x == "right":
                    # go up
                    speedx = -abs(speedx)
                    self.direction_x = "left"
                else:
                    # go down
                    speedx = abs(speed)
                    self.direction_x = "right"

        print(coords)
        print((speedx, speed))

        # when to stop going down
        if self.direction_y == "down":
            if coords.y0 + 30 < self.game.height:
                self.canvas.move(self.id, 0, speed)

        elif self.direction_y == "up":
            if coords.y0 > 0:
                self.canvas.move(self.id, 0, speed)

        # when to stop going right
        if self.direction_x == "right":
            if coords.x0 + 30 < self.game.width:
                self.canvas.move(self.id, speedx, 0)
                pass

        elif self.direction_x == "left":
            if coords.x0 > 0:
                self.canvas.move(self.id, speedx, 0)

        self.previous_coords = coords
        self.game.frame.after(200, self.move)


# init tk
root = tkinter.Tk()

game = Game(frame=root)

# create canvas
myCanvas = tkinter.Canvas(root, bg="white", height=300, width=300)

# draw rect
paddle = Paddle(myCanvas, game=game)
paddle.draw()

# draw cpu paddle
cpu_paddle = CPUPaddle(myCanvas, game=game, x0=game.width - 10, x1=game.width)
cpu_paddle.draw()

# add ball
game.add_ball()


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


root.after(1000, game.ball.move)
root.after(1000, cpu_paddle.move)
root.mainloop()
