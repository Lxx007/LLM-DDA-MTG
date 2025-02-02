import MTG_Game_Process as Game
import Current_Situation as Status

Player_1, Player_2 = Status.initial()
for i in range (7):
    Player_1 = Status.draw("Player", Player_1)
    Player_2 = Status.draw("DDA", Player_2)
Game.MTG_Game(Player_1, Player_2)
