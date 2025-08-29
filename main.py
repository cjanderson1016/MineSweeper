# ----- main.py -----
import tkinter as tk
from board_manager import BoardManager
from game_logic import GameLogic
from input_handler import InputHandler
from user_interface import UserInterface

def main():
    # declare the root for the GUI
    root = tk.Tk()
    # give the GUI the title "Minesweeper"
    root.title("Minesweeper")

    # initialize the game board
    board = BoardManager()

    # initialize the game logic with the game board
    game = GameLogic(board)

    # initialize the UI with the GUI root and game logic
    # None for input handler because it hasn't been created yet and the handler needs the ui to be initialized
    ui = UserInterface(root, game, None)

    # initialize the input handler with the game logic and UI
    input_handler = InputHandler(game, ui)

    # initialize the input handler in the UI
    ui.input = input_handler

    ui.show_mine_prompt()
    root.mainloop()

if __name__ == "__main__":
    main()
