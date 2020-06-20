"""
    File:               Game.py
    Associated Files:   Main.py
    Packages Needed:    random
    Date Created:       3/6/2019
    Author:             John Lukowski
    Date Modified:      6/19/2020 by John Lukowski
    Modified By:        John Lukowski
    License:            CC-BY-SA-4.0

    Purpose:            Setup components to run a simple text based rpg
"""

# Imports
import random as rand

# List of possible enemies to encounter, with their stats [health, strength, armor, blockChance, dodgeChance, critChance, dropChance, lootTable]
enemies = {"Large Frog" : [4, 1, 0, 0, 10, 0, 20, 1],
           "Goblin"     : [2, 2, 0, 0, 0, 0, 20, 1],
           "Wolf"       : [2, 3, 0, 0, 0, 10, 30, 1],
           "Ogre"       : [4, 2, 1, 0, 0, 0, 40, 2],
           "Troll"      : [4, 3, 1, 10, 0, 0, 40, 2]}
spawnChances = [30,30,20,10,10]

# List of possible items the player can obtain and their descriptions
items = {"Apple"    : "Eating heals the player by up to 1 health",
         "Potion"   : "Using heals the player by up to 3 health"}
lootTable = [[60, 40],
             [20,80]]

# List of professions the player can choose from and their stats [health, strength, armor, blockChance, dodgeChance, critChance]
professions = { "Knight"     : [16, 4, 2, 0, 0, 0],
                "Rogue"      : [10, 2, 0, 0, 20, 10],
                "Farmer"     : [14, 3, 1, 0, 0, 0],}

"""
    Function:   wChoice
    Params:     seq of data, weight(int)
    Purpose:    make a random choice based on weighted outcomes
    Returns:    the choice
"""
def wChoice(seq, weights):
    weighted = []
    for i in range(0,len(seq)):
        weighted += [seq[i]] * (weights[i])
    return rand.choice(weighted)

"""
    Class:      Character
    Purpose:    Hold character stats for enemies and players
    Methods:    doDamage, takeDamage
"""
class Character:
    def __init__(self):
        self.name = ""
        self.health = rand.randint(8,15)
        self.healthMax = self.health
        self.strength = rand.randint(2,3)
        self.armor = 0
        self.blockChance = 0    # out of 100
        self.dodgeChance = 0
        self.critChance = 0

    """
        Function:   doDamage
        Params:     opponent
        Purpose:    default assign damage to the opponent
        Returns:    amount of damage dealt
    """
    def doDamage(self, opponent):
        damage = self.strength + rand.randint(0,2)
        if rand.randint(0,100) < self.critChance:
            damage *= 2
            print("%s got a critical strike!" % self.name)
        return opponent.takeDamage(damage)

    """
        Function:   takeDamage
        Params:     damage
        Purpose:    default take damage method
        Returns:    damage dealt
    """
    def takeDamage(self, damage):
        chance = rand.randint(0,100)
        if chance < self.blockChance:
            print("%s blocks the incoming attack" % self.name)
            return 0
        elif chance < self.dodgeChance:
            print("%s dodges the incoming attack" % self.name)
            return 0
        damage -= self.armor
        if damage < 0:
            return 0
        self.health -= damage
        return damage
# END OF CHARACTER CLASS

"""
    Class:      Enemy is a Character
    Purpose:    generate an enemy character based on the stats in the enemies list
    Methods:    
"""
class Enemy(Character):
    def __init__(self, enemy):
        Character.__init__(self)
        self.name = enemy
        self.health = enemies[enemy][0]
        self.healthMax = self.health
        self.strength = enemies[enemy][1]
        self.armor = enemies[enemy][2]
        self.blockChance = enemies[enemy][3]
        self.dodgeChance = enemies[enemy][4]
        self.critChance = enemies[enemy][5]
        self.dropChance = enemies[enemy][6]
        self.loot = enemies[enemy][7]
# END OF ENEMY CLASS

