import random
import pygame
from mlgame.view.view_model import create_rect_view_data

rgb = ["#6C6587","#65877D","#EA95DD","#B5E192","#D1CF7D","#D1B77D","#885333","#C9ECE5","#636875","#E9DCF4","#56386F","#F36E9C"]

class Wall(pygame.sprite.Sprite):
    def __init__(self, init_pos: tuple, init_size: tuple):
        super().__init__()
        self.rect = pygame.Rect(*init_pos, *init_size)
        self.color = rgb[random.randint(0,11)]

    @property
    def xy(self):
        return self.rect.topleft

    @property
    def game_object_data(self):
        return create_rect_view_data(
            name="wall"
            , x=self.rect.x
            , y=self.rect.y
            , width=self.rect.width
            , height=self.rect.height
            , color=self.color
            , angle=0)








