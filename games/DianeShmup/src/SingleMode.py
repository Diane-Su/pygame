import pygame

from os import path
from mlgame.game.paia_game import GameResultState, GameStatus
from mlgame.utils.enum import get_ai_name
from mlgame.view.view_model import create_asset_init_data

from game_module.TiledMap import create_construction
from .Player import Player
from .Mob import Mob
from .env import IMAGE_DIR


class SingleMode:
    def __init__(self, play_rect_area: pygame.Rect):
        pygame.init()
        self._user_num = 1
        self.scene_width = play_rect_area.width
        self.scene_height = play_rect_area.height
        self.scene_height_center = self.scene_height // 2
        self.scene_width_center = self.scene_width // 2
        self.play_rect_area = play_rect_area
        self.all_sprites = pygame.sprite.Group()
        self.player = Player(create_construction(get_ai_name(0), 0, (self.scene_width_center, 530), (50, 50)), self.play_rect_area)
        self.all_sprites.add(self.player)
        self.mobs = pygame.sprite.Group()
        count = 0
        for x in range(50, self.scene_width - 50, 50):
            for y in range(50, self.scene_height_center, 50):
                count += 1
                mob = Mob(create_construction(_id=f"mob_{count}", _no=count, _init_pos=(x, y), _init_size=(50, 50)), play_rect_area=play_rect_area)
                self.mobs.add(mob)
        print(len(self.mobs))
        self.used_frame = 0
        self.state = GameResultState.FAIL
        self.status = GameStatus.GAME_ALIVE

    def update(self, command: dict) -> None:
        self.used_frame += 1
        self.player.update(command)
        self.mobs.update()
        if not self.player.get_is_alive():
            self.get_player_end()

    def reset(self) -> None:
        self.__init__(self.play_rect_area)

    def get_player_end(self):
        self.set_result(GameResultState.FINISH, GameStatus.GAME_OVER)

    def set_result(self, state: str, status: str):
        self.state = state
        self.status = status

    def get_player_result(self) -> list:
        """Define the end of game will return the player's info for user"""
        res = []
        get_res = self.player.get_info_to_game_result()
        get_res["state"] = self.state
        get_res["status"] = self.status
        get_res["used_frame"] = self.used_frame
        res.append(get_res)
        return res

    def check_collisions(self):
        raise Exception("Please overwrite check_collisions")

    def get_init_image_data(self):
        init_image_data = [self.player.get_obj_init_data()]
        for mob in self.mobs:
            if isinstance(mob, Mob):
                init_image_data.append(mob.get_obj_init_data())
        init_image_data.append(create_asset_init_data(f"bullet", *(12, 27), path.join(IMAGE_DIR, f"bullet.png"), "url"))
        return init_image_data

    def get_ai_data_to_player(self):
        to_player_data = self.player.get_data_from_obj_to_game()
        to_player_data["used_frame"] = self.used_frame
        to_player_data["status"] = self.status
        to_player_data["player_info"] = [self.player.get_data_from_obj_to_game()]

        return {get_ai_name(0): to_player_data}

    def get_background_view_data(self) -> list:
        background_view_data = []
        return background_view_data

    def get_obj_progress_data(self) -> list:
        obj_progress_data = self.draw_player()
        for mob in self.mobs:
            if isinstance(mob, Mob):
                obj_progress_data.append(mob.get_obj_progress_data())
        return obj_progress_data

    def get_bias_toggle_progress_data(self) -> list:
        bias_toggle_progress_data = []
        return bias_toggle_progress_data

    def get_toggle_progress_data(self) -> list:
        toggle_data = []
        return toggle_data

    def get_foreground_progress_data(self) -> list:
        foreground_data = []
        return foreground_data

    def get_user_info_data(self) -> list:
        user_info_data = []
        return user_info_data

    def get_game_sys_info_data(self) -> dict:
        game_sys_info_data = {}
        return game_sys_info_data

    def draw_player(self) -> list:
        player_data = self.player.get_obj_progress_data()

        return player_data

    def debugging(self, is_debug: bool) -> list:
        if is_debug:
            raise Exception("Please over writing debugging")
        return []
