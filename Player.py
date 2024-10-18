import random


class Player:
    '''
    A player who takes part in a game
    '''
    def __init__(self, name, full_cards):
        self.maximum_mana = 10
        self.name = name
        self.hp = 30
        self.mana = 1
        self.all_current_mana = self.mana
        self.full_cards = full_cards
        self.cards_in_hands = []
        self.cards_in_battle = []
        for i in range(0,5):
            self.add_card_to_cards_in_hands(self.full_cards[0])
            self.full_cards.remove(self.full_cards[0])

    def add_card_to_cards_in_hands(self, card):
        '''
        Adds card to the player's hand
        :param card: card to add
        '''
        self.cards_in_hands.append(card)

    def add_card_to_cards_in_battle(self, card):
        '''
        Adds a card to a player on the battlefield
        :param card: card to add
        '''
        self.cards_in_battle.append(card)

    def add_card_to_cards_in_battle_from_hands(self, card):
        '''
        Move a card from your hand to the battlefield
        :param card: card to move
        '''
        if card in self.cards_in_hands:
            self.cards_in_battle.append(card)
            self.cards_in_hands.remove(card)


class AIPlayer(Player):
    '''
    A bot that imitates a player
    '''
    def __init__(self, name, full_cards, difficulty):
        super().__init__(name, full_cards)
        self.difficulty = difficulty

    def generate_list_to_battle(self, enemy):
        '''
        Selecting which cards will be placed from the player’s hand onto the playing field
        :param enemy: the player who is opposing this bot
        :return:
        '''
        if self.mana == 1:
            self.mana += 1
        generated_list_to_battle = []
        not_enough_mana = []
        match self.difficulty:
            case "Beginner":
                if self.cards_in_hands[0].name == "Mana":
                    chosen_card = self.cards_in_hands[0]
                    self.cards_in_hands.remove(chosen_card)
                    generated_list_to_battle.append(chosen_card)
                while self.cards_in_hands:
                    chosen_card = random.choice(self.cards_in_hands)
                    self.cards_in_hands.remove(chosen_card)
                    if self.mana >= chosen_card.price:
                        self.mana -= chosen_card.price
                        generated_list_to_battle.append(chosen_card)
                    else:
                        not_enough_mana.append(chosen_card)
                self.cards_in_hands.extend(not_enough_mana)
                self.cards_in_hands.extend(generated_list_to_battle)
                self.mana = self.all_current_mana
            case "Advanced":
                for card in self.cards_in_hands:
                    card.density = (card.damage + card.health/2)/(card.price if card.price > 0 else 1)
                    if card.taunt:
                        card.density += 1
                    if "Summon".lower() in str(card.ability_description).lower():
                        card.density += 0.75
                    if card.style == "SpellAttacker":
                        if enemy.cards_in_battle:
                            card.density = 4
                        else:
                            card.density = -4
                    if card.style == "SpellHelper":
                        if enemy.cards_in_battle and len(self.cards_in_battle)==0:
                            card.density = -4
                        else:
                            card.density = + 2.25
                    if card.name == "Mana":
                        card.density = 100
                self.cards_in_hands = sorted(self.cards_in_hands, key=lambda card: card.density, reverse=True)
                for card in self.cards_in_hands:
                    if self.mana >= card.price:
                        self.mana -= card.price
                        generated_list_to_battle.append(card)
        return generated_list_to_battle