import random
from random import randint

from ursina import Entity, held_keys, raycast

from source.calibrator.game import CalibrationGame
from source.aliases import Vector
from source.calibrator.mouse import MouseParamsController, MouseParamsControllerV2
from source.model.core import Target, FlickAndTarget, calculate_average_delta_diff, vector_length_distance


class Controller(Entity):
    def __init__(self, game: CalibrationGame, mouse: MouseParamsControllerV2, targets_count: int = 25):
        super().__init__()
        self.left_down = game.left_down
        self.player = game.player
        self.game = game
        self.camera = mouse
        self._calibration_results = []
        self._calibration_targets_count = targets_count

    def update(self):
        self.game.reset_player_position()
        self.left_click_detect()
        if self.camera.ready():
            self.camera.update_params()

    def left_click_detect(self):
        if held_keys['left mouse']:
            if not self.left_down:
                self.left_down = True
                self.on_left_clicked()
        else:
            self.left_down = False

    def on_left_clicked(self):
        camera_position, camera_direction = self.game.get_camera_position_and_direction()
        target = self.game.target
        # Направление, в котором смотрит игрок
        # TODO: get end - start of vector between origin and the center of target and normalize it
        #  and find angle between this direction vector and variable "direction"

        # ray = raycast(camera_position, camera_direction, debug=False, ignore=(self.player, self.game.ground))

        target_center = target.world_position
        target_center.y += target.scale.y / 2

        to_target: Vector = target_center - camera_position
        to_target_norm = to_target.normalized()


        self.camera.set_end_point(camera_direction)
        self.clicked_target(to_target_norm)
        self.camera.set_start_point(camera_direction)


        # ray2 = raycast(camera_position, to_target_norm, debug=True, ignore=(self.player, self.game.ground))
        x, y, z = random.uniform(-3.6, 3.6), random.uniform(-0.9, 0.9), random.uniform(-1.95, 1.95)
        self.game.move_target(x, y, z, target)

        # if ray.hit:
        #     hit_point = ray.world_point
        #     delta = target_center - hit_point
        #     delta_direction = delta.normalized()
        #     ray3 = raycast(hit_point, delta_direction, debug=True,
        #                    ignore=(self.player, self.game.ground), distance=vector_length_distance(delta))
        #     # У мишеней pivot point где-то внизу, а не в центре, поэтому прибавляем половину длины объекта



    def clicked_target(self, ideal_to_target_center_vec: Vector):
        if self.camera.last_flick is not None:
            flick_target = FlickAndTarget(self.camera.last_flick, Target(ideal_to_target_center_vec))
            self.camera.last_flick = None
            self._calibration_targets_count -= 1
            self._calibration_results.append(flick_target)
            if self._calibration_targets_count == 0:
                print(calculate_average_delta_diff(self._calibration_results))