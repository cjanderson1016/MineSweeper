"""
File Name: board_manager.py

Description: File that defines the Cell class, which represents individual cells on the board, and the BoardManager class.
BoardManager handles board initialization, random mine placement, adjacent mine calculations, cell access, and board resets. 


All Collaborators: Group 4, ChatGPT

Other sources for code: ChatGPT

Date Created: 8/29/2025

Last Updated: 9/16/2025
"""
# ----- board_manager.py -----
import random

# Class representing an individual cell. The minesweeper board is a 10x10 grid of these cells.
# Source: Original work
class Cell:
    def __init__(self, is_mine = False, is_covered = True, is_flagged = False, adjacent = 0):
        self.is_mine = is_mine
        self.is_covered = is_covered
        self.is_flagged = False
        self.adjacent = adjacent

class BoardManager:
    # Source: ChatGPT
    def __init__(self, size=10):
        #Intialize the board variables and size
        self.size = size
        self.board = []
        self.mines = set()

    # Source: Original work combined with ChatGPT
    def initialize_board(self, mine_count, safe_cell=None):
        # Populate the board with cells and place mines
        self.board = [[Cell()
                       for _ in range(self.size)] for _ in range(self.size)] #Create a 2d array of default cell objects
        self.place_mines(mine_count, safe_cell) #Place mines on the board
        self.calculate_adjacent_counts() #Calculate adjacent mine counts for each cell

    # Source: ChatGPT
    def place_mines(self, mine_count, safe_cell=None):
        # Randomly place mines on the board, avoiding the safe_cell if provided
        positions = [(r, c) for r in range(self.size) for c in range(self.size)] #List of all possible positions
        if safe_cell and safe_cell in positions:
            positions.remove(safe_cell)#Remove the safe cell from possible mine positions
        self.mines = set(random.sample(positions, mine_count)) #Randomly select mine positions
        for r, c in self.mines: #For each randomly selected position
            self.board[r][c].is_mine = True #Mark the cell as a mine

    # Source: ChatGPT
    def calculate_adjacent_counts(self):
        # Calculate the number of adjacent mines for each cell
        # Iterate through each cell in the board
        for r in range(self.size): 
            for c in range(self.size):
                if self.board[r][c].is_mine:
                    continue #Skip if the cell is a mine
                self.board[r][c].adjacent = sum(
                    1 for nr in range(r-1, r+2) 
                    for nc in range(c-1, c+2)
                    if 0 <= nr < self.size and 0 <= nc < self.size and self.board[nr][nc].is_mine #Count adjacent mines
                )

    # Source: ChatGPT
    def get_cell(self, row, col):
        # Return the cell dictionary at the specified position
        return self.board[row][col]

    # Source: ChatGPT
    def reset_board(self):
        # Reset the board to an empty state
        self.board = []
        self.mines.clear()
