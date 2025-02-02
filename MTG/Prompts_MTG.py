import numpy as np
import copy

def system_prompt (ID):
    if ID == "DDA":
        obj_txt = "Balance your life points with your opponent's. Aim to make the difference as close to zero as possible. Be aggresive!"
    elif ID == "Player":
        obj_txt = "Reduce your opponent's life points from 20 to 0. Be aggresive!"
    else:
        return "ERROR"

    sys_prompt = f"""You are a Magic: The Gathering player engaged in a game with an opponent. You already own a deck. You start with 20 life points.
Magic: The Gathering Rules for you:
Your Objective: {obj_txt}
The game flow of Magic: The Gathering includes the following phases:
The Setup Phase, which is executed only once at the initial of the game, allows you to change your hand as needed.
Each turn consists of the Draw Phase, Main Phase, Combat Phase, Opponent's Declare Blockers Step, and Ending Phase.
Critical Term Explanation:
Remember to play Land in each round, if you can.
Mana: To generate mana, you must TAP a land. Lands produce a color of mana indicated on the card. Land cards are not spells. You may play one during each of your turns for free.
Creatures: Creature cards can attack opponents or block their attacks.
Spells: Include instants, sorceries, enchantments, etc.
Abilities: Creatures and other permanents may have special abilities.
"""

    return sys_prompt

def info_change (set_situation):
    prompt_info = []
    if set_situation != []:
        for i in set_situation:
            Card_info_D = i[0]
            for j in range (len(i[1])):
                # mana cost
                if j == 0:
                    Card_info_D = Card_info_D + ". Mana cost = " + i[1][j] + ". " 
                # card type
                elif j == 1:
                    Card_info_D = Card_info_D + "Card type = " + i[1][j] + ". " 
                # power
                elif j == 2:
                    Card_info_D = Card_info_D + "Power = " + i[1][j] + ". " 
                # toughness
                elif j == 3:
                    Card_info_D = Card_info_D + "Toughness = " + i[1][j] + ". " 
                # card description
                elif j == 4:
                    Card_info_D = Card_info_D + "Card description = " + i[1][j] + ". " 
                # Tapped
                elif j == 5:
                    if i[1][j] == 1:
                        Card_info_D = Card_info_D + "Has Tapped. " 
                # Flying
                elif j == 6:
                    if i[1][j] == 1:
                        Card_info_D = Card_info_D + "Has Flying. " 
                # Hexproof
                elif j == 7:
                    if i[1][j] == 1:
                        Card_info_D = Card_info_D + "Has Hexproof. " 
                # Menace
                elif j == 8:
                    if i[1][j] == 1:
                        Card_info_D = Card_info_D + "Has Menace. " 
                # Defender
                elif j == 9:
                    if i[1][j] == 1:
                        Card_info_D = Card_info_D + "Has Defender. " 
                # Reach
                elif j == 10:
                    if i[1][j] == 1:
                        Card_info_D = Card_info_D + "Has Reach. " 
                # Trample
                elif j == 11:
                    if i[1][j] == 1:
                        Card_info_D = Card_info_D + "Has Trample. " 
                # Deathtouch
                elif j == 12:
                    if i[1][j] == 1:
                        Card_info_D = Card_info_D + "Has Deathtouch. " 
                # Vigilance
                elif j == 13:
                    if i[1][j] == 1:
                        Card_info_D = Card_info_D + "Has Vigilance. " 
                # First strike
                elif j == 14:
                    if i[1][j] == 1:
                        Card_info_D = Card_info_D + "Has First strike. " 
                # Can't be blocked by creatures with power 2 or less
                elif j == 15:
                    if i[1][j] == 1:
                        Card_info_D = Card_info_D + "Can't be blocked by creatures with power 2 or less. " 
                # Can't be blocked by more than one creature.
                elif j == 16:
                    if i[1][j] == 1:
                        Card_info_D = Card_info_D + "Can't be blocked by more than one creature. " 
                # Can't be blocked by black creatures
                elif j == 17:
                    if i[1][j] == 1:
                        Card_info_D = Card_info_D + "Can't be blocked by black creatures. " 
            prompt_info.append(copy.deepcopy(Card_info_D))
    return prompt_info

