import random
import numpy as np

class Player:
    def __init__(self) -> None:
        self.player_name = "test_3"
        self.image = "./img/original.gif"

    def choise_roll(self, rolls):
        return np.random.randint(0, 2)

    def choise(self, chance):
        if random.random() < 0.5:
            return True
        else:
            return False
