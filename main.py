import json
import os
from ollama import chat, ChatResponse

SAVE_FILE = "save.json"
TRANSCRIPT_FILE = "samples/transcript.txt"

def load_rules():
    with open("rules.json", "r") as f:
        return json.load(f)

def save_state(state):
    with open(SAVE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def load_state(start_state):
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return start_state.copy()

def append_transcript(entry):
    os.makedirs("samples", exist_ok=True)
    with open(TRANSCRIPT_FILE, "a") as f:
        f.write(entry + "\n\n")

def call_llm(prompt, model="qwen3:4b"):
    """Send prompt to local Ollama model and return text."""
    response: ChatResponse = chat(
        model=model,
        messages=[
            {"role": "system", "content": open("prompts/gm.txt").read()},
            {"role": "user", "content": prompt}
        ]
    )
    return response["message"]["content"]

def main():
    rules = load_rules()
    state = load_state(rules["START"])
    print(rules["QUEST"]["intro"])

    turns = 0
    while True:
        print(f"\n Location: {state['location']}")
        cmd = input("> ").strip()

        # built-in commands
        if cmd == "help":
            print("Commands:", ", ".join(rules["COMMANDS"]))
            continue
        if cmd == "inventory":
            print("Inventory:", state["inventory"])
            continue
        if cmd == "save":
            save_state(state)
            print("Game saved.")
            continue
        if cmd == "load":
            state = load_state(rules["START"])
            print("Game loaded.")
            continue
        if cmd == "quit":
            print("Goodbye!")
            break

        # invalid command handling
        if not any(cmd.startswith(c.split(" ")[0]) for c in rules["COMMANDS"]):
            print("Invalid command. Type 'help' for options.")
            continue

        turns += 1
        user_prompt = json.dumps({
            "state": state,
            "rules": rules,
            "command": cmd
        }, indent=2)

        # call the model
        reply = call_llm(user_prompt)
        print("\n Narration:")
        print(reply)

        # record the exchange
        append_transcript(f"Player: {cmd}\nModel: {reply}")

        # end conditions
        if turns >= rules["END_CONDITIONS"]["MAX_TURNS"]:
            print("You ran out of turns. Game over!")
            break
        if "hp_zero" in state.get("flags", {}):
            print("You lost all health. Game over!")
            break
        if all(flag in state.get("flags", {}) for flag in rules["END_CONDITIONS"]["WIN_ALL_FLAGS"]):
            print("You completed the quest!")
            break

if __name__ == "__main__":
    main()
