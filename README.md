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
| move place | travel to another location, if unlocked | move forest, move gate |
| take item | pick up an item | take key, take crown |
| talk | talk to a NPC | talk elder |
| inventory | Lists the items you are carrying | inventory |
| help | show all available commands | help |
| save | save progress to save.json | save | 
| load | load previously saved game | load | 
| quit | quit current game | quit |

Any other commands, like "run away" or "attack monster" are invalid. 

---

### JSON File 

This file defines what the world allows, commands, quest structure, and the limits. 

{
  "LOCKS": { "Ancient Gate": "have_key" },
  "QUEST": {
    "name": "Find the Crown",
    "goal_flag": "crown_found"
  },
  "END_CONDITIONS": {
    "WIN_ALL_FLAGS": ["crown_found"],
    "LOSE_ANY_FLAGS": ["hp_zero"],
    "MAX_TURNS": 10
  }
}

--- 

### How to Play 

1. Player enter commands {talk elder}
2. The engine sends commands, rules, and state to the loal model (qwen3:4b)
3. The game replies in JSON with:
   - {
  "narration": "You unlock the gate and step through.",
  "state_change": ["move_to:Forest", "set_flag:have_key"]
    }
4. The narration prints, and legal state changes are enforced
5. The game ends when win or lose conditions are met

---

### File Summary 

| File | Purpose|
|---|---|
| main.py | Game loop with Ollama integration |
| rules.json | Defines rules, commands, quest, locks |
| prompts/gm.txt | Game Master system prompt | 
| samples/transcript.txt | Example play transcript | 
| save.json | Created when player saves progress | 
