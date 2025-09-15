# ----- input_handler.py -----

class InputHandler:
    def __init__(self, game_logic, ui):
        # Store reference to the game logic instance for making game state changes
        self.game = game_logic
        # Store reference to the user interface instance for updating the display
        self.ui = ui

    def handle_left_click(self, row, col):
        # Tell the game logic to reveal the clicked cell
        self.game.reveal_cell(row, col)
        # Update the visual board display's new state
        self.ui.update_board()
        # Check for victory or loss condition
        if self.game.game_over:

            # Pass victory status (true/false)
            self.ui.show_game_over(self.game.victory)

    def handle_right_click(self, row, col):
        # Don't try to flag an uncovered cell or if the game is over
        if self.game.game_over:
            return
        cell = self.game.board.get_cell(row, col) # get the cell that was clicked
        # Ignore attempts to flag uncovered cells
        if not cell['is_covered']:
            return

        changed = self.game.toggle_flag(row, col) # toggle the flag and store if it was toggled
        # if the flag was toggled, update the board
        if changed:
            self.ui.update_board()