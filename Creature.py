from Card import Card
import random

class Creature:
    '''
    Unique creations that are the basis for creating cards
    '''
    list_creatures = []
    def __init__(self):
        '''
        Reading all creations from a file
        '''
        try:
            with open('Creature_data', 'r') as file:
                creature_lines = file.readlines()
                for line in creature_lines:
                    tab = line.split('$')
                    Creature.list_creatures.append(
                        Card(tab[0], int(tab[1]), int(tab[2]), int(tab[3]), tab[4], tab[5], tab[6].strip()))
        except FileNotFoundError:
            print("FileNotFoundError")

    def create_deck_for_battle(self):
        '''
        Create a unique deck of cards from existing creatures
        :return: unique deck of cards for the player
        '''
        amount_hero = [6, 5, 4, 4, 3, 2, 2, 2, 1, 1]
        new_deck = []

        for i, value in enumerate(amount_hero):
            creature_deck_temp = [card for card in Creature.list_creatures if card.price == (i+1)]
            for q in range(0, value):
                card_temp = random.choice(creature_deck_temp)
                if str(card_temp.name).split(" ")[0].strip() == "T":
                    card_temp.name = card_temp.name[2:]
                new_deck.append(Card(card_temp.name, card_temp.health, card_temp.damage, card_temp.price, card_temp.ability_description, card_temp.element, card_temp.style))
        random.shuffle(new_deck)
        new_deck.insert(0, Card('Mana',0,0,0,'Increase your mana for 1','Spell','Spell'))
        return new_deck
