from __future__ import print_function, absolute_import

from kivy.factory import Factory
# from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty
# from kivy.clock import Clock

# In practice, `Okapi` will be installed via pip. This mimicks that.
import os
import sys
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))
ENGINE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(ENGINE_PATH)

# Engine
from engine.app import Okapi
from engine.game import Game as OkapiGame
from engine.window_manager import WindowManager as OkapiWindowManager

# Local
import actors
import ground
import itertools


class Game(OkapiGame):

    BLANK_GROUND_CHARACTER = '.'
    EXTRA_GROUNDS = {
        "x": ground.BlockGround,
        "B": ground.BluePlayerGround,
        "b": ground.BlueGround,
        "G": ground.GreenPlayerGround,
        "g": ground.GreenGround,
        "R": ground.RedPlayerGround,
        "r": ground.RedGround,
        "Y": ground.YellowPlayerGround,
        "y": ground.YellowGround,
        "#": ground.ImpassableGround,
        ' ': ground.NullGround
    }

    CLOCK_INTERVAL = 1.0

    def __init__(self, *args, **kwargs):
        self.first_clock_cycle = True
        super(Game, self).__init__(*args, **kwargs)

        self.initialize_level_specific_objects()
        self.players = []
        self.players_dict = {}

    def on_new_level(self):
        """Reset the level-specific objects
        """
        self.initialize_level_specific_objects()
        self.player_cycle = itertools.cycle(self.players)

    def initialize_level_specific_objects(self):
        self._player_actor = None
        self.players = []
        self.players_dict = {}

    @property
    def player_actor(self):
        return self._player_actor

    @player_actor.setter
    def player_actor(self, value):
        self._player_actor = value

    def get_base_ground_class(self):
        return ground.OpenGround

    def on_add_actor(self, actor, level):
        self.players.append(actor)
        self.players_dict[actor.color] = actor
        if not getattr(self, '_player_actor'):
            self._player_actor = self.player_cycle.next()

    def clock_update(self, dt):
        if self.first_clock_cycle:
            self.first_clock_cycle = False
            return

    def on_press_spacebar(self, actor=None):
        self.player_actor = self.player_cycle.next()

    def on_press_b(self):
        self.swap('blue')

    def on_press_g(self):
        self.swap('green')

    def on_press_r(self):
        self.swap('red')

    def on_press_y(self):
        self.swap('yellow')

    def swap(self, color):
        if (color in self.players_dict.keys()) and (self._player_actor.color is not color):
            if self._player_actor.can_swap_with(self.players_dict[color]):
                # Swap the grounds with each other
                old_color_ground = self.players_dict[color].ground
                player_actor_ground = self._player_actor.ground

                # Swap the actors on the ground
                old_color_ground.actor = self._player_actor
                player_actor_ground.actor = self.players_dict[color]

                self._player_actor = self.players_dict[color]

    def on_press_down(self, actor=None):
        actor = actor or self.player_actor
        self._move(actor, 1, 0)

    def on_press_up(self, actor=None):
        actor = actor or self.player_actor
        self._move(actor, -1, 0)

    def on_press_left(self, actor=None):
        actor = actor or self.player_actor
        self._move(actor, 0, -1)

    def on_press_right(self, actor=None):
        actor = actor or self.player_actor
        self._move(actor, 0, 1)

    def on_post_level(self, level):
        pass

    def _move(self, actor, delta_x=0, delta_y=0):
        current_ground = actor.ground
        new_ground = self.current_level.get_ground_by_coords(current_ground.x + delta_x, current_ground.y + delta_y)
        if new_ground and new_ground.can_accommodate(actor, delta_x, delta_y):
            new_ground.actor = actor
            return True
        else:
            return False


class WindowManager(OkapiWindowManager):

    def get_welcome_screen(self):
        return Factory.WelcomeScreen()


class SwappyApp(Okapi):

    PROJECT_PATH = PROJECT_PATH
    WINDOW_MANAGER_CLS = WindowManager
    INI_PATH = "{}/params.ini".format(PROJECT_PATH)

    GAME_CLASS = Game

    # def resize_window(self, window):
    #     window.size = (Game.ROWS * 50, Game.COLS * 50)


if __name__ == '__main__':
    SwappyApp().run()
