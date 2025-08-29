# ----- input_handler.py -----
class InputHandler:
    def __init__(self, game_logic, ui):
        self.game = game_logic
        self.ui = ui

    def handle_left_click(self, row, col):
        self.game.reveal_cell(row, col)
        self.ui.update_board()
        if self.game.game_over:
            self.ui.show_game_over(self.game.victory)

    def handle_right_click(self, row, col):
        self.game.toggle_flag(row, col)
        self.ui.update_board()
