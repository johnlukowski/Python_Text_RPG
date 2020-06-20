"""
    File:               Main.py
    Associated Files:   Game.py
    Packages Needed:    random
    Date Created:       3/6/2019
    Author:             John Lukowski (https://github.com/JLukeSkywalker)
    Date Modified:      6/19/2020 by John Lukowski
    Modified By:        John Lukowski
    License:            CC-BY-SA-4.0

    Purpose:            Run a simple text based rpg
"""

# Imports
from Game import *

"""
    Function:   main
    Params :    none
    Purpose:    run the game loop and communicate with user
    Returns:    none
"""
def main():
    name = input("Welcome to the adventure! What is your character's name?\n> ")
    print("What is %s's profession?" % name,  list(professions.keys()))
    profession = input("> ")
    while profession not in professions:
        profession = input("That is not a valid profession in this forest, try again.\n> ")
    player = Player(name,profession)
    print("(type help to get a list of actions)\n")
    print("%s the %s walks deep into a dark forest looking for an adventure." % (player.name, player.profession))

    while player.health > 0:
        command = input("> ")
        read = False
        for action in actions.keys():
            if command == action:
                print(actions[action](player))
                read = True
        if not read:
            print("%s doesn't understand the suggestion." % player.name)
    if player.status != "quit":
        print("%s was unfortunately not able to make it out of the forest." % player.name)











if __name__ == "__main__":
    main()
