import random


class Player:
    def __init__(self) -> None:
        self.player_name = "test_2"
        self.image = "./img/original.gif"

    def choise(self, chance):
        if random.random() < 0.5:
            return True
        else:
            return False
