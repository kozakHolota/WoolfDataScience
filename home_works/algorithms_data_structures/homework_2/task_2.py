import turtle

import click


def koch_curve(t, order, size):
    if order == 0:
        t.forward(size)
    else:
        for angle in [60, -120, 60, 0]:
            koch_curve(t, order - 1, size / 3)
            t.left(angle)

def draw_koch_snowflake(order, size=300):
    window = turtle.Screen()
    window.bgcolor("white")

    t = turtle.Turtle()
    t.speed(0)
    t.penup()
    t.goto(-size / 2, y=size / 3)
    t.pendown()

    for _ in range(3):
        koch_curve(t, order, size)
        t.right(120)

    window.mainloop()

@click.command()
@click.option("--order", default=3, help="Order of Koch curve")
@click.option("--size", default=300, help="Size of the snowflake")
def main(order: int, size: int):
    draw_koch_snowflake(order, size)

if __name__ == "__main__":
    # Виклик функції
    main()
