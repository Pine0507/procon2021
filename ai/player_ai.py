import random
import numpy as np
from typing import List
from .info_game import gameboard_info, players_info

class Player:
    def __init__(self) -> None:
        self.player_name = "test_1"
        self.image = "./img/original.gif"

    def get_myplayer(self):
        players = players_info()
        my_player_index = [
            idx
            for idx, player in enumerate(players)
            if player["player_name"] == self.player_name
        ][0]
        return players[my_player_index]

    def choise_roll(self, rolls: np.ndarray) -> int:
        # boardにはそれぞれのマスのprice(値段)，base_price(もとの値段)，
        board = gameboard_info()["board"]

        my_player = self.get_myplayer()
        my_position = my_player["position"]
        best_roll = rolls[0]
        for roll in rolls:
            destination_position = (my_position + roll) % len(board)
            if (
                board[destination_position]["own_player"] == 0
                or board[destination_position]["own_player"] == self.player_name
            ):
                best_roll = roll

        return list(rolls).index(best_roll)

    def choise(self, chance: str) -> bool:
        is_choised: bool
        # 増資するチャンスのとき
        if chance == "capital_increase":
            is_choised = True
        # 購入するチャンスのとき
        elif chance == "buy":
            is_choised = True
        else:
            raise ValueError(f"No such chance: {chance}")

        return is_choised