from gameboard import game_board
from config import Config
import tkinter
import players_util
from typing import List
players = players_util.players
config = Config()

width = config.WIDTH_WINDOW
height = config.HEIGHT_WINDOW
root = tkinter.Tk()
root.title("てすと")
canvas = tkinter.Canvas(width=width, height=height, bg='white')
canvas.pack()
idx_board = 0
max_board_len = config.MAX_BOARD_LENGTH
player_colors = ['red', 'blue', 'green', 'yellow']

# プレイヤー情報の描画
def depict_player(position_idxes: List, players_idx: int):
    # 要ランク決め関数
    rank = "現在{0}位".format(players_idx)
    x0, y0 = position_idxes # rectangle左上の座標インデックス
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
        text=text, justify='center')


for player_idx, position_idxes in enumerate([[1, 1], [5, 1], [1, 6], [5, 6]]):
    depict_player(position_idxes, player_idx)

    # 表示する情報：売値、価格（最初）
    # 一回増資したら：増資額、価格


# マス目描画
def create_rectangle(x: int, y: int) -> None:
    canvas.create_rectangle(
        x*width/max_board_len, y*height/max_board_len, (x+1)*width/max_board_len, (y+1)*height/max_board_len, fill='gray')

# マス情報描画
def create_text(x: int, y: int, idx_board: int) -> None:
    text = "利用料：{0}\n値段：{1}".format(game_board[idx_board]["base_price"]//10, game_board[idx_board]["base_price"])
    canvas.create_text((x+0.5)*width/max_board_len, (y+0.7)*height/max_board_len, text=text, justify='center')


for y in range(max_board_len):
    for x in range(max_board_len):
        if y in [0, max_board_len-1] or x in [0, max_board_len-1]:
            create_rectangle(x, y)
            create_text(x, y, idx_board)
            idx_board += 1


root.mainloop()
