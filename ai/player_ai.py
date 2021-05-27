from os import RTLD_LOCAL
import random
import numpy as np
from typing import List
from .info_game import gameboard_info, players_info


class Player:
    def __init__(self) -> None:
        self.player_name = "Matsuo_no_Migawari"
        self.image = "./img/Matsuo_img.jpeg"

    def get_myplayer(self):
        players = players_info()
        my_player_index = [
            idx
            for idx, player in enumerate(players)
            if player["player_name"] == self.player_name
        ][0]
        return players[my_player_index]


# マス目選択関数


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

    def next_kouho_masu(self, roll, next_kouho):
        # my_player = self.get_myplayer()
        # my_position = my_player["position"]
        kouho_masu = next_kouho+roll
        if kouho_masu > 35:
            kouho_masu = kouho_masu - 36
        if kouho_masu < 0:
            kouho_masu = kouho_masu + 36
        kouho_masu_dict = gameboard_info()["board"][kouho_masu]
        return kouho_masu_dict

    def less_dam_choice(self, roll_list):
        my_player = self.get_myplayer()
        tanin_mise_count_list = []

        for roll in roll_list:

            tanin_mise_count = 0
            for next_kouho in range(1, 10):
                # もしそのマスに行った時、そのマスから9マスぶんはどういう状況か
                # 一番他人のマスに止まる確率が低いマスに行こう
                next_who_player_own = self.next_kouho_masu(roll, next_kouho)[
                    "own_player"]
                if next_who_player_own != "Matsuo_no_Migawari"\
                        and next_who_player_own != 0:
                    tanin_mise_count += 1

            tanin_mise_count_list.append(tanin_mise_count)

        min_count = min(tanin_mise_count_list)

        min_tanin_index = tanin_mise_count_list.index(min_count)

        best_roll = roll_list[min_tanin_index]

        # 被害最小のうち、一番進めるものを選ぶ
        for i in range(len(roll_list)):
            count = tanin_mise_count_list[i]
            if count == min_count and \
                    roll_list[i] > best_roll:

                best_roll = roll_list[i]

        return best_roll

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
                if (my_money - howmuch_price) > 50:
                    best_roll_list.append(roll)
                else:
                    good_roll_list.append(roll)

            # 次に自分のマス
            elif who_player_own == "Matsuo_no_Migawari":
                soso_roll_list.append(roll)

            else:
                bad_roll_list.append(roll)

        # 空き店に行く場合：最大値で行く
        if best_roll_list:
            best_roll = self.less_dam_choice(best_roll_list)

        elif good_roll_list:
            best_roll = self.less_dam_choice(good_roll_list)

        # 自分の店に行く場合
        elif soso_roll_list:
            best_roll = self.less_dam_choice(soso_roll_list)

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

#　増資、購入についての選択関数
    def choise(self, chance: str) -> bool:
        is_choised: bool
        my_player = self.get_myplayer()

        my_money = my_player["money"]
        my_position_price = self.now_mase_info("price")
        my_position_base = self.now_mase_info("base_price")
        fee_per_list = gameboard_info()["levels"]["fee_per"]
        fee_per_index = self.now_mase_info("level")

        # 増資するチャンスのとき
        if chance == "capital_increase":
            is_choised = True
            fee_per_index += 1

            if fee_per_index > 3:
                return False
            for roll in range(-7, 8):
                who_player_own = self.kouho_masu(roll)["own_player"]
                howmuch_price = self.kouho_masu(roll)["price"]
                if (my_position_base * fee_per_list[fee_per_index]) > howmuch_price and \
                        who_player_own != "Matsuo_no_Migawari" and who_player_own != 0:
                    is_choised = False

        # 購入するチャンスのとき
        elif chance == "buy":
            is_choised = False
            if (my_money - my_position_price) > 50:
                is_choised = True

        else:
            raise ValueError(f"No such chance: {chance}")

        return is_choised
