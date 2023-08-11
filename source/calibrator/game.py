from ursina import *
from ursina import window
from ursina import camera
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader

from source.calibrator.frametime import Frametime
from source.aliases import Vector



class CalibrationGame:

    def __init__(self, params, frametime: Frametime):
        self.app = Ursina()
        window.vsync = True
        self.frametime = frametime

        Entity.default_shader = lit_with_shadows_shader

        floor_and_walls_visible = True

        self.ground = Entity(model='plane', collider='box', scale=(128, 1, 128), texture='grass',
                             texture_scale=(4, 4), visible=floor_and_walls_visible, position=(0, 0, -76))

        # anchor_sphere = Entity(model='plane', collider='sphere', scale=(1280, 1280, 1280), texture_scale=(4,4), visible=False)

        self.player = FirstPersonController(model='cube', z=-12, color=color.orange,
                                            visible=floor_and_walls_visible)  # , origin_y=-.5, speed=8, visible=False)

        #self.valorant_sens = 0.581

        self.valorant_sens = 0.592

        self.sensitivity = self.valorant_sens * 45.95


        self.player.mouse_sensitivity = Vec2(self.sensitivity, self.sensitivity)

        self.player_start_position = self.player.position

        # shootables_parent = Entity()
        # mouse.traverse_target = shootables_parent

        camera.fov = 103  # Camera FOV for Valorant
        # TODO: move into start settings and make a setting
        target_size = 1.3
        self.target = Entity(model='sphere', origin_y=-.5, scale=target_size,  # texture='vingette', texture_scale=(1,2),
                             collider='sphere',
                             color=color.hsv(random.uniform(0, 360), random.uniform(0, 1), random.uniform(0, 1))
                             )

        self.left_down = False

    def reset_player_position(self):
        self.player.position = self.player_start_position

    def get_camera_position_and_direction(self):
        return self.player.camera_pivot.world_position, self.player.camera_pivot.forward

    def move_target(self, x=None, y=None, z=None, target=None):
        target = target or self.target
        target.setX(x or target.x)
        target.setY(y or target.y)
        target.setZ(z or target.z)