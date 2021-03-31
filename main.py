import numpy as np
import pdb
game_board = [{"count":masu,
               "price":0,
               "base_price":np.random.randint(10*masu,10*(masu+1))*10,
               "player_belong":0,
               "level":0} for masu in range(8)]
for idx in range(len(game_board)):
    game_board[idx]["price"]=game_board[idx]["base_price"]
#count = マス目
# コメント
player_names=["A","B","C","D"]
players=[{"money":1000,"thing":0,"position":0,"player_name":player_names[i]} for i in range(4)]

levels={
         "fee_per":[0.1,0.15,0.25,0.5],
         "sale_per":[0.5 for _ in range(4)]}
i = 0
cn = 0
def sale(player,cn):
    players_belong=player["player_name"]
    prices=[game_board[idx]["price"]*0.5 if game_board[idx]["player_belong"]==players_belong else 10**10 for idx in range(len(game_board))]
    while(player["money"]<0):
        print(player)
        if min(prices)==10**10:
            print("hasan",cn)
            import  sys
            sys.exit()
        game_board[prices.index(min(prices))]["player_belong"]=0
        player["money"]+=min(prices)
        player["thing"]-=game_board[prices.index(min(prices))]["price"]
        prices[prices.index(min(prices))]=10**10

while(cn < 1000):
    i %= 4
    sugoroku = np.random.randint(1,4)
    players[i]["position"] += sugoroku
    players[i]["position"] %= 8
    player=players[i]
    owner=game_board[player["position"]]["player_belong"]
    player_position=player["position"]
    price=game_board[player_position]["price"]
    base_price=game_board[player_position]["base_price"]
    level = game_board[i]["level"]
    #買う時
    if not owner:
        if player["money"]<price:
            pass
        else:
            player["money"]-=price
            player["thing"]+=price
            game_board[player_position]["player_belong"]=player["player_name"]
            game_board[player_position]["price"]=price
    #自分の物件ではないが、買われている時
    elif owner!=player_names[i]:
        fee=int(price*levels["fee_per"][level])
        player["money"]-=fee
        if player["money"]<0:
            sale(player,cn)
        players[player_names.index(owner)]["money"]+=fee
    #自分の物件
    else:
        if level>3:
            pass
        else:
            print("zousi")
            cap_fee=base_price//2
            if player["money"]<cap_fee:
                pass
            else:
                player["money"] -= cap_fee
                player["thing"] += cap_fee
                game_board[player_position]["price"] += cap_fee
                game_board[player_position]["level"]+=1



    # ___
    # _ _
    # A__

    # position_plot=["_" for _ in range(len(game_board))]
    # for _,player in enumerate(players):
    #     position_plot[player["position"]]+=player["player_name"]
    # print(position_plot)
    for idx,ip in enumerate(players):
        # if idx==i:
        #     print(str(ip)+"*")
        # else:
        #     print(ip)
        print(str(ip)+"*" if idx==i else ip)
    for idx,game_board_ in enumerate(game_board):
        print(str(game_board_)+"*" if idx==player["position"] else game_board_)
    print("")

    i += 1
    cn += 1