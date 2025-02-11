import dipict
from gameboard import buy, capital_increase, is_bankruptcy, is_my_property, payment, game_board, is_vacent_property
import numpy as np
import gameboard
import players_util
from dipict import root
import time
from copy import deepcopy
import random

i = 0
cn = 0
# count = マス目
bankruptcy_turn = 0


def game_main():
    global i, cn, bankruptcy_turn
    i %= 4
    dipict.announce(cn)
    sugoroku = random.sample(list(range(1, 10)), 3)
    tmp_sugoroku = deepcopy(sugoroku)
    sugoroku = sugoroku[players_util.players[i]
                        ["player_ai"].choise_roll(tmp_sugoroku)]
    player = players_util.move(players_util.decide_player(i), sugoroku)
    # TODO:プレイやー移動描画
    dipict.delete_player(player)
    dipict.create_player(player["position"], i)

    # time.sleep(0.1)
    # 買う時
    chance, choise = "", False
    if is_my_property(player) or is_vacent_property(player):
        chance = "capital_increase" if is_my_property(player) else "buy"
        # 出目も渡す必要あり
        choise = player["player_ai"].choise(chance=chance)
        if choise:
            buy(player) if chance == "buy" else capital_increase(player)
    else:
        player = payment(player, i)

    players_util.set_player(i, player)
    # TODO:支払い後の描画
    dipict.canvas.delete('all')
    dipict.dipict_player_info()

    dipict.change_gameboard()
    for player_idx, player in enumerate(players_util.players):
        dipict.update_player_info(player_idx)
        dipict.create_player(player["position"], player_idx)
    print("")
    root.after(100, game_main)
    if gameboard.bool_bankruptcy:
        if bankruptcy_turn == 0:
            bankruptcy_turn = cn
        if cn > bankruptcy_turn:
            print("hasan")
            time.sleep(0.1)
            while(True):
                pass
    i += 1
    cn += 1


if __name__ == "__main__":
    game_main()
    root.mainloop()