def prompt_setup(ID, InValid_Action, P1, P2):
    # 0: Library, 1: Hand, 2: Battlefield, 3: Graveyard, 4: LifePoint
    # Current_Phase_Official_Explanation, Critical_Term_Explanation  = Explain.setup()
    P2_0_D = info_change(P2[0])
    P1_1_D = info_change(P1[1])
    P2_1_D = info_change(P2[1])
    
    Current_Situation_P1_D = [P1_1_D]
    Current_Situation_P2_D = [P1_1_D, P2_1_D, P2_0_D]

    Current_Situation_P1 = f"""
Your Hand is: {Current_Situation_P1_D[0]}.
"""

    Current_Situation_P2 = f"""
Your Library is: {Current_Situation_P2_D[2]};
Your opponent Hand is: {Current_Situation_P2_D[0]}.
"""

    if InValid_Action == "":
        Additional_Prompt = ""
    else:
        Additional_Prompt = f"""
Warning:
{InValid_Action}
"""
    if ID == "DDA":
        Sys_Prompt = system_prompt(ID)
        User_Prompt = f"""You need to determine your actions based on the following statement.
Currently, it is the Setup Phase.
Please select between 5 and 7 cards from your library to form your hand.
Please consider your next move step by step, taking into account the strength of each card, the mana cost required, the special abilities of each card, and your own health.
In addition, you should respond using the following format /Cards: CardName1, CardName2, ...
Current Situation: {Current_Situation_P2}
""" + Additional_Prompt
    elif ID == "Player":
        Sys_Prompt = system_prompt(ID)
        User_Prompt = f"""You need to determine your actions based on the Phase Explanation and Critical Term Explanation.
Currently, it is the Setup Phase.
Do you want to MULLIGAN? 
Please consider your next action step by step, taking into account the strength of each card, the mana cost required, the special abilities of each card, and your own health.
Additionally, you should respond using the following format: /Your Answer :(YES or NO)
Phase Explanation: In this phase, your HAND will have seven cards from your LIBRARY. If a you are unhappy with your hand, they may take a MULLIGAN.
Critical Term Explanation: To MULLIGAN, shuffle your hand into your LIBRARY and draw seven cards. Then, put a card of your choice on the bottom of your LIBRARY for each time you MULLIGANED this game.
Current Situation: {Current_Situation_P1}
""" + Additional_Prompt

    return Sys_Prompt, User_Prompt

