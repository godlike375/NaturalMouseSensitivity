from argparse import ArgumentParser

from source.calibrator.game import CalibrationGame
from source.calibrator.frametime import Frametime
from source.calibrator.mouse import MouseParamsController, FlickDetector, MouseParamsControllerV2
from source.calibrator.controller import Controller

def start_calibration_game(params):
    frametime = Frametime()
    game = CalibrationGame(params, frametime)
    flick_detector = FlickDetector()
    mouse = MouseParamsControllerV2(game, flick_detector)
    controller = Controller(game, mouse)
    game.app.run()


if __name__ == '__main__':
    parser = ArgumentParser(description='Sensitivity calibration')
    parser.add_argument('--target_count', type=int, help='Count of targets will be spawned')
    parser.add_argument('--target_range', type=int, help='Average range between spawned targets')
    args = parser.parse_args()
    start_calibration_game(args)