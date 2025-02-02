import MTG_Game_Process as Game
import Current_Situation as Status
import Cards as Cards
import Current_Situation
import re
import copy
import random

def ref_setup(ID, Action, P1, P2, count):
    response = False
    Invalid = ""

    if ID == "DDA":
        Hand = copy.deepcopy(P2[1])
        Deck = copy.deepcopy(P2[0])
        item = Action[0]
        item = item.replace("*", "")
        match = re.search(r'/Cards:\s*(.*)', item)
        if match:
            card_names = match.group(1).split(',')
        else:
            Invalid = "Action does not contain a valid card list. Please use the format as /Cards: CardName1, CardName2, ..."
            return response, Invalid, P1, P2, count
        
        Deck.extend(Hand)
        Deck_Dict = {item[0]: item[1] for item in Deck}
        card_names = [card.strip() for card in card_names]
        Card_D = [[key, Deck_Dict[key]] for key in card_names if key in Deck_Dict]
        missing_cards = [card for card in Card_D if card not in Deck]  
        if missing_cards:
            Invalid = f"The following cards are not in the deck: {', '.join(missing_cards)}."
            return response, Invalid, P1, P2, count
        
        Hand.clear()
        for card in Card_D:
            Hand.append(card)   
            Deck.remove(card)
        
        P2[0] = random.sample(Deck, len(Deck))
        P2[1] = Hand
        response = True
        return response, Invalid, P1, P2, count


    elif ID == "Player":
        item = Action[0]
        item = item.replace("*", "")
        match = re.search(r'/Your Answer: (.+)', item)
        if match:
            answer = match.group(1)
        else:
            Invalid = "Action does not contain a valid answer. Please following the format /Your Answer : YES or NO."
            return response, Invalid,P1,P2,count

        answer = match.group(1).upper()
        if 'YES' in answer:
            answer = 'YES'
        elif 'NO' in answer:
            answer = 'NO'
        else:
            answer = answer
        Hand = copy.deepcopy(P1[1])
        Deck = copy.deepcopy(P1[0])
        if answer == "YES":  
            Deck.extend(Hand)
            Hand.clear()
            P1[1] = Hand
            P1[0] = random.sample(Deck, len(Deck))
            for i in range (7):
                P1 = Status.draw("Player", P1)
            
            count = count + 1
            if count == 6:
                Invalid = f"""You have MULLIGANED {count} times previously. You have no MULLIGAN chance.
You need to discard {count} cards.Please think it step by step. 
Please use the following format for cards will be discarded. /Cards: CardName1, CardName2, ..."""
            elif count >= 7:
                Invalid = f"""You have MULLIGANED 6 times previously. You have no MULLIGAN chance.
You must choose NO MULLIGAN.
You need to discard 6 cards. Please think it step by step. 
Please use the following format for cards will be discarded. /Cards: CardName1, CardName2, ..."""
            else:
                Invalid = f"""You have MULLIGANED {count} time(s) previously. 
Therefore, if you do not want to MULLIGAN this time. You need to discard {count} card(s). Please think it step by step. 
Please use the following format for card(s) will be discarded. /Cards: CardName1, CardName2, ..."""
            return response, Invalid,P1,P2,count
        elif answer == "NO":
            response = True
            if(count > 0):
                item = Action[0]
                item = item.replace("*", "")
                match = re.search(r'/Cards:(.+)', item)
                if match:
                    selected_hand = match.group(0)  
                else:
                    Invalid = "Action does not contain a valid answer. Please name cards will be discarded with the following format /Cards:CardName1, CardName2, ..."
                    return response, Invalid, P1, P2, count
                card_names = [card.strip() for card in match.group(1).split(",")]
                Deck_Dict = {item[0]: item[1] for item in Deck}
                Card_D = [item for item in Hand if item[0] in card_names]
                if Card_D == []:
                    Invalid = f"The following cards are not in the deck: {', '.join(missing_cards)}."
                    return response, Invalid, P1, P2, count
                else:
                    for card in Card_D:
                        Hand.remove(card)
                        Deck.append(card) 
                    P1[0] = random.sample(Deck, len(Deck))
                    P1[1] = Hand
            return response, Invalid, P1, P2, count
        else:
            Invalid = "Action does not contain a valid answer. Please following the format /Your Answer : YES or NO."
            return response, Invalid, P1, P2, count


