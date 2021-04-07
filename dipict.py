from numpy.lib.type_check import imag
from gameboard import game_board, levels
from config import Config
import tkinter
import players_util
from typing import List
from PIL import Image, ImageTk
import gameboard
players = players_util.players
config = Config()

width = config.WIDTH_WINDOW
height = config.HEIGHT_WINDOW
root = tkinter.Tk()
root.title("てすと")
canvas = tkinter.Canvas(width=width*4, height=height, bg='white')
canvas.pack()
idx_board = 0
max_board_len = config.MAX_BOARD_LENGTH
player_colors = ['salmon1', 'SkyBlue1', 'SeaGreen1', 'khaki1']
player_icons = ['red', 'blue', 'green', 'yellow']
game_board_idxes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 19, 29, 39, 49, 59, 69, 79,
                    89, 99, 98, 97, 96, 95, 94, 93, 92, 91, 90, 80, 70, 60, 50, 40, 30, 20, 10]

# プレイヤー情報の描画


def depict_player(position_idxes: List, players_idx: int):
    # 要ランク決め関数
    rank = "現在{0}位".format(players_idx)
    x0, y0 = position_idxes  # rectangle左上の座標インデックス
    x1, y1 = x0+4, y0+3     # rectangle右下の座標インデックス
    text = f'{players[players_idx]["player_name"]}\n{rank}\n{players[0]["money"]}\n{players[0]["thing"]}'
    canvas.create_rectangle(
        x0 * width / max_board_len,
        y0 * height/max_board_len,
        x1 * width/max_board_len,
        y1 * height/max_board_len,
        fill=player_colors[players_idx])
    canvas.create_text(
        (x0 + 3)*width/max_board_len,
        (y0 + 1.5)*height/max_board_len,
        text=text, justify='center', tag="text_"+str(players_idx))


for player_idx, position_idxes in enumerate([[1, 1], [5, 1], [1, 6], [5, 6]]):
    depict_player(position_idxes, player_idx)

    # 表示する情報：売値、価格（最初）
    # 一回増資したら：増資額、価格


# マス目描画
def create_rectangle(x: int, y: int, color='gray') -> None:
    canvas.create_rectangle(
        x*width/max_board_len, y*height/max_board_len, (x+1)*width/max_board_len, (y+1)*height/max_board_len, fill=color)

# マス情報描画
# 上；利用料、下：増資学


def create_text(x: int, y: int, idx_board: int) -> None:
    fee_per = levels["fee_per"][game_board[idx_board]["level"]]
    text = "利用料：{0}\n値段：{1}".format(
        int(game_board[idx_board]["price"]*fee_per), int(game_board[idx_board]["price"]))
    canvas.create_text((x+0.5)*width/max_board_len, (y+0.7)
                       * height/max_board_len, text=text, justify='center')


# プレイヤー描画
def create_player(position: int, idx_player: int) -> None:
    global text
    game_board_idx = game_board_idxes[position]
    y, x = game_board_idx//10, game_board_idx % 10
    text = "●"
    fnt = ("Times New Roman", 40, "bold")
    canvas.create_text((x+(idx_player+1)/5)*width/max_board_len, (y+0.2)
                       * height/max_board_len, text=text, justify='center', fill=player_icons[idx_player], font=fnt, tag=players_util.players[idx_player]["player_name"])


def delete_player(player):
    canvas.delete(player["player_name"])


def change_gameboard():
    player_names = {}
    for idx, player in enumerate(players_util.players):
        player_names[player["player_name"]] = idx
    for idx_board, gameboard_idx in enumerate(game_board_idxes):
        y, x = gameboard_idx // 10, gameboard_idx % 10

        own_player = gameboard.game_board[idx_board]["own_player"]
        create_rectangle(
            x, y, player_colors[player_names[own_player]]) if not own_player == 0 else create_rectangle(x, y)
        create_text(x, y, idx_board)
    # for _ in range(config.LEN_BOARD):
    #     create_rectangle(_, 0)
    #     create_text(_, 0, _)
    # for game_board in gameboard.game_board:

        # 購入、売却、増資処理


def update_player_info(players_idx):
    # 要ランク決め関数
    canvas.delete("text_"+str(players_idx))
    players_money = [player["money"]+player["thing"]
                     for player in players_util.players]
    players_money_sorted = sorted(players_money, reverse=True)
    rank = "現在{0}位".format(
        players_money_sorted.index(players_money[players_idx])+1)
    positiones = [[1, 1], [5, 1], [1, 6], [5, 6]]
    x0, y0 = positiones[players_idx]  # rectangle左上の座標インデックス
    x1, y1 = x0+4, y0+3     # rectangle右下の座標インデックス
    text = f'{players[players_idx]["player_name"]}\n{rank}\n総資産{int(players[players_idx]["money"]+players[players_idx]["thing"])}\n所持金{int(players[players_idx]["money"])}\n資産{int(players[players_idx]["thing"])}'
    # canvas.create_rectangle(
    #     x0 * width / max_board_len,
    #     y0 * height/max_board_len,
    #     x1 * width/max_board_len,
    #     y1 * height/max_board_len,
    #     fill=player_colors[players_idx])
    # image = ImageTk.PhotoImage(Image.open(
    #     players[players_idx]["player_ai"].image))
    # canvas.create_image(0, 0, image=image)
    canvas.create_text(
        (x0 + 3)*width/max_board_len,
        (y0 + 1.5)*height/max_board_len,
        text=text, justify='center', tag="text_"+str(players_idx))


def announce(cn) -> None:
    canvas.create_rectangle(
        1*width/max_board_len, 4*height/max_board_len, 9*width/max_board_len, 6*height/max_board_len, fill='white')
    canvas.create_text(
        5*width/max_board_len,
        5*height/max_board_len,
        text="ターン数："+str(cn//4), justify='center')


# 初期化処理
for idx_board, gameboard_idx in enumerate(game_board_idxes):
    y, x = gameboard_idx // 10, gameboard_idx % 10
    create_rectangle(x, y)
    create_text(x, y, idx_board)

player_img_position = [(2.25, 2.5), (6.25, 2.5), (2.25, 7.5), (6.25, 7.5)]
player_imgs = []
for idx_player, player in enumerate(players_util.players):
    create_player(0, idx_player)
    image = Image.open(player["player_ai"].image).resize((100, 100))
    player_imgs.append(ImageTk.PhotoImage(image))
    image = player_imgs[idx_player]
    x, y = player_img_position[idx_player]
    canvas.create_image(x*width/max_board_len, y *
                        height/max_board_len, image=image)