def prompt_main(ID, InValid_Action, P1, P2):
    # 0: Library, 1: Hand, 2: Battlefield, 3: Graveyard, 4: LifePoint
    P_1_1 = info_change(P1[1])
    P_1_2 = info_change(P1[2])
    P_1_3 = info_change(P1[3])
    
    P_2_1 = info_change(P2[1])
    P_2_2 = info_change(P2[2])
    P_2_3 = info_change(P2[3])
    
    P_1_0_3 = info_change(P1[0][:3])
    P_2_0_3 = info_change(P2[0][:3])
    if ID == "Player":
        Current_Situation_P1_D = [len(P1[0]), P_1_1, P_1_2, P_1_3, P1[4], len(P2[0]), len(P2[1]), P_2_2, len(P2[3]), P2[4]]
        Current_Situation_P2_D = [P_1_0_3, P_1_1, P_1_2, P_1_3, P1[4], P_2_0_3, P_2_1, P_2_2, P_2_3, P2[4]]
    elif ID == "DDA":
        Current_Situation_P1_D = [len(P2[0]), P_2_1, P_2_2, P_2_3, P2[4], len(P1[0]), len(P1[1]), P1[2], len(P1[3]), P1[4]]
        Current_Situation_P2_D = [P_2_0_3, P_2_1, P_2_2, P_2_3, P2[4], P_1_0_3, P_1_1, P_1_2, P_1_3, P1[4]]
    # Difference = Current_Situation.Difference()

    Current_Situation_P1 = f"""
The number of cards in your Library is: {Current_Situation_P1_D[0]};
Your Hand is: {Current_Situation_P1_D[1]};
Your Battlefield is: {Current_Situation_P1_D[2]};
Your Graveyard is: {Current_Situation_P1_D[3]};
Your LifePoint is: {Current_Situation_P1_D[4]};
The number of cards in your opponent's Library is: {Current_Situation_P1_D[5]};
The number of cards in your opponent's Hand is: {Current_Situation_P1_D[6]};
Your opponent Battlefield is: {Current_Situation_P1_D[7]};
The number of cards in your opponent's Graveyard is: {Current_Situation_P1_D[8]};
Your opponent LifePoint is: {Current_Situation_P1_D[9]}.
"""

    Current_Situation_P2 = f"""
Top three card in your Library: {Current_Situation_P2_D[5]};
Your Hand is: {Current_Situation_P2_D[6]};
Your Battlefield is: {Current_Situation_P2_D[7]};
Your Graveyard is: {Current_Situation_P2_D[8]};
Your LifePoint is: {Current_Situation_P2_D[9]};
Top three card in your opponent Library: {Current_Situation_P2_D[0]};
Your opponent Hand is: {Current_Situation_P2_D[1]};
Your opponent Battlefield is: {Current_Situation_P2_D[2]};
Your opponent Graveyard is: {Current_Situation_P2_D[3]};
Your opponent LifePoint is: {Current_Situation_P2_D[4]}.
"""

    if ID == "DDA":
        obj_txt = "Balance your life points with your opponent's. Aim to make the difference as close to zero as possible."
        Current_Situation_P = Current_Situation_P2
    elif ID == "Player":
        obj_txt = "Reduce your opponent's life points from 20 to 0. Do attack as possible as you can."
        Current_Situation_P = Current_Situation_P1
    else:
        return "ERROR"

    if InValid_Action == "":
        Additional_Prompt = ""
    else:
        Additional_Prompt = f"""
Warning:
{InValid_Action}
"""

    Sys_Prompt = system_prompt(ID)
    User_Prompt = f"""Based on the Current Situation, please choose one of the following actions:
Action 1: Play a card from your hand that aligns with your game objectives (this step may cost mana).
Action 2: Activate an ability of a card or cast a spell card (this step may cost mana).
Action 3: End this phase.
You need to carefully consider which action best aligns with your game objectives. Please think it step by step.
Play one card only. We will ask you if you are willing to play another card in the next time.
Objectives: {obj_txt}
If you choose Action 1, please respond in the following format: /[1.Name one card you want to play]
If you choose Action 2, please respond in the following format: /[2.Name that card (a Instant or Sorcery), your target(a card name or self or opponent), target owner(self or opponent)]
If you choose Action 3, please respond in the following format: /[3.End This Phase]
Current Situation: {Current_Situation_P}
""" + Additional_Prompt

    return Sys_Prompt, User_Prompt

