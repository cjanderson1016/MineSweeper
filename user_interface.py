"""
File Name: user_interface.py

Description: Builds and manages the Minesweeper game's graphical user interface (GUI) using Tkinter. 
    Includes --> 1) Prompting for number of mines and starting a game, 
                 2) Building the board grid with buttons, 
                 3) Handling button visuals for revealed/flagged/mine cells, 
                 4) Displaying victory or game-over messages, 
                 5) Providing options to replay with same or new mine count.

All Collaborators: Group 4, ChatGPT

Other sources for code: ChatGPT, Tkinter documentation

Date Created: 8/29/2025

Last Updated: 9/17/2025
"""

# ----- user_interface.py -----
import tkinter as tk
from tkinter import messagebox

class UserInterface:
    def __init__(self, root, game_logic, input_handler):
        self.root = root  # Window
        self.game = game_logic  # Game logic
        self.input = input_handler  # Left and right click actions
        self.buttons = []  # Button Widgets
        
        # Header: mine input + start
        self.header_frame = tk.Frame(self.root)
        self.mine_label = tk.Label(self.header_frame, text="Enter number of mines (10-20):")
        self.mine_entry = tk.Entry(self.header_frame, width=5)
        self.start_button = tk.Button(self.header_frame, text="Start Game", command=self.start_game)
        self.header_frame.pack(pady=5)
        self.mine_label.pack(side=tk.LEFT)
        self.mine_entry.pack(side=tk.LEFT)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        # Status text
        self.status_label = tk.Label(self.root, text="Set mines and click Start Game", font=("Arial", 12))
        self.status_label.pack(pady=5)
        
        # Game grid frame
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(padx=10, pady=10)

    def start_game(self):
        # Start game after validating mine input
        try:
            mines = int(self.mine_entry.get())
            if mines < 10 or mines > 20:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a number between 10 and 20.")
            return

        self.hide_mine_prompt()
        self.game.start_game(mines)
        self.build_board()
        self.status_label.config(text=f"Game in progress — Mines: {mines} | Flags remaining: {mines}")

    def hide_mine_prompt(self):
        # Remove mine entry widgets
        self.start_button.pack_forget()
        self.mine_entry.pack_forget()
        self.mine_label.pack_forget()
        self.header_frame.pack_forget()

    def show_mine_prompt(self, default_same=None):
        # Show mine entry again for replay
        self.clear_board_widgets()
        if default_same is not None:
            self.mine_entry.delete(0, tk.END)
            self.mine_entry.insert(0, str(default_same))
        if not self.header_frame.winfo_ismapped():
            self.header_frame.pack(pady=5)
            self.mine_label.pack(side=tk.LEFT)
            self.mine_entry.pack(side=tk.LEFT)
            self.start_button.pack(side=tk.LEFT, padx=5)
        self.status_label.config(text="Choose mines and press Start Game")

    def build_board(self):
        # Create grid with labels and buttons
        for w in self.grid_frame.winfo_children():
            w.destroy()
        self.buttons = []

        # Coloum header from A-J
        tk.Label(self.grid_frame, text="").grid(row=0, column=0)
        for c in range(self.game.board.size):
            tk.Label(self.grid_frame, text=chr(65+c), font=("Arial", 10, "bold")).grid(row=0, column=c+1)
            
        # Row labels and clickable cells
        for r in range(self.game.board.size):
            tk.Label(self.grid_frame, text=str(r+1), font=("Arial", 10, "bold")).grid(row=r+1, column=0)
            row_buttons = []
            for c in range(self.game.board.size):
                btn = tk.Button(self.grid_frame, width=3, height=1,
                                command=lambda r=r, c=c: self.input.handle_left_click(r, c))
                btn.bind("<Button-3>", lambda e, r=r, c=c: self.input.handle_right_click(r, c))
                btn.bind("<Button-2>", lambda e, r=r, c=c: self.input.handle_right_click(r, c))
                btn.grid(row=r+1, column=c+1)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

    def update_board(self):
        # Refresh grid based on the state of the game
        for r in range(self.game.board.size):
            for c in range(self.game.board.size):
                cell = self.game.board.get_cell(r, c)
                btn = self.buttons[r][c]
                if cell['is_flagged']:
                    btn.config(text="🚩", relief=tk.RAISED, bg="SystemButtonFace")
                elif cell['is_covered']:
                    btn.config(text="", relief=tk.RAISED, bg="SystemButtonFace")
                else:
                    btn.config(state="disabled", relief=tk.SUNKEN, bg="lightgrey")
                    if cell['is_mine']:
                        btn.config(text="💣", disabledforeground="red")
                    elif cell['adjacent'] > 0:
                        btn.config(text=str(cell['adjacent']), disabledforeground="black")
                    else:
                        btn.config(text="")
        
        # Update remaining flags in header
        flags_remaining = self.game.total_mines - self.game.flags
        self.status_label.config(text=f"Game in progress — Mines: {self.game.total_mines} | Flags remaining: {flags_remaining}")



    def show_game_over(self, victory):
        # Display win or lose and pop up to replay
        result = "You Win! 🎉" if victory else "Game Over 💥"
        choice = messagebox.askyesnocancel(result, "Play Again?\nYes = Same Mines\nNo = Choose New Mines\nCancel = Quit")

        if choice is True: 
            # Restart with same mine count
            self.game.start_game(self.game.total_mines)
            self.build_board()
            self.status_label.config(text=f"New game started with {self.game.total_mines} mines — Good luck!")
        elif choice is False:
            # Ask for new mine count
            self.show_mine_prompt(default_same=self.game.total_mines)
        else:
            self.root.destroy()

    def clear_board_widgets(self):
        # Clear the whole grid
        for w in self.grid_frame.winfo_children():
            w.destroy()
        self.buttons = []
