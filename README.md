# AI Dungeon Game

Welcome! This game walks you through a short text adventure game powered by a local LLM, via Ollama, where a user has to retrieve the stolen crown. It is governed by a 'rules.json' file that enforces legal moves, locks, and win/lose conditions. Have fun!

--- 

### Installation and Running

1. Install Ollama (if not already) and run it

    - brew install ollama 
    - ollama serve 
    - ollama pull qwen3:4b

2. Create and Activate Virtual Environment

    - source venv/bin/activate 

3. Install Dependencies 

    - pip install ollama

4. Run game

    - python3 main.py

--- 

### Available Commands 

I have implemented several commands that a user can type to play the game. Below are the commands: 

| Command | What it Does | Usage |
|---|---|---|
| look | describes your surroundings | look |
| move <place> | travel to another location, if unlocked | move forest, move gate |
| take <item> | describes your surroundings | look |