def prompt_combat(ID, InValid_Action, P1, P2):
    P_1_1 = info_change(P1[1])
    P_1_2 = info_change(P1[2])
    P_1_3 = info_change(P1[3])
    
    P_2_1 = info_change(P2[1])
    P_2_2 = info_change(P2[2])
    P_2_3 = info_change(P2[3])
    
    P_1_0_3 = info_change(P1[0][:3])
    P_2_0_3 = info_change(P2[0][:3])


    if ID == "Player":
        Current_Situation_P1_D = [len(P1[0]), P_1_1, P_1_2, P_1_3, P1[4], len(P2[0]), len(P2[1]), P_2_2, len(P2[3]), P2[4]]
        Current_Situation_P2_D = [P_1_0_3, P_1_1, P_1_2, P_1_3, P1[4], P_2_0_3, P_2_1, P_2_2, P_2_3, P2[4]]
    elif ID == "DDA":
        Current_Situation_P1_D = [len(P2[0]), P_2_1, P_2_2, P_2_3, P2[4], len(P1[0]), len(P1[1]), P_1_2, len(P1[3]), P1[4]]
        Current_Situation_P2_D = [P_2_0_3, P_2_1, P_2_2, P_2_3, P2[4], P_1_0_3, P_1_1, P_1_2, P_1_3, P1[4]]
    # Difference = Current_Situation.Difference()

    Current_Situation_P1 = f"""
The number of cards in your Library is: {Current_Situation_P1_D[0]};
Your Hand is: {Current_Situation_P1_D[1]};
Your Battlefield is: {Current_Situation_P1_D[2]};
Your Graveyard is: {Current_Situation_P1_D[3]};
Your LifePoint is: {Current_Situation_P1_D[4]};
The number of cards in your opponent's Library is: {Current_Situation_P1_D[5]};
The number of cards in your opponent's Hand is: {Current_Situation_P1_D[6]};
Your opponent Battlefield is: {Current_Situation_P1_D[7]};
The number of cards in your opponent's Graveyard is: {Current_Situation_P1_D[8]};
Your opponent LifePoint is: {Current_Situation_P1_D[9]}.
"""

    Current_Situation_P2 = f"""
Top three card in your Library: {Current_Situation_P2_D[5]};
Your Hand is: {Current_Situation_P2_D[6]};
Your Battlefield is: {Current_Situation_P2_D[7]};
Your Graveyard is: {Current_Situation_P2_D[8]};
Your LifePoint is: {Current_Situation_P2_D[9]};
Top three card in your opponent Library: {Current_Situation_P2_D[0]};
Your opponent Hand is: {Current_Situation_P2_D[1]};
Your opponent Battlefield is: {Current_Situation_P2_D[2]};
Your opponent Graveyard is: {Current_Situation_P2_D[3]};
Your opponent LifePoint is: {Current_Situation_P2_D[4]}.
"""

    if ID == "DDA":
        obj_txt = "Balance your life points with your opponent's. Aim to make the difference as close to zero as possible."
        Current_Situation_P = Current_Situation_P2
    elif ID == "Player":
        obj_txt = "Reduce your opponent's life points from 20 to 0."
        Current_Situation_P = Current_Situation_P1
    else:
        return "ERROR"

    if InValid_Action == "":
        Additional_Prompt = ""
    else:
        Additional_Prompt = f"""
Warning:
{InValid_Action}
"""

    Sys_Prompt = system_prompt(ID)
    User_Prompt = f"""Based on the Current Situation, please choose one of the following actions:
Action 1: Declare One Attacker.
Action 2: Activate an ability of a card (this step may cost mana).
Action 3: End this phase.
You need to carefully consider which action best aligns with your game objectives. Please think it step by step.
Play one card only. We will ask you if you are willing to play another card in the next time.
Objectives: {obj_txt}
If you choose Action 1, please respond in the following format: /[1.Name one card you want to attack]
If you choose Action 2, please respond in the following format: /[2.Name one card (a Instant or Sorcery), your target(a card name or self or opponent), target owner(self or opponent)]
If you choose Action 3, please respond in the following format: /[3.End This Phase]
Current Situation: {Current_Situation_P}
""" + Additional_Prompt

    return Sys_Prompt, User_Prompt

