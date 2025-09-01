# ----- game_logic.py-----
"""
File Name: game_logic.py

Description: Handles the player's standard interations with the Minesweeper board. 
    Includes --> 1) Keeping track of mines, 2) Placing flags, 3) Revealing cells, and 4) Victory/game-over states

All Collaborators: Group 4, ChatGPT

Other sources for code: ChatGPT

Date Created: 8/29/2025

Last Updated: 8/29/2025
"""
from board_manager import BoardManager



class GameLogic:
    """
    Principle class that manipluates the Minesweeper board whenever the player interacts with it.

     In the game of Minesweeper, the player interacts with the board by clicking on cells. When a cell is clicked on it is revealed to be: empty, adjacent to a mine, or a mine.
    The player may also put down a flag on an unrevealed cell that they suspect has a mine. If the player clicks on a mine, the game-over state is triggered. The game is won when all 
    cells not containing mines are revealed.
    """

    def __init__(self, board_manager: BoardManager):
        """
        Initializes game logic for the board the player will interact with

        Input: BoardManager class object from board_manager.py

        Output: None
        
        """

        self.board = board_manager # The board the game is played on (2D array)

        self.total_mines = 10 # The number of mines randomly distrbued across the board

        self.flags = 0 # The number of flags placed (amount of flags the player can place = num of total mines)

        self.game_over = False # Sets the game-over state

        self.victory = False # Sets the victory state




    def start_game(self, mine_count, safe_cell=None):
        """
        Function that begins the game

        Input: 1 - Number of mines, 2 - Safe cell

        Output: None
        """

        self.total_mines = mine_count #The user-given number of mines (10 - 20)

        self.flags = 0 # Begin to count of the number of flags the user has placed

        # Variables to keep track of game state
        self.game_over = False
        self.victory = False

        self.board.initialize_board(mine_count, safe_cell) #Create Minesweeper board with the given amount of mines

    def toggle_flag(self, row, col):
        """
        Function called whenever the player places down a flag (right click)

        Input: The x/y coordinates of the cell that the player clicks on 

        Output: None
        
        """


        cell = self.board.get_cell(row, col) # The cell that the player clicked on

        # Check if the cell already has a flag on it. If it does, remove the flag.
        if cell['is_flagged']:
            cell['is_flagged'] = False
            self.flags -= 1 # Remove flag
        
        # If there is no flag on the cell, then check if the player has placed all of their flags. If not, place a flag.
        else:
            if self.flags < self.total_mines:
                cell['is_flagged'] = True
                self.flags += 1 # Add flag


    def reveal_cell(self, row, col):
        """
        Function called whenever the player reveals a cell (left click). Checks if the cell can be revealed, triggers game-over if the player uncovers a mine.
            Automatically reveals any adjecant empty cells.

        Input: The x/y coordinates of the cell that the player clicks on 

        Output: None
        """

        # Once the player gets a game-over, they may no longer play.
        if self.game_over:
            return
        
        cell = self.board.get_cell(row, col) # The cell that the player clicked on

        # A cell may not be revealed if: It has a flag on it, or if it has already been revealed.
        if cell['is_flagged'] or not cell['is_covered']:
            return
        
        # Reveal the cell to the player
        cell['is_covered'] = False

        # If the revealed cell contains a mine, trigger a game-over state
        if cell['is_mine']:
            self.game_over = True
            self.victory = False
            return

        # If the revealed cell has no adjacent mines, recursively reveal all surrounding cells.
        if cell['adjacent'] == 0:
            # Check the 8 surrounding cells (nr = near rows, nc = near columns)
            for nr in range(row-1, row+2):
                for nc in range(col-1, col+2):
                    #if the surrounding cells are within the bound of the board AND are not yet revealed, reveal them to the player.
                    if 0 <= nr < self.board.size and 0 <= nc < self.board.size:
                        if self.board.get_cell(nr, nc)['is_covered']:
                            self.reveal_cell(nr, nc) # Recursive call of reveal_cell function

        self.check_victory() # Check for a victory state after every time a cell is revealed



    def check_victory(self):
        """
        Helper function that checks for victory state.

        Input: None

        Output: None
        """

        # Check every cell on the board. If all of the cells without mines in them are revealed, trigger the victory state and the game is won.
        for r in range(self.board.size):
            for c in range(self.board.size):

                cell = self.board.get_cell(r, c)

                # If a cell which does not have a mine is still revealed, the player has not won the game.
                if not cell['is_mine'] and cell['is_covered']:
                    return
        
        self.victory = True
        self.game_over = True
