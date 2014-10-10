import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
######################

GAME_WIDTH = 10
GAME_HEIGHT = 10

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

    def interact(self, player):
        if not self.SOLID:
            player.hover = self

class Wall(GameElement):
    IMAGE = "Wall"
    SOLID = True

class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False
    DOOR_KEY = True

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!"%(len(player.inventory)))
        player.DOOR_KEY = True

class GreenGem(Gem):
    IMAGE = "GreenGem"
    SCREEN_KEY = True
    JUMP_POWER = True

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You have special jumping powers! Hold down SHIFT key to jump!")
        player.JUMP_POWER = True
        player.CHEST_KEY = True

        badguy = BadGuy()
        self.board.register(badguy)
        self.board.set_el(0, 4, badguy)

        walls = [(7,0), (7,1), (7,2), (8,2),(9,2)]
        for pos in walls:
            wall = Wall()
            GAME_BOARD.register(wall)
            GAME_BOARD.set_el(pos[0], pos[1], wall)


class Chest(GameElement):
    IMAGE = "Chest"
    SOLID = True

    def interact(self, player):
        if player.CHEST_KEY:
            self.SOLID = False
            # GAME_BOARD.del_el(badguy.x, badguy.y)
            GAME_BOARD.draw_msg("You've opened the magical chest and won the game!")
        # if player.inventory:
        #     lost_item = player.inventory.pop()
        #     GAME_BOARD.draw_msg("Look out!  That chest was evil!  You lost your %s!" % lost_item)
        #     player.DOOR_KEY = False

class Door(GameElement):
    IMAGE = "DoorClosed"
    SOLID = True

    def interact(self, player):
        if self.IMAGE == "DoorOpen":
            self.SOLID = False
        if player.DOOR_KEY and self.IMAGE == "DoorClosed":
            GAME_BOARD.draw_msg("You have opened the door!")
            self.change_image("DoorOpen")

class BadGuy(GameElement):
    IMAGE = 'Horns'
    direction = 1
    call_count = 0
    hover = None


    def update(self, dt):
        if self.call_count % 3 == 0:
            next_x = self.x + self.direction

            if next_x < 0 or next_x >= self.board.width:
                self.direction *= -1
                next_x = self.x

            character_in_path = self.board.get_el(next_x, 4)

            hover = self.hover

            if isinstance(character_in_path, Character):
                character_in_path.interact(self)

            self.board.del_el(self.x, self.y)
            if hover:
                self.board.set_el(self.x, self.y, hover)
                self.hover = None
            self.board.set_el(next_x, self.y, self)
        self.call_count += 1

    def interact(self, player):
        print "The player is interacting with the badguy"
        # player.hover = self

class Character(GameElement):
    IMAGE = "Girl"
    DOOR_KEY = False
    JUMP_POWER = False
    CHEST_KEY = False
    hover = None
    MOVE_COUNT = 0

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []

    def interact(self, badguy):
        print "The badguy interacts with the player"
        badguy.hover = self
        print "The badguy has run into", badguy.hover
        for item_index in range(len(self.inventory)):
            if isinstance(self.inventory[item_index], GreenGem):
                del self.inventory[item_index]
        self.JUMP_POWER = False
        self.board.draw_msg("The bad guy stole your green gem! Boo hoo")

    def next_pos(self, direction, speed=1):
        if direction == "up":
            return (self.x, self.y-speed)
        elif direction == "down":
            return (self.x, self.y+speed)
        elif direction == "left":
            return (self.x-speed, self.y)
        elif direction == "right":
            return (self.x+speed, self.y)
        return None

    def keyboard_handler(self, symbol, modifier):
        direction = None
        print symbol, modifier

        move_by = 1
        if modifier & key.MOD_SHIFT and self.JUMP_POWER == True:
            print "you're holding shift"
            move_by = 2

        if symbol == key.UP:
            direction = "up"
        elif symbol == key.DOWN:
            direction = "down"
        elif symbol == key.LEFT:
            direction = "left"
        elif symbol == key.RIGHT:
            direction = "right"
        elif symbol == key.Q:
            sys.exit("Game over!")
        self.MOVE_COUNT += 1

        if self.MOVE_COUNT < 30:    
            self.board.draw_msg("[%s] moves %s" % (self.IMAGE, direction))
        else:    
            direction = None
            self.board.draw_msg("You lost! You only get 30 keystrokes! Press Q to quit.")
        if direction:
            next_location = self.next_pos(direction, move_by)

            if next_location:
                next_x = next_location[0]
                next_y = next_location[1]

                if 0 <= next_x < GAME_WIDTH and 0 <= next_y < GAME_HEIGHT: 
                    existing_el = self.board.get_el(next_x, next_y)

                    hover = self.hover

                    if existing_el:
                        print existing_el
                        existing_el.interact(self)

                    if existing_el and existing_el.SOLID:
                        self.board.draw_msg("There's something in my way!")
                    elif existing_el is None or not existing_el.SOLID:
                        self.board.del_el(self.x, self.y)
                        if hover:
                            self.board.set_el(self.x, self.y, hover)
                            self.hover = None
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

    greengem = GreenGem()
    GAME_BOARD.register(greengem)
    GAME_BOARD.set_el(8,8, greengem)

    chest = Chest()
    GAME_BOARD.register(chest)
    GAME_BOARD.set_el(9,0, chest)

    door = Door()
    GAME_BOARD.register(door)
    GAME_BOARD.set_el(7,7, door)

    wall_positions = [(5,8), (5,7), (5,9), (6,7), (8,7), (9,7), (9,8), (9,9)]
    walls = []
    for pos in wall_positions:
        wall = Wall()
        GAME_BOARD.register(wall)
        GAME_BOARD.set_el(pos[0], pos[1], wall)
        walls.append(wall)

