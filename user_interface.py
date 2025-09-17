# ----- user_interface.py -----
import tkinter as tk
from tkinter import messagebox

# Number colors
NUMBER_COLORS = {
    1: 'blue',
    2: 'green',
    3: 'red',
    4: 'navy',
    5: 'maroon',
    6: 'teal',
    7: 'purple',
    8: 'darkorange'
}

class UserInterface:
    def __init__(self, root, game_logic, input_handler):
        self.root = root  # Window
        self.game = game_logic  # Game logic
        self.input = input_handler  # Left and right click actions
        self.buttons = []  # Button Widgets
        
        # Header: mine input + start
        self.header_frame = tk.Frame(self.root)
        self.mine_label = tk.Label(self.header_frame, text="Enter number of mines (10-20):", font=("Segoe UI", 11))
        self.mine_entry = tk.Entry(self.header_frame, width=5, font=("Segoe UI", 11))
        self.mine_entry.insert(0, "10")
        self.mine_entry.bind("<Return>", lambda event: self.start_game())  # Bind Enter key to start game
        self.start_button = tk.Button(self.header_frame, text="Start Game", command=self.start_game, font=("Segoe UI", 10, "bold"))
        self.header_frame.pack(pady=5)
        self.mine_label.pack(side=tk.LEFT)
        self.mine_entry.pack(side=tk.LEFT)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        # Bind F11 to toggle fullscreen and Escape to exit fullscreen
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)
        self.root.bind("<Configure>", self.update_size)  # Adjust button sizes on window resize
        self.fullscreen_label = tk.Label(self.root, text="(F11: Fullscreen, Esc: Exit Fullscreen)", font=("Segoe UI", 9))
        self.fullscreen_label.pack(side=tk.BOTTOM, padx=10)

        # Status text
        self.status_label = tk.Label(self.root, text="Set mines and click Start Game", font=("Segoe UI", 12, "bold"))
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
        # Remove any old widgets
        self.clear_board_widgets()

        # Column header from A-J
        tk.Label(self.grid_frame, text="").grid(row=0, column=0)
        for c in range(self.game.board.size):
            tk.Label(self.grid_frame, text=chr(65+c), font=("Segoe UI", 10, "bold")).grid(row=0, column=c+1)
            
        # Row labels and clickable cells
        for r in range(self.game.board.size):
            tk.Label(self.grid_frame, text=str(r+1), font=("Segoe UI", 10, "bold")).grid(row=r+1, column=0)
            row_buttons = []
            for c in range(self.game.board.size):
                btn = tk.Button(self.grid_frame, width=3, height=1, font=("Segoe UI", 10, "bold"),
                                command=lambda r=r, c=c: self.input.handle_left_click(r, c))
                btn.bind("<Button-3>", lambda e, r=r, c=c: self.input.handle_right_click(r, c))
                btn.bind("<Button-2>", lambda e, r=r, c=c: self.input.handle_right_click(r, c))
                btn.grid(row=r+1, column=c+1)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

    def update_size(self, event=None):
        # Adjust button sizes based on window size
        print("Window resized")
        btn_width = 9 if self.root.attributes('-fullscreen') or self.root.wm_state() == "zoomed" else 3
        btn_height = 3 if self.root.attributes('-fullscreen') or self.root.wm_state() == "zoomed" else 1
        font_size = 14 if self.root.attributes('-fullscreen') or self.root.wm_state() == "zoomed" else 10

        # Guard: if buttons not yet built, skip
        if not self.buttons or len(self.buttons) != self.game.board.size or any(len(row) != self.game.board.size for row in self.buttons):
            return

        for r in range(self.game.board.size):
            for c in range(self.game.board.size):
                btn = self.buttons[r][c]
                btn.config(width=btn_width, height=btn_height, font=("Segoe UI", font_size, "bold"))

    def update_board(self):
        # Refresh grid based on the state of the game
        for r in range(self.game.board.size):
            for c in range(self.game.board.size):
                cell = self.game.board.get_cell(r, c)
                btn = self.buttons[r][c]
                if not cell.is_covered:
                    # revealed tile: visually disabled/sunken
                    btn.config(state="disabled", relief=tk.SUNKEN, bg="lightgrey")
                    if cell.is_mine:
                        btn.config(text="💣", disabledforeground="red")
                    elif cell.adjacent > 0:
                        btn.config(text=str(cell.adjacent), disabledforeground=NUMBER_COLORS[cell.adjacent])
                    else:
                        btn.config(text="")
                else:
                    # covered tile
                    btn.config(state="normal", relief=tk.RAISED, bg="SystemButtonFace")
                    if cell.is_flagged:
                        btn.config(text="🚩")
                    else:
                        btn.config(text="")
        
        # Update remaining flags in header
        flags_remaining = self.game.total_mines - self.game.flags
        if not self.game.game_over:
            self.status_label.config(text=f"Game in progress — Mines: {self.game.total_mines} | Flags remaining: {flags_remaining}")
        else:
            # If game_over, leave the status_label to show the result message elsewhere
            pass


    def show_game_over(self, victory):
        # Display win or lose and pop up to replay
        if not victory:
            # Trigger screen shake first, then show dialog after shake completes
            self.boom_feedback_with_dialog()
            return
        
        # For victory, show dialog immediately (no shake needed)
        self._show_game_over_dialog(victory)

    def boom_feedback_with_dialog(self):
        """
        Trigger boom feedback, then show dialog after shake completes.
        """
        self.flash_grid()
        self.shake_window()
        
        # Calculate shake duration: cycles * 4 steps * interval_ms
        shake_duration = 12 * 4 * 16  # ~768ms
        self.root.after(shake_duration + 100, lambda: self._show_game_over_dialog(False))

    def _show_game_over_dialog(self, victory):
        """
        Show the actual game over dialog.
        """
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

    def toggle_fullscreen(self,event=None):
        # Toggle the full-screen mode of the window
        if self.root.attributes('-fullscreen'):
            self.root.attributes('-fullscreen', False)
        else:
            self.root.attributes('-fullscreen', True)

    def exit_fullscreen(self,event=None):
        # Exit full-screen mode and close the window on Escape key press
        self.root.attributes('-fullscreen', False)

    def shake_window(self, cycles=12, amplitude=14, decay=0.85, interval_ms=16):
        """
        Non-blocking window shake. 
        - cycles: how many direction steps (4 steps ≈ 1 full wobble)
        - amplitude: starting pixel offset
        - decay: multiply amplitude each step
        - interval_ms: time between steps (16 ≈ 60fps)
        """
        # If fullscreen, fall back to a flash since geometry wiggle won't show
        try:
            if self.root.attributes('-fullscreen'):
                self.flash_grid()
                return
        except Exception:
            pass

        # Prevent overlapping shakes
        if getattr(self, "_is_shaking", False):
            return
        self._is_shaking = True

        # Snapshot original position and build a small offset pattern
        try:
            orig_x = self.root.winfo_x()
            orig_y = self.root.winfo_y()
        except Exception:
            # If not yet mapped, just skip
            self._is_shaking = False
            return

        # Sequence: right, left, down, up (repeats), with decaying amplitude
        offsets = []
        a = float(amplitude)
        for i in range(cycles):
            offsets.append((+a, 0))
            offsets.append((-a, 0))
            offsets.append((0, +a))
            offsets.append((0, -a))
            a *= decay

        # Apply offsets using .after so we don't block the UI
        def _step(i=0):
            if i >= len(offsets):
                # Restore original position at the very end
                self.root.geometry(f"+{int(orig_x)}+{int(orig_y)}")
                self._is_shaking = False
                return
            dx, dy = offsets[i]
            self.root.geometry(f"+{int(orig_x + dx)}+{int(orig_y + dy)}")
            self.root.after(interval_ms, _step, i + 1)

        _step()

    def flash_grid(self, flash_ms=140):
        """
        Quick red border flash on the grid card—nice for 'boom' and also works in fullscreen.
        """
        if not hasattr(self, "_grid_border_orig"):
            # Store original border color once
            self._grid_border_orig = self.grid_frame.cget("highlightbackground")

        # Flash red
        self.grid_frame.configure(highlightbackground="red", highlightcolor="red")

        def _restore():
            self.grid_frame.configure(highlightbackground=self._grid_border_orig, highlightcolor=self._grid_border_orig)

        self.root.after(flash_ms, _restore)

    def boom_feedback(self):
        """
        Convenience: flash + shake together.
        """
        self.flash_grid()
        self.shake_window()