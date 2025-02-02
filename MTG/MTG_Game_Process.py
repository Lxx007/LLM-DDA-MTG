import random
import copy
import LLM_Connection as LLM
import Prompts_MTG as prompt
import referee_MTG as ref
import Current_Situation

Player_1 = "Player"
Player_2 = "DDA"

def SetupPhase (P1, P2):
    Invalid_Action = ""
    Invalid = ""
    response = False
    # Player 1 Setup
    count = 0
    while (True):
        if response == False:
            Invalid_Action = Invalid
            sys_p, usr_p = prompt.prompt_setup(Player_1, Invalid_Action, P1, P2)
            Action = LLM.get_chat_response(sys_p, usr_p)
            print (sys_p)
            print (usr_p)
            print (Action[0])
            response, Invalid, P1, P2, count = ref.ref_setup(Player_1, Action, P1, P2, count)
            # response, Invalid = ref.ref_setup(Action)
        else:
            Invalid_Action = ""
            Invalid = ""
            response = False
            break

    # Player 2 Setup
    while (True):
        if response == False:
            Invalid_Action = Invalid_Action + Invalid
            sys_p, usr_p = prompt.prompt_setup(Player_2, Invalid_Action, P1, P2)
            Action = LLM.get_chat_response(sys_p, usr_p)
            print (sys_p)
            print (usr_p)
            print (Action[0])
            response, Invalid, P1, P2, count  = ref.ref_setup(Player_2, Action, P1, P2, count)
            # response, Invalid = ref.ref_setup(Action)
        else:
            Invalid_Action = ""
            Invalid = ""
            response = False
            break
    return P1, P2

def Round_Switch (Initial_State, Active_Player, Pending_Player):
    if Initial_State:
        while (True):
            P1_Dice = random.randint(1,6)
            P2_Dice = random.randint(1,6)
            if P1_Dice != P2_Dice:
                break
        if P1_Dice > P2_Dice:
            Active_Player = Player_1
            Pending_Player = Player_2
        else:
            Active_Player = Player_2
            Pending_Player = Player_1
    else:
        R_Player = Active_Player
        Active_Player = Pending_Player
        Pending_Player = R_Player
    return Active_Player, Pending_Player

def DrawPhase (Active_Player, Player):
    # Player Draw
    Player = Current_Situation.draw(Active_Player, Player)
    return Player

def MainPhase (Active_Player, Active_P, Pending_P, Landcount = 0):
    print ("Start Main Phase-----------------------------------------------------------------------------------------------------------")
    Invalid_Action = ""
    Invalid = ""
    Invalid_pool = []
    response = False
    Land_count = Landcount
    # Player Main
    while (True):
        if response == False:
            for ii in Invalid_pool:
                Invalid_Action = Invalid_Action + "\n" + ii
            sys_p, usr_p = prompt.prompt_main(Active_Player, Invalid_Action, Active_P, Pending_P)
            Action = LLM.get_chat_response(sys_p, usr_p)
            print (sys_p)
            print (usr_p)
            print (" ")
            print ("LLM Answer Main------------------------------------------------------------------------------")
            print (Action[0])
            print ("----------------------------------------------------------------------------------------")
            # ID, answer, P1, P2, Land_count
            response, Invalid, Active_P, Pending_P, Land_count = ref.Main_Selection(Active_Player, Action[0], Active_P, Pending_P, Land_count)
            # Logs
            if Invalid == "":
                print ("Sataus update----------------------------------------------------------------------------------------")
                print (" ")
                print ("Enemy Hand-------------------------------------------------------------------------------------------")
                print (Pending_P[1])
                print ("Enemy Battlefield------------------------------------------------------------------------------------")
                print (Pending_P[2])
                print (" ")
                print ("-----------------------------------------------------------------------------------------------------")
                print (" ")
                print (Active_P[2])
                print ("Player Battlefield-----------------------------------------------------------------------------------")
                print (Active_P[1])
                print ("Player Hand------------------------------------------------------------------------------------------")
                print (" ")
                print ("Current status---------------------------------------------------------------------------------------")
            else:
                print ("LLM Invalid Operation")
                print (Invalid)
                if Invalid not in Invalid_pool:
                    Invalid_pool.append(copy.deepcopy(Invalid))
        else:
            Invalid_Action = ""
            Invalid_pool = []
            response = False
            break
    print ("Main phase end")
    return Active_P, Pending_P, Land_count

