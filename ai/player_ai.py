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

    def choise_roll(self, rolls: list) -> int:
        # my_player にはこんな感じで入っています
        # List[Dict{“money”:所持金，”thing”:資産，”position”:位置，”position_name":プレイヤー名 }]
        my_player = self.get_myplayer()
        my_position = my_player["position"]

        # boardにはそれぞれのマスのprice(値段)，base_price(もとの値段)
        # board には下の感じで入っています
        #  List[ Dict{ "count": マス目， "price": 物件の値段,
        #              "base_price":もとの値段, "own_player": 0 or プレイヤー名, "level": 物件レベル }]
        board = gameboard_info()["board"]
        now_position_price = board[my_position]["price"] 
        # gameboard_info()["levels"]には下のような感じで入っています
        #  levels = Dict {"fee_per": List[利用料比率×4個],"sale_per": 売却比率(0.5)}

        best_roll = rolls[0]
        for roll in rolls:
            if roll>best_roll:
                best_roll = roll

        return rolls.index(best_roll)

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
