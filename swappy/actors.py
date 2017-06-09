from __future__ import print_function, absolute_import

# Engine
from engine.actors import BaseActor


class SwappyActor(BaseActor):
    def __init__(self):
        super(BaseActor, self).__init__()
        self.color = None

    def can_swap_with(self, player):
        if self._both_grounds_can_accommodate(player):
            if (player.x == self.x) or (player.y == self.y):
                return True

    def _both_grounds_can_accommodate(self, player):
        if player.ground.color or self.ground.color:
            if (player.color != self.ground.color) or (self.color != player.ground.color):
                return False
        return True

    @property
    def x(self):
        return self.ground.x

    @property
    def y(self):
        return self.ground.y


class BluePlayer(SwappyActor):
    def __init__(self):
        super(SwappyActor, self).__init__()
        self.color = 'blue'
    SPRITE_SOURCE = 'assets/images/blue-guy.png'
    IS_MOVABLE = True


class GreenPlayer(SwappyActor):
    def __init__(self):
        super(SwappyActor, self).__init__()
        self.color = 'green'
    SPRITE_SOURCE = 'assets/images/green-guy.png'
    IS_MOVABLE = True


class RedPlayer(SwappyActor):
    def __init__(self):
        super(SwappyActor, self).__init__()
        self.color = 'red'
    SPRITE_SOURCE = 'assets/images/red-guy.png'
    IS_MOVABLE = True


class YellowPlayer(SwappyActor):
    def __init__(self):
        super(SwappyActor, self).__init__()
        self.color = 'yellow'
    SPRITE_SOURCE = 'assets/images/yellow-guy.png'
    IS_MOVABLE = True


class Block(BaseActor):
    SPRITE_SOURCE = 'assets/images/fancy-block-50.png'
    IS_MOVABLE = True


class Cheese(BaseActor):
    SPRITE_SOURCE = 'assets/images/fancy-cheese-50.png'
    IS_MOVABLE = False
