import turtle
from math import sqrt

def draw_square(t, x, y, size, angle):
    t.penup()
    t.goto(x, y)
    t.setheading(angle)
    t.pendown()
    points = []
    for _ in range(4):
        points.append(t.position())
        t.forward(size)
        t.left(90)
    return points

def pithagoras_tree(x, y, size, angle, depth, t):
    if depth == 0 or size < 2:
        return

    # Малюємо квадрат
    points = draw_square(t, x, y, size, angle)
    if not points or len(points) != 4:
        return
    p0, p1, p2, p3 = points

    # Довжина сторони для дочірніх квадратів
    new_size = size / sqrt(2)

    # Ліва гілка (кут +45°)
    pithagoras_tree(p3[0], p3[1], new_size, angle + 45, depth - 1, t)
    # Права гілка (кут -45°)
    pithagoras_tree(p2[0], p2[1], new_size, angle - 45, depth - 1, t)


def draw_pithagor_tree(size, x, y, angle=0, depth=0, a=45, b=45):
    screen = turtle.Screen()
    screen.title("Піфагорове дерево")
    screen.tracer(0, 0)

    t = turtle.Turtle()
    t.speed(0)
    t.pensize(1)

    pithagoras_tree(size=size, x=x, y=y, angle=angle, depth=depth, t=t)
    screen.update()
    screen.mainloop()

if __name__ == "__main__":
    draw_pithagor_tree(
        size=80,
        x=-10,
        y=-200,
        angle=0,
        depth=25,
        a=45,
        b=45
    )