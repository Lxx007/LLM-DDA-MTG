import csv
import os
import copy
import random

def initial ():
    Deck, Cards = basic_information()
    Player_1, Player_2 = field_initialization()
    Player_1, Player_2 = game_initialization(Player_1, Player_2, Deck, Cards)
    return Player_1, Player_2

def basic_information():
    DeckInfo = './GPTConn/MTG/data/DeckTable.csv'
    CardInfo = "./GPTConn/MTG/data/CardsTable_tokenAdded.csv"
    Deck = []
    # Card Name, mana cost, card type, power, toughness, card description]
    Cards = []
    with open(DeckInfo, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            deck_i_info = row[2].split(",")
            Deck.append(copy.deepcopy(deck_i_info))

    with open(CardInfo, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            card_i_info = row
            Cards.append(copy.deepcopy(card_i_info))
    return Deck, Cards

def field_initialization():
    Player_1_Hand = []
    Player_1_LifePoint = 20
    Player_1_Battlefield = []
    Player_1_Library = []
    Player_1_Graveyard = []
    Player_1 = [Player_1_Library, Player_1_Hand, Player_1_Battlefield, Player_1_Graveyard, Player_1_LifePoint]
    
    Player_2_Hand = []
    Player_2_LifePoint = 20
    Player_2_Battlefield = []
    Player_2_Library = []
    Player_2_Graveyard = []
    Player_2 = [Player_2_Library, Player_2_Hand, Player_2_Battlefield, Player_2_Graveyard, Player_2_LifePoint]

    return Player_1, Player_2

def game_initialization(Player_1, Player_2, Deck, Cards):
    shuffle_deck = random.sample(Deck[0], len(Deck[0]))
    CardsDetail = {item[0]: item[1:] for item in Cards}
    Deck_w_info = []
    for i in shuffle_deck:
        values = CardsDetail.get(i, "Key not found")
        if values == "Key not found":
            return [],[]
        else:
            Deck_w_info.append(copy.deepcopy([i, values]))
    Player_1[0] = copy.deepcopy(Deck_w_info)

    shuffle_deck = random.sample(Deck[0], len(Deck[0]))
    Deck_w_info = []
    for i in shuffle_deck:
        values = CardsDetail.get(i, "Key not found")
        if values == "Key not found":
            return [],[]
        else:
            Deck_w_info.append(copy.deepcopy([i, values]))
    Player_2[0] = copy.deepcopy(Deck_w_info)
    return Player_1, Player_2

def situation_update(player_id, field_selection, target_ID, go_to, destination_position, enhance_number, enhance_position, Player):
    # 0: Library, 1: Hand, 2: Battlefield, 3: Graveyard, 4: LifePoint
    T_Player = copy.deepcopy(Player)
    Target_Card = copy.deepcopy(T_Player[field_selection][target_ID])
    del T_Player[field_selection][target_ID]
    if enhance_position != -1:
        Target_Card[enhance_position] = copy.deepcopy(Target_Card[enhance_position] + enhance_number)
    if destination_position == -1:
        T_Player[go_to].insert(len(T_Player[go_to]), Target_Card)
    return T_Player


def draw (Player_ID, Player_Status):
    if Player_ID == "Player":
        ID = 1
    elif Player_ID == "DDA":
        ID = 2
    else:
        ID = -1
    Player = situation_update(ID, 0, 0, 1, -1, 0, -1, Player_Status)
    return Player

def Decision (Player_1, Player_2):
    if (Player_1[4] <= 0) or (Player_2[4] <= 0):
        return False
    else:
        return True