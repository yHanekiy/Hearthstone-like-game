import random
import tkinter
from tkinter import simpledialog
import Player
from Hearthstone_gui import GameMoment

class Card:
    '''
    A combat unit for a game based on some kind of creature
    '''
    def __init__(self, name, health, damage, price, ability_description, element, style):
        self.name = name
        self.health = health
        self.damage = damage
        self.price = price
        self.element = element
        self.ability_description = ability_description

        self.card_frame = None
        self.style = style

        self.sleep = True
        self.taunt = True if "Taunt" in ability_description else False
        if self.taunt:
            self.name = "T "+self.name
        self.already_attacked = False
        self.chosen_circle = None
        self.density = 0

    def activate_ability(self, player1, player2, game_moment, this_card):
        '''
        Activates a card's ability
        :param player1: player number 1 in the game
        :param player2: player number 2 in the game
        :param game_moment: index of the moment of play, which determines whose card it is
        :param this_card: card whose ability needs to be activated
        :return:
        '''
        match str(self.name).strip():
            case "Mana":
                if game_moment == GameMoment.Player1Round:
                    player1.mana += 1
                else:
                    player2.mana += 1
            case "F.Spirit":
                player1.hp -= 2
                player2.hp -= 2
            case "Silvia":
                if game_moment == GameMoment.Player1Round:
                    player1.add_card_to_cards_in_battle(Card("Minion",1,1,1,"Ordinary unit","Nothing","Warrior"))
                else:
                    player2.add_card_to_cards_in_battle(Card("Minion",1,1,1,"Ordinary unit","Nothing","Warrior"))
            case "Anchutka":
                if game_moment == GameMoment.Player1Round:
                    player1.maximum_mana = 11
                else:
                    player2.maximum_mana = 11
            case "Health":
                if game_moment == GameMoment.Player1Round:
                    player1.hp += 5
                else:
                    player2.hp += 5
            case "Holy Light":
                if game_moment == GameMoment.Player1Round:
                    for enemy in player2.cards_in_battle:
                        enemy.health -= 2
                else:
                    for enemy in player1.cards_in_battle:
                        enemy.health -= 2
            case "Demon":
                if game_moment == GameMoment.Player1Round:
                    player1.hp -= this_card.damage
                else:
                    player2.hp -= this_card.damage
            case "Death":
                try:
                    if game_moment == GameMoment.Player1Round:
                        user_input = tkinter.simpledialog.askstring("Attack creature",
                                                                    "Write a index of creature you wanna attack")
                        answer = user_input.split(' ')[0]
                        if int(answer) <= len(player2.cards_in_battle) or int(answer) > 0:
                            player2.cards_in_battle[int(answer)-1].health -= 6
                        else:
                            return False
                    else:
                        if isinstance(player2, Player.AIPlayer):
                            answer = random.randint(0, len(player1.cards_in_battle))
                        else:
                            user_input = tkinter.simpledialog.askstring("Attack creature",
                                                                        "Write a index of creature you wanna attack")
                            answer = user_input.split(' ')[0]
                        if int(answer) <= len(player1.cards_in_battle) or int(answer) > 0:
                            player1.cards_in_battle[int(answer)-1].health -= 6
                        else:
                            return False

                except Exception:
                    return False
            case "T Big frog":
                pass
            case "Elemental":
                if game_moment == GameMoment.Player1Round:
                    player1.add_card_to_cards_in_battle(Card("Minion", 3, 3, 3, "Ordinary unit", "Nothing", "Warrior"))
                else:
                    player2.add_card_to_cards_in_battle(Card("Minion", 3, 3, 3, "Ordinary unit", "Nothing", "Warrior"))
            case "Chaos":
                if game_moment == GameMoment.Player1Round:
                    player1.add_card_to_cards_in_battle(Card("Minion", 1, 1, 1, "Ordinary unit", "Nothing", "Warrior"))
                    player1.add_card_to_cards_in_battle(Card("Minion", 1, 1, 1, "Ordinary unit", "Nothing", "Warrior"))
                else:
                    player2.add_card_to_cards_in_battle(Card("Minion", 1, 1, 1, "Ordinary unit", "Nothing", "Warrior"))
                    player2.add_card_to_cards_in_battle(Card("Minion", 1, 1, 1, "Ordinary unit", "Nothing", "Warrior"))
            case "Ogr":
                pass
            case "Fogsnout":
                if game_moment == GameMoment.Player1Round:
                    player1.add_card_to_cards_in_battle(Card("Minion", 1, 1, 1, "Taunt", "Taunt", "Warrior"))
                    player1.add_card_to_cards_in_battle(Card("Minion", 1, 1, 1, "Taunt", "Taunt", "Warrior"))
                else:
                    player2.add_card_to_cards_in_battle(Card("Minion", 1, 1, 1, "Taunt", "Taunt", "Warrior"))
                    player2.add_card_to_cards_in_battle(Card("Minion", 1, 1, 1, "Taunt", "Taunt", "Warrior"))
            case "Ancient":
                if game_moment == GameMoment.Player1Round:
                    player1.hp += 7
                else:
                    player2.hp += 7
            case "Wish":
                if game_moment == GameMoment.Player1Round:
                    if len(player1.cards_in_battle) == 0 and len(player1.cards_in_hands) == 0:
                        return False
                    for card in player1.cards_in_battle:
                        card.health += 3
                        card.damage += 2
                    for card in player1.cards_in_hands:
                        card.health += 3
                        card.damage += 2
                else:
                    if len(player2.cards_in_battle) == 0 and len(player2.cards_in_hands) == 0:
                        return False
                    for card in player2.cards_in_battle:
                        card.health += 3
                        card.damage += 2
                    for card in player2.cards_in_hands:
                        card.health += 3
                        card.damage += 2
            case "Dragon":
                if game_moment == GameMoment.Player1Round:
                    for card in player2.cards_in_battle:
                        if this_card.health > 0:
                            card.health -= this_card.damage
                            this_card.health -= card.damage
                        else:
                            return True
                    for card in player1.cards_in_battle:
                        if this_card.health > 0 and this_card != card:
                            card.health -= this_card.damage
                            this_card.health -= card.damage
                        else:
                            return True
                else:
                    for card in player1.cards_in_battle:
                        if this_card.health > 0:
                            card.health -= this_card.damage
                            this_card.health -= card.damage
                        else:
                            return True
                    for card in player2.cards_in_battle:
                        if this_card.health > 0 and this_card != card:
                            card.health -= this_card.damage
                            this_card.health -= card.damage
                        else:
                            return True
            case "T Dreadlord":
                if game_moment == GameMoment.Player1Round:
                    player1.add_card_to_cards_in_battle(Card("Minion", 5, 5, 5, "Ordinary unit", "Nothing", "Warrior"))
                else:
                    player2.add_card_to_cards_in_battle(Card("Minion", 5, 5, 5, "Ordinary unit", "Nothing", "Warrior"))
            case "T Sphinx":
                if game_moment == GameMoment.Player1Round:
                    if len(player2.cards_in_battle)>0:
                        card = random.choice(player2.cards_in_battle)
                        card.health = 0
                    else:
                        return False
                else:
                    if len(player1.cards_in_battle)>0:
                        card = random.choice(player1.cards_in_battle)
                        card.health = 0
                    else:
                        return False
            case "Anubisath":
                if game_moment == GameMoment.Player1Round:
                    for card in player1.cards_in_hands:
                        card.health += 3
                        card.damage += 3
                else:
                    for card in player2.cards_in_hands:
                        card.health += 3
                        card.damage += 3
            case "T Elekk":
                if game_moment == GameMoment.Player1Round:
                    for enemy in player2.cards_in_battle:
                        enemy.health -= 3
                else:
                    for enemy in player1.cards_in_battle:
                        enemy.health -= 3
            case "T Neptulon":
                pass
        return True
    def remove_from_gui(self):
        '''
        Removing a card from the playing field
        '''
        if self.card_frame:
            self.card_frame.destroy()


    def __str__(self):
        '''
        Method of displaying a card when writing information
        :return:
        '''
        return f"Name: {self.name}\nDamage: {self.damage}\nHealth: {self.health}\nPrice: {self.price}\nAbility: {self.ability_description}"