def ref_combat(ID, Action, Active_P, Pending_P):
    
    P = copy.deepcopy(Active_P)
    response = False
    Invalid = ""
    # Search for the pattern in the input string 
    match = re.findall(r'/\[(.*?)\]', Action)
   
    if match: 
        if len(match) >= 2:
            Invalid = f"Do not play more than one card in your answer"
            return response, Invalid, P, Pending_P, []
        Player_Answer = match[0].split(".")
        Coice = Player_Answer[0]
        Card_Info = Player_Answer[1]
    else: 
        Invalid = f"Output formate is incorrect, please retry"
        return response, Invalid, P, Pending_P, []
    Attack = []

    if Coice == "1":
        if next(((index, item) for index, item in enumerate(P[2]) if item[0] == Card_Info), None) == None:
            Invalid = f"Your picked card does not exists in your hand, which is {Card_Info[0]}"
            return response, Invalid, P, Pending_P, Attack
        else:
            Card_index, Card_Deatil = next(((index, item) for index, item in enumerate(P[2]) if item[0] == Card_Info), None)
            if "Creature" in Card_Deatil[1][1]:
                if Card_Deatil[1][5] == 1:
                    Invalid = f"Your picked card is tapped, which is {Card_Info[0]}"
                else:
                    Attack.append(copy.deepcopy([Card_index, Card_Deatil]))
            else:
                Invalid = f"Your picked card is not a creature, which is {Card_Info[0]}"
        return response, Invalid, P, Pending_P, Attack
    elif Coice == "2":
        Card_Info = Card_Info.split(",")
        Used_Card = Card_Info[0]
        Target_card = Card_Info[1]
        Target_Controllor = Card_Info[2]
        if next(((index, item) for index, item in enumerate(P[1]) if item[0] == Used_Card), None) == None:
            if next(((index, item) for index, item in enumerate(P[2]) if item[0] == Used_Card), None) == None:
                Invalid = f"Your picked card does not exists in your hand or battlefield, which is {Used_Card}"
                return response, Invalid, P, Pending_P, Attack
        else:
            Card_index, Card_Deatil = next(((index, item) for index, item in enumerate(P[1]) if item[0] == Used_Card), None)
            # 手牌
            if next(((index, item) for index, item in enumerate(P[1]) if item[0] == Used_Card), None) != None:
                CanbePlayed, Used_Card_Index = Card_mana_True(P, Card_index, Card_Deatil)
                if CanbePlayed == False:
                    Invalid = f"Not enough mana to play '{Card_Deatil}'."
                else:
                    for i_b in Used_Card_Index:
                        P[2][i_b][1][5] = copy.deepcopy(1)
                    print("Under construction !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")       
                P = Current_Situation.situation_update(ID, 1, Card_index, 3, -1, 0, -1, P)
            # 场上的怪    
            elif next(((index, item) for index, item in enumerate(P[2]) if item[0] == Used_Card), None) != None:
                print("Not Implement")
        return response, Invalid, P, Pending_P, Attack
    elif Coice == "3":
        print("Turn ended.")
        response = True
        return response, Invalid, P, Pending_P, Attack
    
 
