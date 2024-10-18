import tkinter as tk
import Hearthstone_gui as hearthstone
import Creature
from Player import *

creature = Creature.Creature()

class MainGui:
    '''
    Initial program window
    '''
    def __init__(self):
        '''
        Positions the window and blocks expansion
        '''
        self.root = tk.Tk()
        self.window_width = 800
        self.window_height = 600

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.position_x = int(self.screen_width / 2 - self.window_width / 2)
        self.position_y = int(self.screen_height / 2 - self.window_height / 2)

        self.root.geometry(f'{self.window_width}x{self.window_height}+{self.position_x}+{self.position_y}')
        self.root.resizable(False, False)
        self.root.title("Main menu HearthStone")

        self.create_widgets()

    def create_widgets(self):
        '''
        Adding buttons to the screen
        '''
        title_label = tk.Label(self.root, text="HearthStone", font=("Arial", 24, "bold"))
        title_label.pack(pady=(20, 40))

        self.button1 = tk.Button(self.root, text="Player VS Bot", font=("Arial", 16), width=20, height=3)
        self.button1.bind("<Button-1>", self.player_vs_bot)

        self.button2 = tk.Button(self.root, text="Player VS Player", font=("Arial", 16), width=20, height=3)
        self.button2.bind("<Button-1>", self.player_vs_player)

        self.button1.pack(pady=20)
        self.button2.pack(pady=20)

        self.information_button = tk.Button(self.root, text="Small", font=("Arial", 10), width=10, height=2)
        self.information_button.place(x=self.window_width - 110, y=self.window_height - 50)
        self.information_button.bind("<Button-1>", self.show_instructions)

    def show_instructions(self, event):
        '''
        Reading instructions from text and showing them to the user
        :param event: click event
        '''
        instruction_window = tk.Toplevel(self.root)
        instruction_window.title("Instructions")
        instruction_window.geometry("600x800")
        instruction_window.transient(self.root)
        instruction_window.grab_set()

        instruction_text = ""
        try:
            with open("Instruction", "r") as file:
                instruction_text = file.read()
        except FileNotFoundError:
            instruction_text = "Instruction file not found."

        text_widget = tk.Text(instruction_window, wrap="word", font=("Arial", 12))
        text_widget.insert("1.0", instruction_text)
        text_widget.config(state="disabled")
        text_widget.pack(expand=True, fill="both")

        close_button = tk.Button(instruction_window, text="Close", command=instruction_window.destroy)
        close_button.pack(pady=10)

    def player_vs_player(self, event):
        '''
        Display HearthStone_gui for two players
        :param event: с click event
        '''
        self.root.destroy()

        player1 = Player("Player 1", creature.create_deck_for_battle())
        player2 = Player("Player 2", creature.create_deck_for_battle())

        game_root = tk.Tk()
        game_app = hearthstone.HearthstoneApp(game_root, player1, player2)
        game_app.display_cards_in_game()

        game_root.mainloop()

    def player_vs_bot(self, event):
        choice_window = tk.Toplevel(self.root)
        choice_window.geometry("300x200")
        choice_window.title("Choose difficulty")

        choice_window.transient(self.root)
        choice_window.grab_set()

        tk.Label(choice_window, text="Choose an option", font=("Arial", 14)).pack(pady=20)

        button1 = tk.Button(choice_window, text="Beginner", font=("Arial", 12),
                            command=lambda: self.player_vs_bot_display("Beginner"))
        button2 = tk.Button(choice_window, text="Advanced", font=("Arial", 12),
                            command=lambda: self.player_vs_bot_display("Advanced"))

        button1.pack(pady=10)
        button2.pack(pady=10)

    def player_vs_bot_display(self, difficulty):

        '''
        Display HearthStone_gui for one player and a bot
        :param difficulty: bot difficulty
        :return:
        '''
        self.root.destroy()

        player1 = Player("Player 1", creature.create_deck_for_battle())
        player2 = AIPlayer("Player 2", creature.create_deck_for_battle(), difficulty)

        game_root = tk.Tk()
        game_app = hearthstone.HearthstoneApp(game_root, player1, player2)
        game_app.display_cards_in_game()

        game_root.mainloop()

    def run(self):
        '''
        Launch screen
        '''
        self.root.mainloop()

if __name__ == "__main__":
    app = MainGui()
    app.run()
