from os import path

import pygame
from mlgame.utils.enum import get_ai_name
from mlgame.view.view_model import create_image_view_data, create_asset_init_data

from .env import IMAGE_DIR
Vec = pygame.math.Vector2


class Bullet(pygame.sprite.Sprite):
    def __init__(self, construction: dict, **kwargs):
        """
        初始化玩家資料
        construction可直接由TiledMap打包地圖資訊後傳入
        :param construction:
        :param kwargs:
        """
        super().__init__()
        self.image_id = "bullet"
        self._id = construction["_id"]
        self._no = construction["_no"]
        self.rect = pygame.Rect(construction["_init_pos"], construction["_init_size"])
        self.rect.center = construction["_init_pos"]
        self._origin_xy = self.rect.topleft
        self._origin_center = self.rect.center
        self._angle = 0
        self._score = 0
        self._shield = 100
        self._lives = 3
        self._power = 10
        self.vel = Vec(0, 0)
        self._is_alive = True
        self._is_shoot = False
        self.play_rect_area = kwargs["play_rect_area"]
        self.move_steps = 15
        self.used_frame = 0
        self.last_move_frame = 0
        self.move_cd = 15
        self.speed = 10
        self.last_shoot_frame = 0
        if self._id == "mob":
            if self._id == "mob":
                self.angle = 180 * 3.14 // 180

    def move_up(self):
        self.vel.y = -self.speed
    def move_down(self):
        self.vel.y = self.speed

    def update(self) -> None:
        self.rect.center += self.vel
        if self._id == "player":
            self.move_up()
        else:
            self.move_down()
        """
        更新玩家資料
        self._used_frame += 1
        self.rect.center += self._vel
        self.act(command[get_ai_name(self._id)])
        if self._shield <= 0:
            self._lives -= 1
            self._shield = 100
            self.reset()
        if self._lives <= 0:
            self._is_alive = False
        :param command:
        :return:
        """

    def reset(self) -> None:
        """
        Reset Player center = origin_center
        :return:
        """
        self.rect.topleft = self._origin_xy

    def shoot(self) -> None:
        """
        _is_shoot = True
        :return:
        """
        if not self._is_shoot and self.used_frame - self.last_shoot_frame > 10:
            self._last_shoot_frame = self.used_frame
            self._is_shoot = True

    def stop_shoot(self) -> None:
        """
        _is_shoot = False
        :return:
        """
        self._is_shoot = False

    def add_score(self, score: int) -> None:
        """
        _score += score
        :param score:
        :return:
        """
        self._score += score

    def get_score(self) -> int:
        """
        :return: _score
        """
        return self._score

    def get_lives(self) -> int:
        """
        :return: _lives
        """
        return self._lives

    def get_shield(self) -> int:
        """
        :return: _shield
        """
        return self._shield

    def get_is_alive(self) -> bool:
        """
        :return: _is_alive
        """
        return self._is_alive

    def get_is_shoot(self) -> bool:
        """
        :return: _is_shoot
        """
        return self._is_shoot

    def set_is_shoot(self, is_shoot: bool) -> None:
        """
        _is_shoot = is_shoot
        :param is_shoot:
        :return:
        """
        self._is_shoot = is_shoot

    def reset_xy(self, new_pos=()) -> None:
        """
        :param new_pos:
        :return:
        """
        if new_pos:
            self.rect.topleft = new_pos
        else:
            self.rect.topleft = self._origin_xy

    def get_xy(self) -> tuple:
        """
        :return: topleft
        """
        return self.rect.topleft

    def get_size(self) -> tuple:
        """
        :return: width, height
        """
        return self.rect.width, self.rect.height

    def get_center(self) -> tuple:
        """
        :return: center
        """
        return self.rect.center

    def get_id(self) -> int:
        """
        :return: center
        """
        return self._id

    def get_data_from_obj_to_game(self) -> dict:
        """
        在遊戲主程式獲取遊戲資料給AI時被調用
        :return:
        """
        info = {"id": f"{self.image_id}_{self.id}"
            , "x": self.rect.x
            , "y": self.rect.y
                }
        return info

    def get_obj_progress_data(self) -> dict or list:
        """
        使用view_model函式，建立符合mlgame物件更新資料格式的資料，在遊戲主程式更新畫面資訊時被調用
        :return:
        """
        image_data = create_image_view_data(f"{self.image_id}_{self.no}", *self.rect.topleft, *self.get_size(), self.angle)
        return image_data

    def get_obj_init_data(self) -> dict or list:
        """
        使用view_model函式，建立符合mlgame物件初始資料格式的資料，在遊戲主程式初始畫面資訊時被調用
        :return:
        """
        image_init_data = create_asset_init_data(f"mob", self.rect.width, self.rect.height
                                                 , path.join(IMAGE_DIR, "mob.png"), "url")
        return image_init_data

    def get_info_to_game_result(self):
        info = {"id": f"{self._id}P"
                , "x": self.rect.x
                , "y": self.rect.y
                }
        return info

