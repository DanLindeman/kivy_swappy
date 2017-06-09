# mimicks pip install of engine
import os
import sys
ENGINE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(ENGINE_PATH)

# Engine
from engine import ground as okapi_ground

# Local
import actors


class OpenGround(okapi_ground.BaseGround):
    sprite_path = 'assets/images/fancy-ground-50.png'
    color = None


    def can_accommodate(self, actor, delta_x, delta_y):
        """
        This is the code that pushes rows of blocks!
        If we try to walk onto ground already occupied by an actor,
        we see if that actor is a block. If so, we traverse in the
        direction of the desired movement until we find empty territory,
        at which time we move the entire row of blocks.
        """
        current_target_x = self.x
        current_target_y = self.y

        movable_row = []

        if self.color:
            if actor.color != self.color:
                return False

        if self.actor and self.actor.IS_MOVABLE:

            # Only mice can push blocks. Not cats. That would make no
            # real world sense. Come on!
            # if not isinstance(actor, actors.Rat):
            #     return False

            movable_row.append(self.actor)

            while True:
                # Every step through this loop, obviously we must continue
                # to stride out in the desired direction
                current_target_x += delta_x
                current_target_y += delta_y

                # Get ground at the target location
                ground = self.level.get_ground_by_coords(current_target_x, current_target_y)

                # If the ground doesn't exist or is impassible, the whole ruse is up
                if ground is None or not ground.is_passable:
                    return False

                # If the ground has an actor...
                if ground.actor:
                    # Non-blocks are show-stoppers. Ruse is up. (Will be updated when we have cheese!)
                    if not ground.actor.IS_MOVABLE:
                        return False

                    # Finding more blocks means we push on...
                    else:
                        movable_row.append(ground.actor)

                # Land-ho! We found an empty spot.
                else:
                    movable_row.reverse()
                    for actor in movable_row:
                        self.level.game._move(actor, delta_x, delta_y)
                    return True

        return super(OpenGround, self).can_accommodate(actor, delta_x, delta_y)


class GreenGround(OpenGround):
    color = 'green'
    sprite_path = 'assets/images/green-ground.png'


class BlueGround(OpenGround):
    color = 'blue'
    sprite_path = 'assets/images/blue-ground.png'


class RedGround(OpenGround):
    color = 'red'
    sprite_path = 'assets/images/red-ground.png'


class YellowGround(OpenGround):
    color = 'yellow'
    sprite_path = 'assets/images/yellow-ground.png'


class BluePlayerGround(OpenGround):
    initial_actor_cls = actors.BluePlayer
    color = None


class GreenPlayerGround(OpenGround):
    initial_actor_cls = actors.GreenPlayer
    color = None


class RedPlayerGround(OpenGround):
    initial_actor_cls = actors.RedPlayer
    color = None


class YellowPlayerGround(OpenGround):
    initial_actor_cls = actors.YellowPlayer
    color = None


class GreenPlayerGoal(OpenGround):
    sprite_path = 'path/to/goalimage.png'
    color = None


class BlockGround(OpenGround):
    initial_actor_cls = actors.Block


class NullGround(OpenGround):
    is_passable = False
    color = None
    sprite_path = 'assets/images/black.png'


class ImpassableGround(okapi_ground.BaseGround):
    is_passable = False
    color = None
    sprite_path = 'assets/images/fancy-impassable-50.png'
