# ----- game_logic.py -----
from board_manager import BoardManager

class GameLogic:
    def __init__(self, board_manager: BoardManager):
        self.board = board_manager
        self.total_mines = 10
        self.flags = 0
        self.game_over = False
        self.victory = False

    def start_game(self, mine_count, safe_cell=None):
        self.total_mines = mine_count
        self.flags = 0
        self.game_over = False
        self.victory = False
        self.board.initialize_board(mine_count, safe_cell)

    def toggle_flag(self, row, col):
        cell = self.board.get_cell(row, col)
        if cell['is_flagged']:
            cell['is_flagged'] = False
            self.flags -= 1
        else:
            if self.flags < self.total_mines:
                cell['is_flagged'] = True
                self.flags += 1


    def reveal_cell(self, row, col):
        if self.game_over:
            return
        cell = self.board.get_cell(row, col)
        if cell['is_flagged'] or not cell['is_covered']:
            return
        cell['is_covered'] = False

        if cell['is_mine']:
            self.game_over = True
            self.victory = False
            return

        if cell['adjacent'] == 0:
            for nr in range(row-1, row+2):
                for nc in range(col-1, col+2):
                    if 0 <= nr < self.board.size and 0 <= nc < self.board.size:
                        if self.board.get_cell(nr, nc)['is_covered']:
                            self.reveal_cell(nr, nc)
        self.check_victory()

    def check_victory(self):
        for r in range(self.board.size):
            for c in range(self.board.size):
                cell = self.board.get_cell(r, c)
                if not cell['is_mine'] and cell['is_covered']:
                    return
        self.victory = True
        self.game_over = True
