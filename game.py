import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
######################

GAME_WIDTH = 8
GAME_HEIGHT = 8

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False
    DOOR_KEY = True

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!"%(len(player.inventory)))
        player.DOOR_KEY = True

class Chest(GameElement):
    IMAGE = "Chest"
    SOLID = False

    def interact(self, player):
        if player.inventory:
            lost_item = player.inventory.pop()
            GAME_BOARD.draw_msg("Look out!  That chest was evil!  You lost your %s!" % lost_item)

class Door(GameElement):
    IMAGE = "DoorClosed"
    SOLID = True

    def interact(self, player):
        if self.IMAGE == "DoorOpen":
            self.SOLID = False
        if player.DOOR_KEY and self.IMAGE == "DoorClosed":
            GAME_BOARD.draw_msg("You have opened the door!")
            self.change_image("DoorOpen")
      
            


class Character(GameElement):
    IMAGE = "Girl"
    DOOR_KEY = False

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []

    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        return None

    def keyboard_handler(self, symbol, modifier):
        direction = None

        if symbol == key.UP:
            direction = "up"
        elif symbol == key.DOWN:
            direction = "down"
        elif symbol == key.LEFT:
            direction = "left"
        elif symbol == key.RIGHT:
            direction = "right"

        self.board.draw_msg("[%s] moves %s" % (self.IMAGE, direction))

        if direction:
            next_location = self.next_pos(direction)

            if next_location:
                next_x = next_location[0]
                next_y = next_location[1]

                if 0 <= next_x < GAME_WIDTH and 0 <= next_y < GAME_HEIGHT: 
                    existing_el = self.board.get_el(next_x, next_y)

                    if existing_el:
                        print existing_el
                        existing_el.interact(self)

                    if existing_el and existing_el.SOLID:
                        self.board.draw_msg("There's something in my way!")
                    elif existing_el is None or not existing_el.SOLID:
                        self.board.del_el(self.x, self.y)
                        self.board.set_el(next_x, next_y, self)
                else:
                    self.board.draw_msg("I can't go any farther!")


####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    rock_positions = [
            (2,1),
            (1,2),
            (3,2),
            (2,3)
        ]

    rocks = []
    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    rocks[-1].SOLID = False

    player = Character()
    GAME_BOARD.register(player)
    GAME_BOARD.set_el(2,2,player)


    GAME_BOARD.draw_msg("This game is wicked awesome.")

    gem = Gem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(3, 1, gem)

    chest = Chest()
    GAME_BOARD.register(chest)
    GAME_BOARD.set_el(0,7, chest)

    door = Door()
    GAME_BOARD.register(door)
    GAME_BOARD.set_el(6,6, door)

