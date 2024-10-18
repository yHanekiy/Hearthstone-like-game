import tkinter

class EndGameGUI:
    '''
    EndGame GUI

    Window for ending the game, displaying the winner
    '''
    def __init__(self, player):
        self.root = tkinter.Tk()
        self.root.title("Finish game")
        self.setup_gui(player)
        self.root.mainloop()

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

    def setup_gui(self, player):
        '''
        Creates graphic design
        '''
        self.setup_window()
        self.root.after(100, self.create_canvas, player)

    def create_canvas(self, text):
        '''
        Creates a caption about the winning player
        :param text: text to be displayed
        '''
        title_canvas = tkinter.Canvas(self.root, width=self.root.winfo_width(), height=self.root.winfo_height(), bg="white", highlightthickness=0)
        title_canvas.create_text(self.root.winfo_width() / 2, self.root.winfo_height() / 2, text=text, fill="black", font=("Arial", 40, "bold"))
        title_canvas.pack()