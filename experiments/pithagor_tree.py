import turtle

class PithagorTree:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.__squares = []
        self.__window = turtle.Screen()
        self.__turtle = turtle.Turtle()

    def draw(self, size=None, x=None, y=None):
        if not self.__squares:
            size = self.size
            x = self.x
            y = self.y
        self.__window.bgcolor("white")
        self.__turtle.penup()
        self.__turtle.goto(x, y)
        x_, y_ = self.__turtle.position()
        left_end = {"x": x_, "y": y_, "rotation": "left"}
        self.__turtle.pendown()
        for i in range(2):
            self.__turtle.forward(size)
            x_, y_ = self.__turtle.position()
            if i == 0:
                right_end = {"x": x_, "y": y_, "rotation": "right"}
            self.__turtle.left(90)
            self.__turtle.forward(size*2)
            self.__turtle.left(90)
            self.__turtle.forward(size)

        self.__squares.append({"left_end": left_end, "right_end": right_end, "size": size})

        self.__window.mainloop()

if __name__ == "__main__":
    pit_tree = PithagorTree(0, 0, 100)
    pit_tree.draw()