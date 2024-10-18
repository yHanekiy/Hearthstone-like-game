import random
import tkinter as tk
from enum import Enum
from tkinter import simpledialog

import EndGame_gui
import Player
from MyFrame import MyFrame


class GameMoment(Enum):
    Player1Round = 1
    Player2Round = 2


class HearthstoneApp:
    '''
    Hearthstone GUI

    The main screen of the game, where all events take place
    '''
    counter_round = 0
    player1_cards_battle = []
    player2_cards_battle = []
    player1_cards_hands = []
    player2_cards_hands = []
    current_card = None

    def __init__(self, root, player1, player2):

        self.player2 = player2
        self.player1 = player1
        self.GameMoment = GameMoment.Player1Round
        self.root = root
        self.root.title("Hearthstone Clone")
        self.setup_window()
        self.setup_ui()

        self.card_frame_player_1 = tk.Canvas()
        self.card_frame_player_2 = tk.Canvas()
        self.card_frame_enemy_1 = tk.Canvas()
        self.card_frame_enemy_2 = tk.Canvas()

    def setup_window(self):
        '''
            Positions the window and blocks expansion
        '''
        window_width = 1300
        window_height = 600

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        position_x = int(screen_width / 2 - window_width / 2)
        position_y = int(screen_height / 2 - window_height / 2)

        self.root.geometry(f'{window_width}x{window_height}+{position_x}+{position_y}')
        self.root.resizable(False, False)

    def setup_ui(self):
        '''
            Creates graphic design
        '''
        self.player_frame = tk.Frame(self.root, bg='LightYellow2', height=100)
        self.enemy_frame = tk.Frame(self.root, bg='LightYellow2', height=100)

        self.board_enemy_frame = tk.Frame(self.root, bg='white', height=200)
        self.board_enemy_frame.bind("<Button-1>", self.action_with_board_enemy)

        self.button_change_creature_1 = tk.Button(self.enemy_frame, text="Change creatures",
                                                  command=self.change_creature_1)
        self.button_change_creature_1.place(anchor='sw', relx=0.79, rely=0.4)

        self.board_player_frame = tk.Frame(self.root, bg='white', height=200)
        self.board_player_frame.bind("<Button-1>", self.action_with_board_player)

        self.button_change_creature_2 = tk.Button(self.player_frame, text="Change creatures",
                                                  command=self.change_creature_2)
        self.button_change_creature_2.place(anchor='sw', relx=0.79, rely=0.87)

        board = tk.Frame(self.root, bg='LightSalmon4', height=5)

        self.enemy_frame.pack(side='top', fill='x')
        self.board_enemy_frame.pack(side='top', fill='x')
        board.pack(fill='x')
        self.board_player_frame.pack(side='top', fill='x', expand=True)
        self.player_frame.pack(side='bottom', fill='x')

        self.playe1_iconic_hero = self.display_iconic_hero(self.player2, self.player_frame)

        self.enemy_deck_canvas = tk.Canvas(self.board_enemy_frame, bg='white', width=50, height=100)
        self.enemy_deck_canvas.create_rectangle(5, 5, 45, 95, outline='black', fill='coral4')
        self.enemy_deck_canvas.create_text(25, 50, text='E', font=('Arial', 20, 'bold'), fill='white')
        self.enemy_deck_canvas.pack(side='right', padx=20, pady=50)

        self.playe2_iconic_hero = self.display_iconic_hero(self.player1, self.enemy_frame)

        self.player_deck_canvas = tk.Canvas(self.board_player_frame, bg='white', width=50, height=100)
        self.player_deck_canvas.create_rectangle(5, 5, 45, 95, outline='black', fill='DodgerBlue')
        self.player_deck_canvas.create_text(25, 50, text='P', font=('Arial', 20, 'bold'), fill='white')
        self.player_deck_canvas.pack(side='right', padx=20, pady=50)

        self.end_turn_button = tk.Button(self.root, text="End Turn", command=self.end_turn)
        self.end_turn_button.place(anchor='sw', relx=0.93, rely=0.53)


    def change_creature_1(self):
        '''
        Replaces cards in the second player's hand
        '''
        if self.GameMoment == GameMoment.Player2Round:
            unique_list = []

            if isinstance(self.player2, Player.AIPlayer):
                for i, card in enumerate(self.player2.cards_in_hands):
                    if card.price >= 5:
                        unique_list.append(i)
                        self.append_message(f"Card {card.name} was changed")
            else:
                user_input = simpledialog.askstring("Change creatures",
                                                "Write a index of creature to change separated by space")
                if user_input:
                    indexes = user_input.split(' ')
                    unique_list = list(set(indexes))
            cards_to_return = []
            for index in unique_list:
                try:
                    if isinstance(self.player2, Player.AIPlayer):
                        cards_to_return.append(self.player2.cards_in_hands[int(index)])
                    else:
                        if int(index) - 1 < len(self.player2.cards_in_hands):
                            cards_to_return.append(self.player2.cards_in_hands[int(index) - 1])
                except Exception:
                    print("It's not number")

            if len(cards_to_return) > 0:
                for card in cards_to_return:
                    card.remove_from_gui()
                    self.player2.cards_in_hands.remove(card)
                    self.player2.full_cards.append(card)
                for i in range(0, len(cards_to_return)):
                    self.player2.cards_in_hands.append(self.player2.full_cards[i])
                    self.player2.full_cards.remove(self.player2.full_cards[i])
                self.change_game_moment()
                self.display_cards_in_game()
                self.change_game_moment()
                self.display_cards_in_game()

                self.button_change_creature_1.destroy()

    def change_creature_2(self):
        '''
        Replaces cards in the second player's hand
        '''
        if self.GameMoment == GameMoment.Player1Round:
            user_input = simpledialog.askstring("Change creatures",
                                                "Write a index of creature to change separated by space")
            unique_list = []
            if user_input:
                indexes = user_input.split(' ')
                unique_list = list(set(indexes))
            cards_to_return = []
            for index in unique_list:
                try:
                    if int(index) - 1 < len(self.player1.cards_in_hands):
                        cards_to_return.append(self.player1.cards_in_hands[int(index) - 1])
                except Exception:
                    print("It's not number")

            if len(cards_to_return) > 0:
                for card in cards_to_return:
                    card.remove_from_gui()
                    self.player1.cards_in_hands.remove(card)
                    self.player1.full_cards.append(card)
                for i in range(0, len(cards_to_return)):
                    self.player1.cards_in_hands.append(self.player1.full_cards[i])
                    self.player1.full_cards.remove(self.player1.full_cards[i])
                for i in range(0,4):
                    self.change_game_moment()
                    self.display_cards_in_game()

                self.button_change_creature_2.destroy()
    def action_with_board_player(self, event):
        '''
        Performs the operation of placing a first player`s card on the field, that is, puts the card into play
        :param event: click event
        '''
        if len(self.player1_cards_battle) < 9 and self.GameMoment == GameMoment.Player1Round and self.current_card and \
                str(self.current_card.card_frame).split("!")[1] == "frame.":
            if (self.player1.mana >= self.current_card.price):
                if str(self.current_card.style).strip() == "Warrior":
                    self.player1.add_card_to_cards_in_battle_from_hands(self.current_card)
                else:
                    if str(self.current_card.style).strip() == "SpellAttacker" and len(
                            self.player2.cards_in_battle) == 0:
                        return
                    self.player1.cards_in_hands.remove(self.current_card)
                if self.current_card.activate_ability(self.player1, self.player2, self.GameMoment, self.current_card) == False and str(self.current_card.style).strip() == "SpellAttacker":
                    self.player1.cards_in_hands.append(self.current_card)
                if self.check_end_game():
                    return
                self.player1.mana -= self.current_card.price
                self.current_card.remove_from_gui()
                self.player1_cards_hands.remove(self.current_card)
                self.playe1_iconic_hero.list[1].itemconfig(self.playe1_iconic_hero.list[1].find_all()[1],
                                                           text=str(self.player1.mana))
                self.playe1_iconic_hero.list[0].itemconfig(self.playe1_iconic_hero.list[0].find_all()[1],
                                                           text=str(self.player1.hp))
                self.playe2_iconic_hero.list[1].itemconfig(self.playe2_iconic_hero.list[1].find_all()[1],
                                                           text=str(self.player2.mana))
                self.playe2_iconic_hero.list[0].itemconfig(self.playe2_iconic_hero.list[0].find_all()[1],
                                                           text=str(self.player2.hp))
                for i in range(0, 4):
                    self.change_game_moment()
                    self.display_cards_in_game()

                self.current_card = None

    def action_with_board_enemy(self, event):
        '''
        Performs the operation of placing a second player`s card on the field, that is, puts the card into play
        :param event: click event
        '''
        if len(self.player2_cards_battle) < 9 and self.GameMoment == GameMoment.Player2Round and self.current_card and \
                str(self.current_card.card_frame).split("!")[1] == "frame2.":
            if (self.player2.mana >= self.current_card.price):
                if str(self.current_card.style).strip() == "Warrior":
                    self.player2.add_card_to_cards_in_battle_from_hands(self.current_card)
                else:
                    if str(self.current_card.style).strip() == "SpellAttacker" and len(
                            self.player1.cards_in_battle) == 0:
                        return
                    self.player2.cards_in_hands.remove(self.current_card)
                if self.current_card.activate_ability(self.player1, self.player2, self.GameMoment, self.current_card) == False and str(self.current_card.style).strip() == "SpellAttacker":
                    self.player2.cards_in_hands.append(self.current_card)
                if self.check_end_game():
                    return
                self.player2.mana -= self.current_card.price
                self.current_card.remove_from_gui()
                self.player2_cards_hands.remove(self.current_card)
                self.playe1_iconic_hero.list[1].itemconfig(self.playe1_iconic_hero.list[1].find_all()[1],
                                                           text=str(self.player1.mana))
                self.playe1_iconic_hero.list[0].itemconfig(self.playe1_iconic_hero.list[0].find_all()[1],
                                                           text=str(self.player1.hp))
                self.playe2_iconic_hero.list[1].itemconfig(self.playe2_iconic_hero.list[1].find_all()[1],
                                                           text=str(self.player2.mana))
                self.playe2_iconic_hero.list[0].itemconfig(self.playe2_iconic_hero.list[0].find_all()[1],
                                                           text=str(self.player2.hp))
                self.change_game_moment()
                self.display_cards_in_game()
                self.change_game_moment()
                self.display_cards_in_game()
                self.change_game_moment()
                self.display_cards_in_game()
                self.change_game_moment()
                self.display_cards_in_game()
                self.current_card = None

    def check_end_game(self):
        '''
        There is a check to see if the game is over, that is, if all players have more than 0 hp
        :return bool True if the game is over, otherwise False
        '''
        if self.player1.hp <= 0 and self.player2.hp <= 0:
            self.root.destroy()
            EndGame_gui.EndGameGUI("Draw")
            return True
        elif self.player1.hp <= 0:
            self.root.destroy()
            EndGame_gui.EndGameGUI(self.player2.name + " wins")
            return True
        elif self.player2.hp <= 0:
            self.root.destroy()
            EndGame_gui.EndGameGUI(self.player1.name + " wins")
            return True
        return False

    def end_turn(self):
        '''
        Ends a player's turn and assigns additional mana and health to them
        '''

        if self.check_end_game():
            return
        self.counter_round += 1
        if self.GameMoment == GameMoment.Player1Round:
            self.GameMoment = GameMoment.Player2Round
            temp = self.player1_cards_battle
            if self.counter_round != 0 and self.player1.all_current_mana < self.player1.maximum_mana:
                self.player1.all_current_mana += 1
                self.player1.mana = self.player1.all_current_mana
            else:
                self.player1.mana = self.player1.all_current_mana
            # increase the amount of player1`s mana
            self.playe1_iconic_hero.list[1].itemconfig(self.playe1_iconic_hero.list[1].find_all()[1],
                                                           text=str(self.player1.mana))
            if self.counter_round == 1 and self.button_change_creature_2:
                self.button_change_creature_2.destroy()
            for card in self.player1.cards_in_battle:
                card.sleep = False
            for card in self.player1.cards_in_battle:
                card.already_attacked = False
            if self.player1.full_cards:
                if len(self.player1.cards_in_hands) == 9:
                    try:
                        info_window = tk.Toplevel(self.root)
                        info_window.wm_overrideredirect(True)
                        card = self.player1.full_cards[0]
                        info_label = tk.Message(info_window,
                                                text=card,
                                                bg="white", justify="left", width=200)
                        info_label.pack()

                        user_input = tk.simpledialog.askstring("Replace creature in hand",
                                                               "Write a index of creature to replace or something another to remove new card")
                        info_window.destroy()
                        index = user_input.split(' ')[0]
                        self.player1.cards_in_hands[int(index) - 1].remove_from_gui()
                        self.player1.cards_in_hands[int(index) - 1] = self.player1.full_cards[0]
                        self.player1.full_cards.remove(self.player1.full_cards[0])
                    except Exception:
                        self.player1.full_cards.remove(self.player1.full_cards[0])
                else:
                    self.player1.add_card_to_cards_in_hands(self.player1.full_cards[0])
                    self.player1.full_cards.remove(self.player1.full_cards[0])
            else:
                self.player1.hp -= 1
                self.playe1_iconic_hero.list[0].itemconfig(self.playe1_iconic_hero.list[0].find_all()[1],
                                                           text=str(self.player1.hp))
        else:
            self.GameMoment = GameMoment.Player1Round
            temp = self.player2_cards_battle
            if self.counter_round != 0 and self.player2.all_current_mana < self.player2.maximum_mana:
                self.player2.all_current_mana += 1
                self.player2.mana = self.player2.all_current_mana
                self.playe2_iconic_hero.list[1].itemconfig(self.playe2_iconic_hero.list[1].find_all()[1],
                                                           text=str(self.player2.mana))
            else:
                self.player2.mana = self.player2.all_current_mana
            if self.counter_round == 2 and self.button_change_creature_1:
                self.button_change_creature_1.destroy()
            for card in self.player2.cards_in_battle:
                card.sleep = False
            for card in self.player2.cards_in_battle:
                card.already_attacked = False
            if self.player2.full_cards:
                if len(self.player2.cards_in_hands) == 9:
                    try:
                        if isinstance(self.player2, Player.AIPlayer):
                            self.player2.full_cards.remove(self.player2.full_cards[0])
                        else:
                            info_window = tk.Toplevel(self.root)
                            info_window.wm_overrideredirect(True)
                            card = self.player2.full_cards[0]
                            info_label = tk.Message(info_window,
                                                text=card,
                                                bg="white", justify="left", width=200)
                            info_label.pack()

                            user_input = tk.simpledialog.askstring("Replace creature in hand",
                                                                "Write a index of creature to replace or something another to remove new card")
                            info_window.destroy()
                            index = user_input.split(' ')[0]
                            self.player2.cards_in_hands[int(index) - 1].remove_from_gui()
                            self.player2.cards_in_hands[int(index) - 1] = card
                            self.player2.full_cards.remove(card)
                    except Exception:
                        self.player2.full_cards.remove(self.player2.full_cards[0])
                else:
                    self.player2.add_card_to_cards_in_hands(self.player2.full_cards[0])
                    self.player2.full_cards.remove(self.player2.full_cards[0])
            else:
                self.player2.hp -= 1
                self.playe2_iconic_hero.list[0].itemconfig(self.playe2_iconic_hero.list[0].find_all()[1],
                                                           text=str(self.player2.hp))



        self.display_cards_in_game()
        self.current_card = None

        if isinstance(self.player2, Player.AIPlayer) and self.GameMoment == GameMoment.Player2Round:
            self.action_for_bot()

    def action_for_bot(self):
        '''
        A method for playing with a bot that imitates the behavior of a living character
        '''
        self.create_info_window()
        if self.counter_round == 1:
             self.change_creature_1()
        cards_to_add = self.player2.generate_list_to_battle(self.player1)
        for card in cards_to_add:
            self.current_card = card
            self.action_with_board_enemy(None)
            self.append_message(f"Card {card.name} was placed")

        for card in self.player2.cards_in_battle:
            self.current_card = card
            creatures_with_taunt = [card for card in self.player1.cards_in_battle if card.taunt]
            if creatures_with_taunt:
                if card.health > 0 and card.sleep == False:
                    chosen_card = random.choice(creatures_with_taunt)
                    self.highlight_card(chosen_card)
                    self.append_message(f"Card {chosen_card.name} was attacked by {card.name}")

            else:
                if random.uniform(0, 10) < 8.2 and self.player1.cards_in_battle:
                    if card.health > 0 and card.sleep == False:
                        self.current_card = card
                        chosen_card = random.choice(self.player1.cards_in_battle)
                        self.highlight_card(chosen_card)
                        self.append_message(f"Card {chosen_card.name} was attacked by {card.name}")

                else:
                    if card.health > 0 and card.sleep == False:
                        self.on_iconic_hero_click(None)
                        self.append_message(f"Card {self.player2.name} was attacked by {card.name}")
        self.end_turn()

    def create_info_window(self):
        '''
        Displays a window in which everything is written in order, what the bot did during the previous round
        '''
        self.info_window = tk.Toplevel(self.root)
        self.info_window.wm_overrideredirect(True)

        self.info_area = tk.Text(self.info_window, bg="white", width=60, height=50, state="disabled")
        self.info_area.pack()

        screen_height = self.root.winfo_screenheight()

        x_position =0
        y_position = screen_height - 500

        self.info_window.geometry(f"220x500+{x_position}+{y_position}")

    def append_message(self, message):
        '''
        Adds bot actions to the window
        :param message: message to be added to the window
        '''
        self.info_area.config(state="normal")
        self.info_area.insert(tk.END, message + "\n")
        self.info_area.config(state="disabled")
        self.info_area.yview(tk.END)

    def display_iconic_hero(self, player, frame):
        '''
        Displays the character icon on the playing field
        :param player: the player whose icon should be displayed
        :param frame: the frame on which the icon will be displayed
        :return:  the frame as a character icon
        '''
        current_frame = tk.Frame(frame, bg="white", width=150, height=75, bd=2, relief="solid",
                                 highlightthickness=0)
        current_frame.pack(side="right", padx=10, pady=10)
        title_canvas = tk.Canvas(current_frame, width=90, height=30, bg="white", highlightthickness=0)
        title_canvas.create_text(45, 15, text=player.name, fill="black", font=("Arial", 10, "bold"))
        title_canvas.place(relx=0.2, rely=0.0, anchor='nw')

        healt_circle = tk.Canvas(current_frame, width=30, height=30, bg="white", highlightthickness=0)
        healt_circle.create_oval(5, 5, 25, 25, outline="black", fill="red")
        healt_circle.create_text(15, 15, text=str(player.hp), fill="white")
        healt_circle.place(relx=0.0, rely=0.5, anchor='nw')

        mana_circle = tk.Canvas(current_frame, width=30, height=30, bg="white", highlightthickness=0)
        mana_circle.create_oval(5, 5, 25, 25, outline="black", fill="SteelBlue3")
        mana_circle.create_text(15, 15, text=str(player.mana), fill="white")
        mana_circle.place(relx=0.78, rely=0.5, anchor='nw')

        iconic_hero = MyFrame(current_frame, [healt_circle, mana_circle])
        current_frame.bind("<Button-1>", self.on_iconic_hero_click)
        current_frame.bind("<Button-1>", self.on_iconic_hero_click)

        return iconic_hero

    def on_iconic_hero_click(self, event):
        '''
        Performs an attack on an enemy character
        :param event: click event
        '''
        if self.current_card is None:
            return
        if str(self.current_card.card_frame).split('!')[1] == 'frame3.' and self.current_card.already_attacked == False:
            if self.check_taunt_cards(self.player1, None):
                self.player1.hp -= self.current_card.damage
                if self.check_end_game():
                    return
                self.current_card.already_attacked = True
                self.playe1_iconic_hero.list[0].itemconfig(self.playe1_iconic_hero.list[0].find_all()[1],
                                                       text=str(self.player1.hp))
        elif str(self.current_card.card_frame).split('!')[1] == 'frame4.' and self.current_card.already_attacked == False:
            if self.check_taunt_cards(self.player2, None):
                self.player2.hp -= self.current_card.damage
                if self.check_end_game():
                    return
                for card in self.player1.cards_in_battle:
                    if card == self.current_card:
                        card.already_attacked = True
                self.current_card.already_attacked = True
                self.playe2_iconic_hero.list[0].itemconfig(self.playe2_iconic_hero.list[0].find_all()[1],
                                                       text=str(self.player2.hp))
        self.change_game_moment()
        self.display_cards_in_game()
        self.change_game_moment()
        self.display_cards_in_game()


    def display_cards_in_game(self):
        '''
        Displays all the cards in the game (in a hands, in a battlefields)
        '''
        self.display_back_card(len(self.player2.cards_in_hands), len(self.player1.cards_in_hands))

        if self.GameMoment == GameMoment.Player1Round:
            self.player1_cards_hands.clear()
            for card in self.player1.cards_in_hands:
                card_frame = tk.Frame(self.player_frame, bg="white", width=100, height=75, bd=2, relief="solid")
                card_frame.pack(side="left", padx=10, pady=10)

                title_canvas = tk.Canvas(card_frame, width=90, height=30, bg="white", highlightthickness=0)
                title_canvas.create_text(45, 15, text=card.name, fill="black", font=("Arial", 10, "bold"))
                title_canvas.place(relx=0.5, rely=0.25, anchor='center')

                card_frame.bind("<Enter>", lambda event, c=card: self.show_info(event, c))
                card_frame.bind("<Leave>", self.hide_info)

                card_frame.bind("<Button-1>", lambda event, c=card: self.on_card_clicked(event, c))

                card.card_frame = card_frame
                self.player1_cards_hands.append(card)

            self.player2_cards_battle.clear()
            for card in self.player2.cards_in_battle:
                card.remove_from_gui()
            for card in self.player2.cards_in_hands:
                card.remove_from_gui()
            for card in self.player2.cards_in_battle:
                if card.sleep == False:
                    self.display_front_card(card, self.board_enemy_frame)


        else:
            self.player2_cards_hands.clear()
            for card in self.player2.cards_in_hands:
                card_frame = tk.Frame(self.enemy_frame, bg="white", width=100, height=75, bd=2, relief="solid")
                card_frame.pack(side="left", padx=10, pady=10)

                title_canvas = tk.Canvas(card_frame, width=90, height=30, bg="white", highlightthickness=0)
                title_canvas.create_text(45, 15, text=card.name, fill="black", font=("Arial", 10, "bold"))
                title_canvas.place(relx=0.5, rely=0.25, anchor='center')

                card_frame.bind("<Enter>", lambda event, c=card: self.show_info(event, c))
                card_frame.bind("<Leave>", self.hide_info)

                card_frame.bind("<Button-1>", lambda event, c=card: self.on_card_clicked(event, c))

                card.card_frame = card_frame
                self.player2_cards_hands.append(card)
            self.player1_cards_battle.clear()
            for card in self.player1.cards_in_battle:
                card.remove_from_gui()
            for card in self.player1.cards_in_hands:
                card.remove_from_gui()
            for card in self.player1.cards_in_battle:
                if card.sleep == False:
                    self.display_front_card(card, self.board_player_frame)

    def on_card_clicked(self, event, card):
        '''
        Selects a card that is in the player's hand and update graphics
        :param event: click event
        :param card: chosen card
        '''
        event.widget.config(bg="seashell3")
        self.current_card = card
        if self.GameMoment == GameMoment.Player1Round:
            for card in self.player1_cards_hands:
                if card.card_frame != self.current_card.card_frame:
                    card.card_frame.config(bg="white")
            for myFrame in self.player1_cards_battle:
                if myFrame.card.already_attacked:
                    myFrame.list[2].itemconfig(1, fill="black")
                else:
                    myFrame.list[2].itemconfig(1, fill="white")

        else:
            for card in self.player2_cards_hands:
                if card.card_frame != self.current_card.card_frame:
                    card.card_frame.config(bg="white")
            for myFrame in self.player2_cards_battle:
                if myFrame.card.already_attacked:
                    myFrame.list[2].itemconfig(1, fill="black")
                else:
                    myFrame.list[2].itemconfig(1, fill="white")

    def display_front_card(self, card, frame):
        '''
        Displays the front part of card on the playing field

        :param card: card based on which the frame is drawn
        :param frame: where the card is drawn
        '''
        if card.health > 0:
            card_frame = tk.Frame(frame, bg="white", width=100, height=150, bd=2, relief="solid",
                                  highlightbackground="red")
            card_frame.pack(side="left", padx=10, pady=10)

            title_canvas = tk.Canvas(card_frame, width=90, height=30, bg="white", highlightthickness=0)
            title_canvas.create_text(45, 15, text=card.name, fill="black", font=("Arial", 10, "bold"))
            title_canvas.place(x=0, y=0)

            description_canvas = tk.Canvas(card_frame, width=90, height=65, bg="white", highlightthickness=0)
            description_text = card.ability_description
            description_lines = [description_text[i:i + 10] for i in
                                 range(0, len(description_text), 10)]
            for i, line in enumerate(description_lines):
                description_canvas.create_text(45, 15 + 15 * i, text=line, fill="black")
            description_canvas.place(x=5, y=25)

            damage_circle = tk.Canvas(card_frame, width=30, height=30, bg="white", highlightthickness=0)
            damage_circle.create_oval(5, 5, 25, 25, outline="black", fill="red")
            damage_circle.create_text(15, 15, text=str(card.damage), fill="white")
            damage_circle.place(x=0, y=115)

            health_circle = tk.Canvas(card_frame, width=30, height=30, bg="white", highlightthickness=0)
            health_circle.create_oval(5, 5, 25, 25, outline="black", fill="green")
            health_circle.create_text(15, 15, text=str(card.health), fill="white")
            health_circle.place(x=65, y=115)

            choose_circle = tk.Canvas(card_frame, width=30, height=30, bg="white", highlightthickness=0)
            if card.already_attacked == False:
                choose_circle.create_oval(5, 5, 25, 25, outline="black", fill="white")
            else:
                choose_circle.create_oval(5, 5, 25, 25, outline="black", fill="black")
            choose_circle.place(x=32, y=115)

            card_frame.bind("<Button-1>",
                            lambda event,: self.highlight_card(card))

            card.card_frame = card_frame
            card.chosen_circle = choose_circle
            if str(card.card_frame).split('!')[1] == 'frame4.':
                self.player1_cards_battle.append(MyFrame(card, [damage_circle, health_circle, choose_circle]))
            else:
                self.player2_cards_battle.append(MyFrame(card, [damage_circle, health_circle, choose_circle]))
        else:
            if card in self.player1.cards_in_battle:
                self.player1.cards_in_battle.remove(card)
            if card in self.player2.cards_in_battle:
                self.player2.cards_in_battle.remove(card)

    def display_back_card(self, player1_cards_length, player2_cards_length):
        '''
        Displays the back part of card on the playing field and the number of cards in a hand

        :param player1_cards_length: amount of first player cards
        :param player2_cards_length: amount of second player cards
        '''
        if self.GameMoment != GameMoment.Player2Round:
            self.card_frame_enemy_1 = tk.Frame(self.enemy_frame, bg="coral4", width=60, height=75, bd=2, relief="solid",
                                               highlightthickness=0)
            self.card_frame_enemy_1.pack(side="left", padx=10, pady=10)
            label = tk.Label(self.card_frame_enemy_1, text='E', font=('Arial', 20, 'bold'), bg='coral4', fg='white')
            label.place(relx=0.5, rely=0.5, anchor='center')

            self.card_frame_enemy_2 = tk.Frame(self.enemy_frame, bg="LightYellow2", width=60, height=75)
            self.card_frame_enemy_2.pack(side="left", padx=10, pady=10)
            label = tk.Label(self.card_frame_enemy_2, text=player1_cards_length, font=('Arial', 20, 'bold'),
                             bg='LightYellow2', fg='Black')
            label.place(relx=0.2, rely=0.5, anchor='center')
            self.card_frame_player_1.destroy()
            self.card_frame_player_2.destroy()
        else:
            self.card_frame_player_1 = tk.Frame(self.player_frame, bg="DodgerBlue", width=60, height=75, bd=2,
                                                relief="solid",
                                                highlightthickness=0)
            self.card_frame_player_1.pack(side="left", padx=10, pady=10)
            label = tk.Label(self.card_frame_player_1, text='P', font=('Arial', 20, 'bold'), bg='DodgerBlue',
                             fg='black')
            label.place(relx=0.5, rely=0.5, anchor='center')

            self.card_frame_player_2 = tk.Frame(self.player_frame, bg="LightYellow2", width=60, height=75)
            self.card_frame_player_2.pack(side="left", padx=10, pady=10)
            label = tk.Label(self.card_frame_player_2, text=player2_cards_length, font=('Arial', 20, 'bold'),
                             bg='LightYellow2', fg='Black')
            label.place(relx=0.2, rely=0.5, anchor='center')
            self.card_frame_enemy_1.destroy()
            self.card_frame_enemy_2.destroy()

    def highlight_card(self, this_card):
        '''
        Selects a card on the battlefield, or makes an attack on an enemy card
        :param this_card: card on which the operation is carried out
        '''
        if (str(this_card.card_frame).split('!')[1] == 'frame4.' and self.GameMoment == GameMoment.Player1Round) or (
                str(this_card.card_frame).split('!')[1] == 'frame3.' and self.GameMoment == GameMoment.Player2Round):
            if this_card.already_attacked == False:
                self.current_card = this_card
                if self.GameMoment == GameMoment.Player1Round:
                    temp = self.player1_cards_battle
                    for card in self.player1_cards_hands:
                        card.card_frame.config(bg="white")
                else:
                    temp = self.player2_cards_battle
                    for card in self.player2_cards_hands:
                        card.card_frame.config(bg="white")
                for myFrame in temp:
                    if myFrame.card.already_attacked == False:
                        myFrame.list[2].itemconfig(1, fill="white")
                new_color = "yellow"
                print(this_card.chosen_circle)
                this_card.chosen_circle.itemconfig(1, fill=new_color)

        else:
            try:
                card_damage = self.current_card.damage
                receive_damage = this_card.damage
                if self.GameMoment == GameMoment.Player1Round:
                    player = self.player2
                else:
                    player = self.player1
                if this_card.taunt or self.check_taunt_cards(player, this_card):
                    if str(self.current_card.card_frame).split('!')[1] == 'frame4.' or \
                            str(self.current_card.card_frame).split('!')[1] == 'frame3.':
                        self.change_game_moment()
                        this_card.health -= card_damage
                        this_card.chosen_circle.itemconfig(1, fill="black")
                        self.current_card.already_attacked = True
                        self.current_card.health -= receive_damage
                        self.current_card = None
                        self.display_cards_in_game()
                        self.change_game_moment()
                        self.display_cards_in_game()
                        self.change_game_moment()
                        self.display_cards_in_game()
                        self.change_game_moment()
                        self.display_cards_in_game()
            except Exception:
                print("You don`t choose an offensive card")

    def check_taunt_cards(self, player, this_card):
        '''
        Checking whether the attack is made on a creature with a taunt, if it does exist
        :param player: the player whose presence of creatures with taunt is checked
        :param this_card: an object that is being damaged
        :return:
        '''
        for card in player.cards_in_battle:
            if card.taunt == True and card != this_card:
                return False
        return True

    def change_game_moment(self):
        '''
        Changes the round index
        '''
        if self.GameMoment == GameMoment.Player1Round:
            self.GameMoment = GameMoment.Player2Round
        else:
            self.GameMoment = GameMoment.Player1Round

    def show_info(self, event, card):
        '''
        Displays information about the creature that the player has in hand
        :param event: enter event
        :param card: card, information about which should be displayed
        '''
        self.info_window = tk.Toplevel(self.root)
        self.info_window.geometry(f"+{event.x_root + 20}+{event.y_root + 20}")
        self.info_window.wm_overrideredirect(True)

        info_label = tk.Message(self.info_window,
                                text=card,
                                bg="white", justify="left", width=200)
        info_label.pack()

    def hide_info(self, event):
        '''
        Hides previously displayed information
        :param event: leave event
        :return:
        '''
        if hasattr(self, 'info_window'):
            self.info_window.destroy()
            del self.info_window