def Card_mana_True (P, Card_index, Card_Detail):
    Battlefield_P = P[2]
    Hand_P = P[1]
    Cost_Hand = [item[1][0] for item in Hand_P]
    Type_Hand = [item[1][1] for item in Hand_P]
    Type_Battlefield = [item[1][1] for item in Battlefield_P]
    Active_Battlefield = [item[1][5] for item in Battlefield_P]
    CardInfo_Battlefield = [item[1][4] for item in Battlefield_P]
    # mana. G, W, U, B, R, N
    Active_Land_Index = []
    Potential_mana = [0, 0, 0, 0, 0, 0]
    for i_act_land in range(len(P[2])):
        if (Type_Battlefield[i_act_land]== "Land") & ((Active_Battlefield[i_act_land]== "0") or (Active_Battlefield[i_act_land]== 0)):
            Active_Land_Index.append(copy.deepcopy(i_act_land))
    
    Active_Land_Type = []
    Max_mana_poss = [0, 0, 0, 0, 0, 0]
    for mi in Active_Land_Index:
        current_mana_type = []
        mana_T = CardInfo_Battlefield[mi]
        if "Add G" in mana_T:
            current_mana_type.append(copy.deepcopy("G"))
            Max_mana_poss[0] = Max_mana_poss[0] + 1
            Max_mana_poss[5] = Max_mana_poss[5] + 1
        if "Add W" in mana_T:
            current_mana_type.append(copy.deepcopy("W"))
            Max_mana_poss[1] = Max_mana_poss[1] + 1
            Max_mana_poss[5] = Max_mana_poss[5] + 1
        if "Add U" in mana_T:
            current_mana_type.append(copy.deepcopy("U"))
            Max_mana_poss[2] = Max_mana_poss[2] + 1
            Max_mana_poss[5] = Max_mana_poss[5] + 1
        if "Add B" in mana_T:
            current_mana_type.append(copy.deepcopy("B"))
            Max_mana_poss[3] = Max_mana_poss[3] + 1
            Max_mana_poss[5] = Max_mana_poss[5] + 1
        if "Add R" in mana_T:
            current_mana_type.append(copy.deepcopy("R"))
            Max_mana_poss[4] = Max_mana_poss[4] + 1
            Max_mana_poss[5] = Max_mana_poss[5] + 1
        if "Add 1" in mana_T:
            current_mana_type.append(copy.deepcopy("A"))
            Max_mana_poss[5] = Max_mana_poss[5] + 1
        Active_Land_Type.append(copy.deepcopy(current_mana_type))
            
                  
    needed_mana = [0, 0, 0, 0, 0, 0]
    # mana. G, W, U, B, R, N
    parts = Card_Detail[1][0].split('&')
    if parts[0].isdigit():
        mana_cost = [int(parts[0]), parts[1:]]  
    else:
        mana_cost = [0, parts] 
        
    for n_m_i in mana_cost[1]:
        if n_m_i == "G":
            needed_mana[0] = needed_mana[0] + 1
        elif n_m_i == "W":
            needed_mana[1] = needed_mana[1] + 1
        elif n_m_i == "U":
            needed_mana[2] = needed_mana[2] + 1
        elif n_m_i == "B":
            needed_mana[3] = needed_mana[3] + 1
        elif n_m_i == "R":
            needed_mana[4] = needed_mana[4] + 1
        elif str(n_m_i).isdigit():
            needed_mana[5] = needed_mana[5] + int(n_m_i)
    
    needed_mana[5] = needed_mana[5] + mana_cost[0]
    Final_picking = []      
    Excluded_index = set({})
    for z_i in range (len(needed_mana)):
        if needed_mana[z_i] == 0:
            Excluded_index.add(copy.deepcopy(z_i))
    non_zero_count = len([x for x in needed_mana if x != 0])
    for i in range (non_zero_count):
        Remain_mana = [a - b for a, b in zip(Max_mana_poss, needed_mana)]
        negative_count = len([x for x in Remain_mana if x < 0])
        if negative_count > 0:
            return False, []
        else:
            min_index = min(
                (i for i in range(len(Remain_mana)) if i not in Excluded_index),  
                key=lambda x: Remain_mana[x] 
            )  
            picked_value = []
            if min_index == 0:
                k_w = "G"
                Max_mana_poss[5] = Max_mana_poss[5] - needed_mana[min_index]
                Max_mana_poss[0] = Max_mana_poss[0] - needed_mana[min_index]
            elif min_index == 1:
                k_w = "W"
                Max_mana_poss[5] = Max_mana_poss[5] - needed_mana[min_index]
                Max_mana_poss[1] = Max_mana_poss[1] - needed_mana[min_index]
            elif min_index == 2:
                k_w = "U"
                Max_mana_poss[5] = Max_mana_poss[5] - needed_mana[min_index]
                Max_mana_poss[2] = Max_mana_poss[2] - needed_mana[min_index]
            elif min_index == 3:
                k_w = "B"
                Max_mana_poss[5] = Max_mana_poss[5] - needed_mana[min_index]
                Max_mana_poss[3] = Max_mana_poss[3] - needed_mana[min_index]
            elif min_index == 4:
                k_w = "R"
                Max_mana_poss[5] = Max_mana_poss[5] - needed_mana[min_index]
                Max_mana_poss[4] = Max_mana_poss[4] - needed_mana[min_index]
            elif min_index == 5:
                k_w = "A"
                Max_mana_poss[5] = Max_mana_poss[5] - needed_mana[min_index]
            for i in range(needed_mana[min_index]):
                if k_w == "A":
                    try:
                        land_index = random.choice(Active_Land_Index)
                    except:
                        return False, []
                    picked_value.append(copy.deepcopy(land_index))
                    picked_color = Active_Land_Type[Active_Land_Index.index(land_index)]
                    for cc in picked_color:
                        if cc == "G":
                            Max_mana_poss[0] = Max_mana_poss[0] - 1
                            Remain_mana[0] = Remain_mana[0] - 1
                        elif cc == "W":
                            Max_mana_poss[1] = Max_mana_poss[1] - 1
                            Remain_mana[1] = Remain_mana[1] - 1
                        elif cc == "U":
                            Max_mana_poss[2] = Max_mana_poss[2] - 1
                            Remain_mana[2] = Remain_mana[2] - 1
                        elif cc == "B":
                            Max_mana_poss[3] = Max_mana_poss[3] - 1
                            Remain_mana[3] = Remain_mana[3] - 1
                        elif cc == "R":
                            Max_mana_poss[4] = Max_mana_poss[4] - 1
                            Remain_mana[4] = Remain_mana[4] - 1    
                else:
                    valid_indices = [i for i, val in enumerate(Active_Land_Type) if k_w in val]
                    valid_values = [Active_Land_Index[i] for i in valid_indices]
                    land_index = copy.deepcopy(random.choice(valid_values) if valid_values else None)
                    picked_value.append(land_index)
                del Active_Land_Type[Active_Land_Index.index(land_index)]
                Active_Land_Index.remove(land_index)
            # picked_value = random.sample(indices, needed_mana[min_index])
            Excluded_index.add(copy.deepcopy(min_index))
            needed_mana[min_index] = 0
            for i in picked_value:
                Final_picking.append(copy.deepcopy(i))
    return True, Final_picking
    
    
