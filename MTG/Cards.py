import csv

class Card:
    def __init__(self, cardname, mana, cardtype, power, toughness, description):
        self.cardname = cardname
        self.mana = mana
        self.cardtype = cardtype
        self.power = int(power) if power.isdigit() else 0
        self.toughness = int(toughness) if toughness.isdigit() else 0
        self.description = description

    def __str__(self):
        return (f"{self.cardname} - Mana Cost: {self.mana}, Type: {self.cardtype}, "
                f"Power: {self.power}, Toughness: {self.toughness}, Description: {self.description}")

    def change_power(self, amount):
        self.power += amount
        print(f"{self.cardname}'s Power changed to {self.power}.")

    def change_toughness(self, amount):
        self.toughness += amount
        print(f"{self.cardname}'s Toughness changed to {self.toughness}.")

def read_cards_from_csv(file_path):
    cards = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            card = Card(
                cardname=row['Card Name'],
                mana=row['mana cost'],
                cardtype=row['card type'],
                power=row['power'],
                toughness=row['toughness'],
                description=row['card description']
            )
            cards.append(card)
    return cards

def find_card_by_name(cards, name):
    for card in cards:
        if card.cardname.lower() == name.lower():
            return card
    return None

def parse_mana_cost(mana_cost):
    total_mana = 0

    for char in mana_cost:
        if char.isdigit():
            total_mana += int(char)  
        elif char.isalpha():
            total_mana += 1  

    return total_mana

file_path = r'./GPTConn/MTG/data/CardsTable.csv'
cards = read_cards_from_csv(file_path)

def referee_modify_card(cards, card_name, power_change, toughness_change):
    card = find_card_by_name(cards, card_name)
    if card:
        print(f"Found card: {card}")
        card.change_power(power_change)
        card.change_toughness(toughness_change)
    else:
        print(f"Card '{card_name}' not found.")