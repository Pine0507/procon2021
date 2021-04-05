import dipict
from numpy.core.fromnumeric import choose
from gameboard import buy, capital_increase, is_my_property, payment, game_board, is_vacent_property
import numpy as np
import players_util
import pdb
from dipict import root
import time

i = 0
cn = 0
# count = マス目


def game_main():
    global i, cn
    i %= 4
    sugoroku = np.random.randint(1, 4)
    player = players_util.move(players_util.decide_player(i), sugoroku)
    # TODO:プレイやー移動描画
    dipict.delete_player(player)
    dipict.create_player(player["position"], 0, i)

    time.sleep(0.1)
    # 買う時
    if is_my_property(player) or is_vacent_property(player):
        chance = "capital_increase" if is_my_property(player) else "buy"
        # choise = True
        # 出目も渡す必要あり
        choise = player["player_ai"].choise(chance=chance)
        choise = True
        if choise:
            buy(player) if chance == "buy" else capital_increase(player)
    else:
        player = payment(player, i)
    for idx, ip in enumerate(players_util.players):
        print(str(ip)+"*" if idx == i else ip)
    for idx, game_board_ in enumerate(game_board):
        print(str(game_board_)+"*" if idx ==
              player["position"] else game_board_)
    players_util.set_player(i, player)
    # TODO:支払い後の描画

    dipict.change_gameboard()
    for player_idx, player in enumerate(players_util.players):
        dipict.update_player_info(player_idx)
        dipict.create_player(player["position"], 0, player_idx)
    root.after(100, game_main)
    print("")
    i += 1
    cn += 1


if __name__ == "__main__":
    game_main()
    root.mainloop()
