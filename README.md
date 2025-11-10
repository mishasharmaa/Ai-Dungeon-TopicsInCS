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

---

### Example Session 

The village elder begs you to recover the stolen Crown.

Location: Village Square
> talk elder

Narration:
{
  "narration": "The village elder, a weathered man with eyes that hold the weight of centuries, steps forward. 'The Crown has been stolen by shadowy figures from the west,' he begins, his voice low but urgent. 'To restore peace, you must find the key hidden in the village well and unlock the Ancient Gate. Only then can you retrieve the Crown.'",
  "state_change": []
}

Location: Village Square
> look well

Narration:
{
  "narration": "An old stone well stands in the center of the Village Square, its rusted iron cover broken and loose. The murky water inside reflects the sky faintly, and you notice a small indentation at the bottom that might hold something.",
  "state_change": []
}

Location: Village Square
> search well

Narration:
{
  "narration": "You carefully search the old stone well in the village square. After a moment, your fingers brush against a small iron key hidden beneath the moss. You pull it free and hold it in your hand.",
  "state_change": ["add_item:key"]
}
🧺 Added 'key' to inventory.

Location: Village Square
> inventory
Inventory: ['key']

Location: Village Square
> use key

Narration:
{
  "narration": "You unlock the Ancient Gate with the key. The gate creaks open, revealing a path into the forest.",
  "state_change": [
    "set_flag:have_key"
  ]
}
Flag set: have_key

Location: Village Square
> move gate

Narration:
{
  "narration": "You approach the Ancient Gate, which is now unlocked by the key you carry.",
  "state_change": ["move_to:forest"]
}
You moved to forest.

Location: forest
> look around

Narration:
{
  "narration": "You step into the forest clearing and see an ancient stone altar. On the altar sits a golden crown, its intricate design catching the sunlight.",
  "state_change": []
}

Location: forest
> take crown

Narration:
{
  "narration": "You pick up the ancient Crown from the forest floor. The quest to recover the stolen Crown is complete!",
  "state_change": [
    "set_flag:crown_found"
  ]
}

Flag set: crown_found
You completed the quest!
