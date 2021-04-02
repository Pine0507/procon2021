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

# プレイヤー情報の描画


def depict_player(position_idxes: List, players_idx: int):
    rank = "現在１位"
    text = f'{players[players_idx]["player_name"]}\n{rank}\n{players[0]["money"]}\n{players[0]["thing"]}'
    canvas.create_rectangle(
        position_idxes[0]*width / max_board_len,
        position_idxes[1]*height/max_board_len,
        (position_idxes[0]+4)*width/max_board_len,
        (position_idxes[1]+3)*height/max_board_len, fill='blue')
    canvas.create_text(
        4*width/max_board_len, 2.5*height/max_board_len, text=text, justify='center')


for player_idx, position_idxes in enumerate([[1, 1], [5, 1], [1, 6], [5, 6]]):
    depict_player(position_idxes, player_idx)

    # 表示する情報：売値、価格（最初）
    # 一回増資したら：増資額、価格


def create_rectangle(x: int, y: int) -> None:
    canvas.create_rectangle(
        x*width/max_board_len, y*height/max_board_len, (x+1)*width/max_board_len, (y+1)*height/max_board_len, fill='gray')


def create_text(x: int, y: int, idx_board: int) -> None:
    canvas.create_text((x+0.5)*width/max_board_len, (y+0.66)*height/max_board_len, text="値段："+str(
        game_board[idx_board]["base_price"]), justify='center')


for y in range(max_board_len):
    for x in range(max_board_len):
        if y in [0, max_board_len-1] or x in [0, max_board_len-1]:
            create_rectangle(x, y)
            create_text(x, y, idx_board)
            idx_board += 1


root.mainloop()
