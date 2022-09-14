import sys
from os import path

<<<<<<< HEAD
from src.MyGame import MyGame

=======
>>>>>>> aa2cb5e9e21f84fe86c615e148543219a4b27f49
sys.path.append(path.dirname(__file__))
from src.MyGame import MyGame

GAME_SETUP = {
    "game": MyGame,
}
