import random


class Player:
    def __init__(self) -> None:
        self.player_name = "test_1"

    def choise(self, chance):
        if random.random() < 0.5:
            return True
        else:
            return False
