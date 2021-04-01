import numpy as np
import players_util
game_board = [{"count": masu,
               "price": 0,
               "base_price": np.random.randint(10*masu, 10*(masu+1))*10,
               "own_player": 0,
               "level": 0} for masu in range(8)]

# 初期化処理
for idx in range(len(game_board)):
    game_board[idx]["price"] = game_board[idx]["base_price"]


levels = {
    "fee_per": [0.1, 0.15, 0.25, 0.5],
    "sale_per": [0.5 for _ in range(4)]}


def gameboard_info():
    return {"board": game_board, "levels": levels}


def get_game_pass(player):
    return game_board[player["position"]]


def get_player_position(player):
    return player["position"]


def buy(player: dict) -> dict:
    global game_board
    player_position = get_player_position(player)
    price = game_board[player_position]["price"]
    if player["money"] < price:
        return player
    else:
        player["money"] -= price
        player["thing"] += price
        game_board[player_position]["own_player"] = player["player_name"]
        game_board[player_position]["price"] = price
    return player


def is_vacent_property(player: dict) -> bool:
    game_mass = game_board[get_player_position(player)]
    return game_mass["own_player"] == 0


def is_my_property(player: dict) -> bool:
    game_mass = game_board[get_player_position(player)]
    return game_mass["own_player"] == player["player_name"]


def payment(player: dict, gameboard_idx: int):
    game_mass = get_game_pass(player)
    level = game_mass["level"]
    fee = int(game_mass["price"]*levels["fee_per"][level])
    player["money"] -= fee
    idx_owner = players_util.idx_player(game_mass["own_player"])
    owner_property = players_util.players[idx_owner]
    owner_property["money"] += fee
    players_util.set_player(idx_owner, owner_property)
    if is_bankruptcy(player, 1):
        print("hasan")
        import sys
        sys.exit()
    else:
        return player


def capital_increase(player: dict) -> dict:
    global game_board
    player_position = get_player_position(player)
    game_mass = get_game_pass(player)
    cap_fee = game_mass["base_price"]//2
    if player["money"] < cap_fee or game_board[player_position]["level"] == len(levels["fee_per"])-1:
        pass
    else:
        player["money"] -= cap_fee
        player["thing"] += cap_fee
        game_board[player_position]["price"] += cap_fee
        game_board[player_position]["level"] += 1
    return player


def is_bankruptcy(player, cn):
    global game_board
    players_belong = player["player_name"]
    prices = [game_board[idx]["price"]*0.5 if game_board[idx]["own_player"]
              == players_belong else 10**10 for idx in range(len(game_board))]
    while(player["money"] < 0):
        print(player)
        if min(prices) == 10**10:
            print("hasan")
            import sys
            sys.exit()
            return True
        game_board[prices.index(min(prices))]["own_player"] = 0
        player["money"] += min(prices)
        player["thing"] -= game_board[prices.index(min(prices))]["price"]
        prices[prices.index(min(prices))] = 10**10