def Main_Selection(ID, answer, Active_P, Pending_P, Land_count):
    # 0: Library, 1: Hand, 2: Battlefield, 3: Graveyard, 4: LifePoint

    P = copy.deepcopy(Active_P)
    response = False
    Invalid = ""
    # Search for the pattern in the input string 
    match = re.findall(r'/\[(.*?)\]', answer)
   
    if match: 
        if len(match) >= 2:
            Invalid = f"Do not play more than one card in your answer"
            return response, Invalid, P, Pending_P, Land_count
        Player_Answer = match[0].split(".")
        Coice = Player_Answer[0]
        Card_Info = Player_Answer[1]
        print ("LLM Choice ------------------------------------------------------")
        print (Coice)
        print (Card_Info)
    else: 
        Invalid = f"Output formate is incorrect, please retry"
        return response, Invalid, P, Pending_P, Land_count
    if Coice == "1":
        if next(((index, item) for index, item in enumerate(P[1]) if item[0] == Card_Info), None) == None:
            Invalid = f"Your picked card does not exists in your hand, which is {Card_Info}"
            return response, Invalid, P, Pending_P, Land_count
        else:
            Card_index, Card_Deatil = next(((index, item) for index, item in enumerate(P[1]) if item[0] == Card_Info), None)
            if Card_Deatil[1][1] == "Land" and Land_count == 0:
                # situation_update(player_id, field_selection, target_ID, go_to, destination_position, enhance_number, enhance_position, Player):
                # 0: Library, 1: Hand, 2: Battlefield, 3: Graveyard, 4: LifePoint
                P = Current_Situation.situation_update(ID, 1, Card_index, 2, -1, 0, -1, P)
                Land_count += 1
                return response, Invalid, P, Pending_P, Land_count
            elif Card_Deatil[1][1] != "Land":
                CanbePlayed, Used_Card_Index = Card_mana_True(P, Card_index, Card_Deatil)
                if CanbePlayed:
                    for i_b in Used_Card_Index:
                        P[2][i_b][1][5] = copy.deepcopy(1)
                    P = Current_Situation.situation_update(ID, 1, Card_index, 2, -1, 0, -1, P)
                    P[2][-1][1][5] = copy.deepcopy(1)
                    return response, Invalid, P, Pending_P, Land_count
                else:
                    Invalid = f"Not enough mana to play '{Card_Deatil[0]}'."
                    return response, Invalid, P, Pending_P, Land_count
            else:
                Invalid = f"You have played Land this turn."
                return response, Invalid, P, Pending_P, Land_count

    elif Coice == "2":
        Card_Info = Card_Info.split(",")
        Used_Card = Card_Info[0]
        Target_card = Card_Info[1]
        Target_Controllor = Card_Info[2]
        if next(((index, item) for index, item in enumerate(P[1]) if item[0] == Used_Card), None) == None:
            if next(((index, item) for index, item in enumerate(P[2]) if item[0] == Used_Card), None) == None:
                Invalid = f"Your picked card does not exists in your hand or battlefield, which is {Used_Card}"
                return response, Invalid, P, Pending_P, Land_count
        else:
            Card_index, Card_Deatil = next(((index, item) for index, item in enumerate(P[1]) if item[0] == Used_Card), None)
            # 手牌
            if next(((index, item) for index, item in enumerate(P[1]) if item[0] == Used_Card), None) != None:
                CanbePlayed, Used_Card_Index = Card_mana_True(P, Card_index, Card_Deatil)
                if CanbePlayed == False:
                    Invalid = f"Not enough mana to play '{Card_Deatil[0]}'."
                else:
                    for i_b in Used_Card_Index:
                        P[2][i_b][1][5] = copy.deepcopy(1)
                    print("Under construction !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")       
                P = Current_Situation.situation_update(ID, 1, Card_index, 3, -1, 0, -1, P)
            # 场上的怪    
            elif next(((index, item) for index, item in enumerate(P[2]) if item[0] == Used_Card), None) != None:
                print("Not Implement")
        return response, Invalid, P, Pending_P, Land_count

    elif Coice == "3":
        # print("Turn ended.")
        response = True
        return response, Invalid, P, Pending_P, Land_count
    
