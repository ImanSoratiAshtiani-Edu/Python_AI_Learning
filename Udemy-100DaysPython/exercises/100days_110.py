def a():
    from turtle import Turtle, Screen
    timmy = Turtle()
    print(timmy)
    my_screen= Screen()
    print(my_screen.canvheight)
    timmy.shape("turtle")
    timmy.color("coral")
    timmy.pencolor("black")
    timmy.forward(50)
    timmy.penup()
    my_screen.exitonclick()
def b():
    from prettytable import PrettyTable
    table=PrettyTable()
    table.add_column("Pokemon Name", ("Pikachu","Squirtle", "Charmander"),"l")
    table.add_column("Type", ("Electric", "Water", "Fire"), "l")
    table.align="r"
    print(table)

b()


