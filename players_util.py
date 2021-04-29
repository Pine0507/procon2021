from ai.player_ai_4 import Player as Player_4
from ai.player_ai_3 import Player as Player_3
from ai.player_ai_2 import Player as Player_2
from ai.player_ai import Player as Player_1
from config import Config
cfg = Config()
player_aies = [Player_1(), Player_2(), Player_3(), Player_4()]
player_names = [player_ai.player_name for player_ai in player_aies]
players = [{"money": 1000,
            "thing": 0,
            "position": i*9,
            "player_name": player_names[i],
            "player_ai":player_ai} for i,
           player_ai in enumerate(player_aies)]


def players_info():
    return [{"money": player["money"],
             "thing": player["thing"],
             "position": player["position"],
             "player_name": player["player_name"]} for player in players]


def set_player(idx: int, player: dict):
    global players
    players[idx] = player


def decide_player(idx_player: int) -> dict:
    return players[idx_player]


def idx_player(player_name: str) -> int:
    return player_names.index(player_name)


def move(player: dict, count: int) -> dict:
    player_position = player["position"]
    player_position += count
    player_init_position = player_names.index(player["player_name"])*9
    if player_init_position == 0:
        if player_position // cfg.LEN_BOARD > 0:
            player["money"] += cfg.BONUS
    else:
        if player["position"] < player_init_position <= player_position:
            player["money"] += cfg.BONUS
    player_position %= cfg.LEN_BOARD

    player["position"] = player_position
    return player