def ref_block(ID, Active_P, Pending_P, Action, Attackers):
    P = copy.deepcopy(Pending_P)
    response = False
    Invalid = ""
    # Search for the pattern in the input string 
    match = re.findall(r'/\[(.*?)\]', Action)
    Blockers = []
    if match: 
        if len(match) >= 2:
            Invalid = f"Do not play more than one card in your answer"
            return Attackers, Blockers, -1, Invalid, Action, response
        Player_Answer = match[0].split(".")
        Coice = Player_Answer[0]
        Card_Info = Player_Answer[1].split(",")
        if len(Card_Info) == 1:
            Card_Info = Card_Info[0]
        else:
            Block_info = Card_Info[0]
            Attack_info = Card_Info[1]
        print ("LLM Choice ------------------------------------------------------")
        print (Coice)
        print (Card_Info)

    else: 
        Invalid = f"Output formate is incorrect, please retry"
        return Attackers, Blockers, -1, Invalid, Action, response
    
    if Coice == "1":
        for ai in Attackers:
            if next(((index, item) for index, item in enumerate(P[2]) if item[0] == Block_info), None) == None:
                Invalid = f"Your picked card does not exists in your hand or battlefield, which is {Used_Card}"
                return Attackers, Blockers, -1, Invalid, Action, response
            else:
                Card_index, Card_Deatil = next(((index, item) for index, item in enumerate(P[2]) if item[0] == Block_info), None)
                if int(Card_Deatil[1][5]) == 0:
                    Blockers = [Attackers[0], Card_Deatil]
                    Invalid = f"You have already asked {Block_info} to block {Attack_info}"
                else:
                    Invalid = f"You cannot declear {Card_Deatil[0]} as blocker, since its Tapped"
                    return Attackers, Blockers, -1, Invalid, Action, response
        return Attackers, Blockers, Card_index, Invalid, Action, response
    elif Coice == "2":
        # Card_Info = Card_Info.split(",")
        Used_Card = Card_Info[0]
        Target_card = Card_Info[1]
        Target_Controllor = Card_Info[2]
        if next(((index, item) for index, item in enumerate(P[1]) if item[0] == Used_Card), None) == None:
            if next(((index, item) for index, item in enumerate(P[2]) if item[0] == Used_Card), None) == None:
                Invalid = f"Your picked card does not exists in your hand or battlefield, which is {Used_Card}"
                return Attackers, Blockers, -1, Invalid, Action, response
        else:
            Card_index, Card_Deatil = next(((index, item) for index, item in enumerate(P[1]) if item[0] == Used_Card), None)
            if ("Instant" not in Card_Deatil[1][1]) or ("Sorcery" not in Card_Deatil[1][1]):
                Invalid = f"'{Card_Deatil[0]}' is not a Instant or Sorcery."
            # 手牌
            if next(((index, item) for index, item in enumerate(P[1]) if item[0] == Used_Card), None) != None:
                CanbePlayed, Used_Card_Index = Card_mana_True(P, Card_index, Card_Deatil)
                if CanbePlayed == False:
                    Invalid = f"Not enough mana to play '{Card_Deatil[0]}'."
                else:
                    for i_b in Used_Card_Index:
                        P[2][i_b][1][5] = copy.deepcopy(1)
                    print("Under construction !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")       
                P = Current_Situation.situation_update(ID, 1, Card_index, 3, -1, 0, -1, P)
            # 场上的怪    
            elif next(((index, item) for index, item in enumerate(P[2]) if item[0] == Used_Card), None) != None:
                print("Not Implement")
        return Attackers, Blockers, -1, Invalid, Action, response

    elif Coice == "3":
        # print("Turn ended.")
        response = True
        return Attackers, Blockers, -1, Invalid, Action, response
    