def prompt_block(ID, InValid_Action, Opponent_Declared_Attackers, P1, P2):
    P_1_1 = info_change(P1[1])
    P_1_2 = info_change(P1[2])
    P_1_3 = info_change(P1[3])
    
    P_2_1 = info_change(P2[1])
    P_2_2 = info_change(P2[2])
    P_2_3 = info_change(P2[3])
    
    P_1_0_3 = info_change(P1[0][:3])
    P_2_0_3 = info_change(P2[0][:3])
    # Current_Phase_Official_Explanation, Critical_Term_Explanation  = Explain.block()
    if ID == "Player":
        Current_Situation_P1_D = [len(P1[0]), P_1_1, P_1_2, P_1_3, P1[4], len(P2[0]), len(P2[1]), P_2_2, len(P2[3]), P2[4]]
        Current_Situation_P2_D = [P_1_0_3, P_1_1, P_1_2, P_1_3, P1[4], P_2_0_3, P_2_1, P_2_2, P_2_3, P2[4]]
    elif ID == "DDA":
        Current_Situation_P1_D = [len(P2[0]), P_2_1, P_2_2, P_2_3, P2[4], len(P1[0]), len(P1[1]), P_1_2, len(P1[3]), P1[4]]
        Current_Situation_P2_D = [P_2_0_3, P_2_1, P_2_2, P_2_3, P2[4], P_1_0_3, P_1_1, P_1_2, P_1_3, P1[4]]
    # Difference = Current_Situation.Difference()

    Current_Situation_P1 = f"""
The number of cards in your Library is: {Current_Situation_P1_D[0]};
Your Hand is: {Current_Situation_P1_D[1]};
Your Battlefield is: {Current_Situation_P1_D[2]};
Your Graveyard is: {Current_Situation_P1_D[3]};
Your LifePoint is: {Current_Situation_P1_D[4]};
The number of cards in your opponent's Library is: {Current_Situation_P1_D[5]};
The number of cards in your opponent's Hand is: {Current_Situation_P1_D[6]};
Your opponent Battlefield is: {Current_Situation_P1_D[7]};
The number of cards in your opponent's Graveyard is: {Current_Situation_P1_D[8]};
Your opponent LifePoint is: {Current_Situation_P1_D[9]}.
"""

    Current_Situation_P2 = f"""
Top three card in your Library: {Current_Situation_P2_D[5]};
Your Hand is: {Current_Situation_P2_D[6]};
Your Battlefield is: {Current_Situation_P2_D[7]};
Your Graveyard is: {Current_Situation_P2_D[8]};
Your LifePoint is: {Current_Situation_P2_D[9]};
Top three card in your opponent Library: {Current_Situation_P2_D[0]};
Your opponent Hand is: {Current_Situation_P2_D[1]};
Your opponent Battlefield is: {Current_Situation_P2_D[2]};
Your opponent Graveyard is: {Current_Situation_P2_D[3]};
Your opponent LifePoint is: {Current_Situation_P2_D[4]}.
"""

    if ID == "DDA":
        obj_txt = "Balance your life points with your opponent's. Aim to make the difference as close to zero as possible."
        Current_Situation_P = Current_Situation_P2
    elif ID == "Player":
        obj_txt = "Reduce your opponent's life points from 20 to 0."
        Current_Situation_P = Current_Situation_P1
    else:
        return "ERROR"

    if InValid_Action == "":
        Additional_Prompt = ""
    else:
        Additional_Prompt = f"""
Warning:
{InValid_Action}
"""

    Sys_Prompt = system_prompt(ID)
    User_Prompt = f"""Based on the Current Situation, please choose one of the following actions:
Action 1: Declare One Blocker.
Action 2: Activate an ability of a valid card (this step may cost mana).
Action 3: End this Step.
Phase Explanation: Current_Phase_Official_Explanation
Critical Term Explanation: Critical_Term_Explanation
You need to carefully consider which action best aligns with your game objectives. Please think it step by step.
Choose one card only. We will ask you if you are willing to play another card in the next time.
Objectives: {obj_txt}
If you choose Action 1, you need to specify which card you will use to block each of your opponent's cards.: /[1.One Blocker's name,
One Attack's name]
If you choose Action 2, please respond in the following format: /[2.Name one card (a Instant or Sorcery), your target(a card name or self or opponent), target owner(self or opponent)]
If you choose Action 3, please respond in the following format: /[3.End This Phase]
Current Situation: {Current_Situation_P}
Being Attacked by: {Opponent_Declared_Attackers}
""" + Additional_Prompt

    return Sys_Prompt, User_Prompt