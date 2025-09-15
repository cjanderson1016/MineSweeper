# Minesweeper Game

A classic Minesweeper game implementation built with Python and Tkinter GUI. This project features a modular architecture with separate components for game logic, board management, user interface, and input handling.

The game board consists of cells that may contain mines or numbers indicating how many mines are adjacent to that cell.

## How to Run

### Prerequisites
- Python 3.x installed on your system
- Tkinter (usually included with Python)

### Running the Game
1. Clone or download this repository
2. Navigate to the project directory
3. Run the main file:
   ```bash
   python main.py
   ```

## 🎯 How to Play

### Game Setup
1. **Choose Difficulty**: When the game starts, you'll see a prompt to enter the number of mines (10-20)
2. **Start Game**: Click "Start Game" or press Enter to begin
3. **First Click Safety**: Your first click is always safe - no mine will be placed there

### Game Controls
- **Left Click**: Reveal a cell
- **Right Click**: Place/remove a flag on a cell
- **F11**: Toggle fullscreen mode
- **Escape**: Exit fullscreen mode
- **Enter**: Start the game (when entering mine count)

### Game Rules
1. **Objective**: Reveal all cells that don't contain mines
2. **Numbers**: Each revealed cell shows a number indicating how many mines are in the 8 adjacent cells
3. **Flags**: Use flags (🚩) to mark cells you suspect contain mines
4. **Auto-Reveal**: Clicking on a cell with no adjacent mines automatically reveals all connected empty cells
5. **Game Over**: Clicking on a mine (💣) ends the game
6. **Victory**: Reveal all non-mine cells to win

### Game Features
- **Dynamic Board**: 10x10 grid with customizable mine count (10-20 mines)
- **Smart First Click**: Your first click is always safe
- **Flag Management**: Limited flags equal to the number of mines
- **Visual Feedback**: 
  - Numbers show adjacent mine count
  - Flags mark suspected mines
  - Mines show as bombs when revealed
  - Empty cells are automatically revealed
- **Replay Options**: After winning or losing, choose to play again with same settings or new mine count

## Project Architecture

The project is organized into modular components:

### Core Files
- **`main.py`**: Entry point that initializes all components and starts the GUI
- **`board_manager.py`**: Manages the game board, mine placement, and cell calculations
- **`game_logic.py`**: Handles game rules, cell revealing, flag management, and victory conditions
- **`input_handler.py`**: Processes user input (clicks) and coordinates between game logic and UI
- **`user_interface.py`**: Creates and manages the Tkinter GUI, displays the game board

### Key Features
- **Modular Design**: Clean separation of concerns between game logic, UI, and input handling
- **Object-Oriented**: Each component is a well-defined class with specific responsibilities
- **Event-Driven**: Uses Tkinter's event system for responsive user interaction
- **State Management**: Tracks game state, flags, mines, and victory conditions

## User Interface

The game features a clean, intuitive interface:
- **Grid Layout**: 10x10 board with labeled rows (1-10) and columns (A-J)
- **Status Bar**: Shows current game state and remaining flags
- **Mine Counter**: Displays total mines and flags remaining
- **Responsive Design**: Buttons resize automatically in fullscreen mode
- **Game Over Dialog**: Options to replay with same settings, choose new settings, or quit

## Game Mechanics

### Mine Placement
- Mines are randomly distributed across the board
- Your first click is guaranteed to be safe
- Mine count ranges from 10-20 for balanced gameplay

### Cell States
- **Covered**: Default state, clickable
- **Revealed**: Shows number or is empty
- **Flagged**: Marked with 🚩, cannot be revealed
- **Mine**: Shows 💣 when revealed

### Victory Conditions
- **Win**: All non-mine cells are revealed
- **Lose**: Click on a mine

## Technical Details

### Dependencies
- `tkinter`: Built-in Python GUI library
- `random`: For mine placement
- `messagebox`: For game over dialogs

### System Requirements
- Python 3.x
- Tkinter support (included with most Python installations)
- Any operating system that supports Python and Tkinter