def CombatSummary(Attacker, Blocker, Block_index, Active_P, Pending_P):
    no_blocked_damage = 0
    for i in Attacker:
        Block_detail = next((item[1] for item in Blocker if item[0] == i[0]), None)
        if Block_detail == None:
            no_blocked_damage = no_blocked_damage + int(i[1][1][2])
        else:
            Attack_power = int(i[1][1][2])
            Attack_toughness = int(i[1][1][3])
            Block_power = int(Block_detail[1][2])
            Block_toughness = int(Block_detail[1][3])
            i[1][1][3] = copy.deepcopy(int(i[1][1][3] - Block_power))
            Block_detail[1][3] = copy.deepcopy(int(Block_detail[1][3] - Attack_power))
    Active_Break = []
    for i in Attacker:
        if int(i[1][1][3]) <= 0:
            Active_Break.append(copy.deepcopy(i[0]))
    Pending_Break = []
    for i in range (len(Blocker)):
        if int(Blocker[i][1][1][3]) <= 0:
            Pending_Break.append(Block_index[i])
            
    for i in Active_Break:
        Active_P = Current_Situation.situation_update("Act", 2, i, 3, -1, 0, -1, Active_P)
    for i in Pending_Break:
        Pending_P = Current_Situation.situation_update("Act", 2, i, 3, -1, 0, -1, Pending_P)
        
    Pending_P[4] = copy.deepcopy(Pending_P[4] - no_blocked_damage)
    
    return Active_P, Pending_P 
