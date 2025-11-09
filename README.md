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

| Command | What it Does | 
|---|---|
| look around | See what’s in your area (Village Square, forest, etc.) | 
| look well | Inspect the well closely | 
| talk elder | Speak to the village elder for clues | 
| search well | Search the well to find the hidden key | 
| take key | Pick up the key once it’s found | 
| use key | Use the key to unlock the Ancient Gate | 
| move gate | Move toward or open the gate | 
| move forest | Enter the forest beyond the gate |  
| take crown | Pick up the Crown to win the quest | 
| inventory | View your collected items |
| help | See all available commands |
| save | Save your progress | 
| load | Load your saved game | 
| quit | Exit the game |

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
#### To Change Quest 

Edit "goal_flag" and "name" under "QUEST"

#### To Add A Lock 

"LOCKS": { "Castle Door": "have_silver_key" }

#### To Add A Command

Add to "COMMANDS" list, e.g. "attack <enemy>"

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
