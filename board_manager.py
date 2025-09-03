# ----- board_manager.py -----
import random

class BoardManager:
    def __init__(self, size=10):
        self.size = size
        self.board = []
        self.mines = set()

    def initialize_board(self, mine_count, safe_cell=None):
        self.board = [[{'is_mine': False, 'is_covered': True, 'is_flagged': False, 'adjacent': 0}
                       for _ in range(self.size)] for _ in range(self.size)]
        self.place_mines(mine_count, safe_cell)
        self.calculate_adjacent_counts()

    def place_mines(self, mine_count, safe_cell=None):
        positions = [(r, c) for r in range(self.size) for c in range(self.size)]
        if safe_cell and safe_cell in positions:
            positions.remove(safe_cell)
        self.mines = set(random.sample(positions, mine_count))
        for r, c in self.mines:
            self.board[r][c]['is_mine'] = True

    def calculate_adjacent_counts(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c]['is_mine']:
                    continue
                self.board[r][c]['adjacent'] = sum(
                    1 for nr in range(r-1, r+2)
                    for nc in range(c-1, c+2)
                    if 0 <= nr < self.size and 0 <= nc < self.size and self.board[nr][nc]['is_mine']
                )

    def get_cell(self, row, col):
        # Return the cell dictionary at the specified position
        return self.board[row][col]

    def reset_board(self):
        self.board = []
        self.mines.clear()
