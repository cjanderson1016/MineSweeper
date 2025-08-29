import tkinter as tk
from tkinter import messagebox
import random

class MinesweeperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")
        self.root.resizable(False, False)

        # Constants
        self.rows, self.cols = 10, 10

        # Game state
        self.total_mines = 10
        self.buttons = []
        self.mines = set()
        self.flags = set()
        self.first_click = True
        self.game_over = False

        # Header (mine selection prompt)
        self.header_frame = tk.Frame(self.root)
        self.mine_label = tk.Label(self.header_frame, text="Enter number of mines (10–20):")
        self.mine_entry = tk.Entry(self.header_frame, width=5)
        self.mine_entry.insert(0, "10")
        self.start_button = tk.Button(self.header_frame, text="Start Game", command=self.start_game)

        # Layout header initially (only before start or when choosing mines)
        self.header_frame.pack(pady=5)
        self.mine_label.pack(side=tk.LEFT)
        self.mine_entry.pack(side=tk.LEFT)
        self.start_button.pack(side=tk.LEFT, padx=5)

        # Status
        self.status_label = tk.Label(self.root, text="Set mines and click Start Game", font=("Arial", 12))
        self.status_label.pack(pady=5)

        # Grid area
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(padx=10, pady=10)

    # -------------------- UI Helpers --------------------
    def show_mine_prompt(self, default_same=None):
        """Show the mine selection prompt. Optionally prefill if default_same provided."""
        if default_same is not None:
            self.mine_entry.delete(0, tk.END)
            self.mine_entry.insert(0, str(default_same))
        if not self.header_frame.winfo_ismapped():
            self.header_frame.pack(pady=5)
            self.mine_label.pack(side=tk.LEFT)
            self.mine_entry.pack(side=tk.LEFT)
            self.start_button.pack(side=tk.LEFT, padx=5)
        self.status_label.config(text="Choose mines and press Start Game")

    def hide_mine_prompt(self):
        self.start_button.pack_forget()
        self.mine_entry.pack_forget()
        self.mine_label.pack_forget()
        self.header_frame.pack_forget()

    def clear_board_widgets(self):
        for w in self.grid_frame.winfo_children():
            w.destroy()
        self.buttons = []

    # -------------------- Game Setup --------------------
    def start_game(self):
        # Validate mine count
        try:
            mines = int(self.mine_entry.get())
            if not 10 <= mines <= 20:
                raise ValueError
            self.total_mines = mines
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a number between 10 and 20.")
            return

        # Reset state
        self.hide_mine_prompt()
        self.reset_state()
        self.build_board()
        self.status_label.config(text=f"Game in progress — Mines: {self.total_mines} | Flags remaining: {self.total_mines}")

    def reset_state(self):
        self.mines.clear()
        self.flags.clear()
        self.first_click = True
        self.game_over = False
        self.clear_board_widgets()

    def build_board(self):
        # Column headers A–J
        tk.Label(self.grid_frame, text="").grid(row=0, column=0)
        for c in range(self.cols):
            tk.Label(self.grid_frame, text=chr(65+c), font=("Arial", 10, "bold")).grid(row=0, column=c+1)
        # Rows
        for r in range(self.rows):
            tk.Label(self.grid_frame, text=str(r+1), font=("Arial", 10, "bold")).grid(row=r+1, column=0)
            row_btns = []
            for c in range(self.cols):
                btn = tk.Button(self.grid_frame, width=3, height=1,
                                command=lambda r=r, c=c: self.on_left_click(r, c))
                btn.grid(row=r+1, column=c+1)
                # Right-click bindings (include Button-2 for macOS trackpads)
                btn.bind("<Button-3>", lambda e, r=r, c=c: self.on_right_click(r, c))
                btn.bind("<Button-2>", lambda e, r=r, c=c: self.on_right_click(r, c))
                row_btns.append(btn)
            self.buttons.append(row_btns)

    def place_mines(self, safe_r, safe_c):
        while len(self.mines) < self.total_mines:
            r, c = random.randint(0, self.rows-1), random.randint(0, self.cols-1)
            if (r, c) != (safe_r, safe_c):
                self.mines.add((r, c))

    # -------------------- Event Handlers --------------------
    def on_left_click(self, r, c):
        if self.game_over or (r, c) in self.flags:
            return
        if self.first_click:
            self.place_mines(r, c)
            self.first_click = False
        if (r, c) in self.mines:
            self.reveal_mines()
            self.game_over = True
            self.status_label.config(text="Game Over 💥 — Choose an option")
            self.restart_dialog()
            return
        self.reveal_cell(r, c)
        if self.check_win():
            self.game_over = True
            self.status_label.config(text="You Win 🎉 — Choose an option")
            self.restart_dialog()
        else:
            self.status_label.config(text=f"Game in progress — Mines: {self.total_mines} | Flags remaining: {self.total_mines - len(self.flags)}")

    def on_right_click(self, r, c):
        if self.game_over:
            return
        btn = self.buttons[r][c]
        if btn["state"] != "normal":
            return
        if (r, c) in self.flags:
            self.flags.remove((r, c))
            btn.config(text="")
        else:
            if len(self.flags) < self.total_mines:
                self.flags.add((r, c))
                btn.config(text="🚩")
        self.status_label.config(text=f"Game in progress — Mines: {self.total_mines} | Flags remaining: {self.total_mines - len(self.flags)}")

    # -------------------- Reveal Logic --------------------
    def reveal_cell(self, r, c):
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return
        btn = self.buttons[r][c]
        if btn["state"] != "normal":
            return
        btn.config(state="disabled", relief=tk.SUNKEN)
        adj = self.adjacent_mine_count(r, c)
        if adj > 0:
            btn.config(text=str(adj))
        else:
            for rr in range(r-1, r+2):
                for cc in range(c-1, c+2):
                    if (rr, cc) != (r, c):
                        self.reveal_cell(rr, cc)

    def adjacent_mine_count(self, r, c):
        count = 0
        for rr in range(r-1, r+2):
            for cc in range(c-1, c+2):
                if 0 <= rr < self.rows and 0 <= cc < self.cols:
                    if (rr, cc) in self.mines and not (rr == r and cc == c):
                        count += 1
        return count

    def reveal_mines(self):
        for (r, c) in self.mines:
            btn = self.buttons[r][c]
            btn.config(text="💣", state="disabled", disabledforeground="red")

    def check_win(self):
        # Win if all non-mine cells are disabled
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) not in self.mines and self.buttons[r][c]["state"] == "normal":
                    return False
        return True

    # -------------------- Restart Dialog --------------------
    def restart_dialog(self):
        dlg = tk.Toplevel(self.root)
        dlg.title("Play Again?")
        dlg.transient(self.root)
        dlg.grab_set()
        tk.Label(dlg, text="Choose an option:").pack(padx=15, pady=10)

        def same_mines():
            dlg.destroy()
            # Immediate restart with same mine count
            self.hide_mine_prompt()
            self.reset_state()
            self.build_board()
            self.status_label.config(text=f"New game started with {self.total_mines} mines — Good luck!")

        def choose_mines():
            dlg.destroy()
            # Remove board and show prompt to choose mines
            self.reset_state()
            self.show_mine_prompt(default_same=self.total_mines)
            self.status_label.config(text="Choose mines and press Start Game")

        def quit_game():
            dlg.destroy()
            self.root.quit()

        btn_frame = tk.Frame(dlg)
        btn_frame.pack(padx=10, pady=10)
        tk.Button(btn_frame, text="Play Again (Same Mines)", command=same_mines).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Play Again (Choose Mines)", command=choose_mines).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Quit", command=quit_game).pack(side=tk.LEFT, padx=5)

        dlg.wait_window()


if __name__ == "__main__":
    root = tk.Tk()
    app = MinesweeperGUI(root)
    root.mainloop()