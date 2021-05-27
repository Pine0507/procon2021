import random
import numpy as np
from typing import List
from .info_game import gameboard_info, players_info


class Player:
    def __init__(self) -> None:
        self.player_name = "test_200"
        self.image = "./img/original.gif"

    def get_myplayer(self):
        players = players_info()
        my_player_index = [
            idx
            for idx, player in enumerate(players)
            if player["player_name"] == self.player_name
        ][0]
        return players[my_player_index]

    def kouho_masu(self, roll):
        my_player = self.get_myplayer()
        my_position = my_player["position"]
        kouho_masu = my_position+roll
        if kouho_masu > 35:
            kouho_masu = kouho_masu - 36
        if kouho_masu < 0:
            kouho_masu = kouho_masu + 36
        kouho_masu_dict = gameboard_info()["board"][kouho_masu]
        return kouho_masu_dict

    def now_mase_info(self, element):
        my_player = self.get_myplayer()
        my_position = my_player["position"]
        info = gameboard_info()["board"][my_position][element]
        return info

    def choise_roll(self, rolls: list) -> int:
        # my_player にはこんな感じで入っています
        # List[Dict{“money”:所持金，”thing”:資産，”position”:位置，”position_name":プレイヤー名 }]
        my_player = self.get_myplayer()
        # my_position = my_player["position"]
        my_money = my_player["money"]

        # gameboard_info()["board"]
        # board には下の感じで入っています
        #  List[ Dict{ "count": マス目， "price": 物件の値段,
        #              "base_price":もとの値段, "own_player": 0 or プレイヤー名, "level": 物件レベル }]

        # gameboard_info()["levels"]には下のような感じで入っています
        #  levels = Dict {"fee_per": List[利用料比率×4個],"sale_per": 売却比率(0.5)}
        best_roll = 0
        best_roll_list = []
        good_roll_list = []
        soso_roll_list = []
        bad_roll_list = []

        for roll in rolls:
            who_player_own = self.kouho_masu(roll)["own_player"]
            howmuch_price = self.kouho_masu(roll)["price"]
            # まず、空いてるマス。
            if who_player_own == 0:
                if (my_money - howmuch_price) > 200:
                    best_roll_list.append(roll)
                else:
                    good_roll_list.append(roll)

            # 次に自分のマス
            elif who_player_own == "Matsuo_no_Migawari":
                soso_roll_list.append(roll)

            else:
                bad_roll_list.append(roll)

        # 買える空き店に行く場合：最大値で行く
        if best_roll_list:
            b_roll = best_roll_list[0]
            for roll in best_roll_list:
                if b_roll < roll:
                    b_roll = roll
            best_roll = b_roll

        elif good_roll_list:
            good_roll = good_roll_list[0]
            for roll in good_roll_list:
                if good_roll < roll:
                    good_roll = roll
            best_roll = good_roll

        # 自分の店に行く場合
        elif soso_roll_list:
            soso_roll = soso_roll_list[0]
            for roll in soso_roll_list:
                if soso_roll < roll:
                    soso_roll = roll
            best_roll = soso_roll

        # どこに行ってもダメな時は一番被害が少ないところへ
        else:
            worst_best_roll = bad_roll_list[0]
            worst_best_value = self.kouho_masu(worst_best_roll)["price"]
            for roll in bad_roll_list:
                if worst_best_value > self.kouho_masu(roll)["price"]:
                    worst_best_value = self.kouho_masu(roll)["price"]
                    worst_best_roll = roll
                # 一緒ならより多く進む
                elif worst_best_value == self.kouho_masu(roll)["price"] and worst_best_roll < roll:
                    worst_best_roll = roll

                else:
                    pass

            best_roll = worst_best_roll

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