def CombatPhase (Active_Player, Pending_Player, Active_P, Pending_P):
    Invalid_Action = ""
    Invalid = ""
    response = False
    All_Attacks = []
    # Player Combat
    while (True):
        if response == False:
            Invalid_Action = Invalid_Action + Invalid
            sys_p, usr_p = prompt.prompt_combat(Active_Player, Invalid_Action, Active_P, Pending_P)
            Action = LLM.get_chat_response(sys_p, usr_p)
            print (sys_p)
            print (usr_p)
            print (" ")
            print ("LLM Answer Attack-----------------------------------------------------------------------")
            print (Action[0])
            print ("----------------------------------------------------------------------------------------")
            response, Invalid, Active_P, Pending_P, Attackers = ref.ref_combat(Active_Player, Action[0], Active_P, Pending_P)
            for ai in Attackers:
                All_Attacks.append(copy.deepcopy(ai))
                Active_P[2][ai[0]][1][5] = copy.deepcopy(1)
        else:
            Invalid_Action = ""
            Invalid = ""
            response = False
            break
    if len(All_Attacks) != 0:
        Active_P, Pending_P = BlockStep(Pending_Player, All_Attacks, Active_P, Pending_P) 
        return Active_P, Pending_P
    else:
        return Active_P, Pending_P

def BlockStep (Pending_Player, Attackers, Active_P, Pending_P):
    Invalid_Action = ""
    Invalid = ""
    response = False
    Block_position = []
    Blockers = []
    # Player Block
    while (True):
        if response == False:
            Invalid_Action = Invalid_Action + Invalid
            sys_p, usr_p = prompt.prompt_block(Pending_Player, Invalid_Action, Attackers, Pending_P, Active_P)
            Action = LLM.get_chat_response(sys_p, usr_p)
            print (sys_p)
            print (usr_p)
            print (" ")
            print ("LLM Answer Defence----------------------------------------------------------------------")
            print (Action[0])
            print ("----------------------------------------------------------------------------------------")
            Attacker, Blocker, Block_index, Invalid, Action, response = ref.ref_block(Pending_Player, Active_P, Pending_P, Action[0], Attackers)
            if len(Blocker) != 0:
                Blockers.append(copy.deepcopy(Blocker))
                Block_position.append(copy.deepcopy(Block_index))
                Pending_P[2][Block_index][1][5] = copy.deepcopy(1)
        else:
            Invalid_Action = ""
            Invalid = ""
            response = False
            break
    Active_P, Pending_P = ref.CombatSummary(Attacker, Blocker, Block_index, Active_P, Pending_P)
    return Active_P, Pending_P

def UntapPhase (Active_P):
    for i in Active_P[2]:
        i[1][5] = copy.deepcopy(0)
    return Active_P


def MTG_Game(P1, P2):
    Initial_State = True
    Active_Player = Pending_Player = None
    P1, P2 = SetupPhase (P1, P2)
    while (Current_Situation.Decision(P1, P2)):
        Active_Player, Pending_Player = Round_Switch (Initial_State, Active_Player, Pending_Player)
        if Initial_State == True:
            if Active_Player == "Player":
                Active_P = P1
                Pending_P = P2
            elif Active_Player == "DDA":
                Active_P = P2
                Pending_P = P1
            Initial_State = False
        else:
            Buffer_P = copy.deepcopy(Active_P)
            Active_P = copy.deepcopy(Pending_P)
            Pending_P = copy.deepcopy(Buffer_P)
        Active_P = DrawPhase(Active_Player, Active_P)
        Active_P = UntapPhase(Active_P)
        Active_P, Pending_P, Land_count = MainPhase (Active_Player, Active_P, Pending_P)
        Active_P, Pending_P = CombatPhase (Active_Player, Pending_Player, Active_P, Pending_P)
        Active_P, Pending_P, Land_count = MainPhase (Active_Player, Active_P, Pending_P, Land_count)
        if Current_Situation.Decision(P1, P2) == False:
            break