"""
    Class:      Player is a Character
    Purpose:    generate and control a player character
    Methods:    quit, help, getStatus, rest, explore, flee, attack, inventory, useItem, inspect
"""
class Player(Character):
    def __init__(self, name, profession):
        Character.__init__(self)
        self.name = name
        self.profession = profession
        self.status = "rested"
        self.enemy = None
        self.inventory = {}
        self.health         = professions[profession][0]
        self.healthMax      = self.health
        self.strength       = professions[profession][1]
        self.armor          = professions[profession][2]
        self.blockChance    = professions[profession][3]
        self.dodgeChance    = professions[profession][4]
        self.critChance     = professions[profession][5]

        if profession == "Farmer":
            self.inventory.update({"Apple":3})

    """
            Function:   quit
            Params:     
            Purpose:    end the game
            Returns:    exit string
    """
    def quit(self):
        self.health = 0
        self.status = "quit"
        return "%s decides to head back home." % self.name

    """
            Function:   help
            Params:     
            Purpose:    print out all available player actions
            Returns:    available actions
    """
    def help(self):
        return list(actions.keys())

    """
            Function:   getStatus
            Params:     
            Purpose:    give current player status
            Returns:    status and health of player
    """
    def getStatus(self):
        return "%s is %s with health: %d/%d." % (self.name, self.status, self.health, self.healthMax)

    """
            Function:   rest
            Params:     
            Purpose:    heal up if tired and not attacking
            Returns:    rested or cant rest string
    """
    def rest(self):
        if self.status == "tired":
            if self.health < self.healthMax:
                self.health += 1
            self.status = "rested"
            return "%s feels refreshed." % self.name
        if self.status == "rested":
            return "%s is already well rested." % self.name
        return "%s can't rest right now" % self.name

    """
            Function:   explore
            Params:     
            Purpose:    generate a random encounter
            Returns:    new exploration or default
    """
    def explore(self):
        if self.status != "in-combat":
            enemy = wChoice(list(enemies.keys()), spawnChances)
            self.enemy = Enemy(enemy)
            self.status = "in-combat"
            return "%s has run into a %s!" % (self.name, self.enemy.name)
        return "%s is currently distracted." % self.name

    """
            Function:   flee
            Params:     
            Purpose:    escape from combat
            Returns:    escape or run around uselessly
    """
    def flee(self):
        if self.status == "in-combat":
            self.status = "tired"
            self.enemy = None
            return "%s flees like a coward." % self.name
        self.status = "tired"
        return "%s runs in a circle a couple of times." % self.name

    """
        Function:   attack
        Params:     
        Purpose:    attack enemy if there is one
        Returns:    attack or uselessly attack the air
    """
    def attack(self):
        if self.status == "in-combat":
            dmgDealt = self.doDamage(self.enemy)
            if self.enemy.health > 0:
                dmgTaken = self.enemy.doDamage(self)
                return "%s dealt %d damage to the %s\nThe %s dealt %d damage to %s." % (self.name, dmgDealt, self.enemy.name, self.enemy.name, dmgTaken, self.name)
            self.status = "tired"
            if rand.randint(0,100) > 50:
                drop = wChoice(list(items.keys()), lootTable[self.enemy.loot])
                if drop in self.inventory:
                    self.inventory[drop] += 1
                else:
                    self.inventory.update({drop:1})
                return "%s dealt %d damage to the %s, vanquishing it! It dropped a(n) %s!" % (self.name, dmgDealt, self.enemy.name, drop)
            return "%s dealt %d damage to the %s, vanquishing it!" % (self.name, dmgDealt, self.enemy.name)
        self.status = "tired"
        return "%s ineffectively attacks the air for a while." % self.name

    """
        Function:   printInv
        Params:     
        Purpose:    print out all items in inventory
        Returns:    list of items
    """
    def printInv(self):
        return [item + "(s) : " + str(self.inventory[item]) for item in list(self.inventory.keys())]

    """
        Function:   useItem
        Params:     
        Purpose:    check if item, then use it
        Returns:    no item or use of item
    """
    def useItem(self):
        item = input("Enter item to use > ")
        if item in self.inventory:  # if you have the item, remove one and use it
            self.inventory[item] -= 1
            if self.inventory[item] <= 0:
                self.inventory.pop(item)
            if item == "Potion":
                self.health += 3
            elif item == "Apple":
                self.health += 1
            if self.health > self.healthMax:
                self.health = self.healthMax

            return "%s used a(n) %s" % (self.name, item)
        return "%s doesn't own that item." % self.name

    """
        Function:   inspect
        Params:     
        Purpose:    chack an item's description
        Returns:    no item or description of item
    """
    def inspect(self):
        item = input("Enter item to inspect > ")
        if item in self.inventory:  # if you have the item, describe it
            return items[item]
        return "%s doesn't own that item." % self.name
# END OF PLAYER CLASS

# list of possible player actions
actions = {"quit"       : Player.quit,
           "help"       : Player.help,
           "status"     : Player.getStatus,
           "rest"       : Player.rest,
           "explore"    : Player.explore,
           "flee"       : Player.flee,
           "attack"     : Player.attack,
           "inventory"  : Player.printInv,
           "use"        : Player.useItem,
           "inspect"    : Player.inspect}