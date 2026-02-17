# 2048 Game (Python + Tkinter)

A Python implementation of the popular 2048 puzzle game, featuring a simple GUI built with the Tkinter library.

## Features

- Classic 2048 gameplay
- Different levels of difficulty (Gameboard size|value which ends game)
  - 3x3|128
  - 4x4|1024
  - 4x4|2048 (standard game)
  - 5x5|2048
  - 6x6|4096
- Interactive graphical user interface (GUI) using Tkinter
- Keyboard controls for smooth play
- Previous scores and records tracking
- Lightweight and easy to run

## Screenshots

![img.png](images/readme_main_menu.png)\
*Main menu of the game*

![img.png](images/readme_gameboard_1.png)\
*The gameboard of the easiest level*

![img.png](images/readme_gameboard_5.png)\
*The gameboard of the hardest level*

## Getting Started

### Prerequisites

- Python 3.x
- Everything included in `reqirements.txt` file
```bash
# installation of the required packages
pip install -r requirements.txt
```

Tkinter is included with most Python installations. If you encounter issues, you may need to install it separately:

```bash
# For Ubuntu/Debian
sudo apt-get install python3-tk

# For MacOS/Homebrew
brew install python-tk
```

### Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/xxNauty/2048-game.git
    cd 2048-game
    ```

2. **Run the game**
    ```bash
    python main.py
    ```

## How to Play

- **Use arrow keys** (or **W S A D**) to move the tiles.
- When two tiles with the same number touch, they merge into one with the value of their sum.
- The game goal is to reach the tile with required number (which for default settings is **2048**).
- The game fails if there is no room for any move before reaching required value.

## Project Structure

```
├── backend             # holds actual game logic
├── gui                 # responsible for everything you see on the screen
├── logs                # informations about last 8 games played
├── records             # stores informations about your personal records
├── game_settings.json  # the file which stores informations about the levels of the game
└── main.py             # the main file of the game
```

## License

This project is licensed under the "Unlicensed license".