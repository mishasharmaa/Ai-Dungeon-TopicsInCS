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

def apply_state_changes(state, rules, reply):
    """Parse and apply the model's JSON 'state_change' list."""
    try:
        data = json.loads(reply)
    except json.JSONDecodeError:
        print("Model reply not valid JSON; skipping state update.")
        return state, False  # treat as failed

    # if no state change, count as fail
    if len(data.get("state_change", [])) == 0:
        return state, False

    success = True

    for change in data["state_change"]:
        if change.startswith("add_item:"):
            item = change.split(":")[1]
            if len(state["inventory"]) < rules["INVENTORY_LIMIT"]:
                if item not in state["inventory"]:
                    state["inventory"].append(item)
                    print(f"Added '{item}' to inventory.")
                else:
                    print(f"You already have '{item}'.")
            else:
                print("Inventory full! Cannot take more items.")

        elif change.startswith("set_flag:"):
            flag = change.split(":")[1]
            state.setdefault("flags", {})[flag] = True
            print(f"Flag set: {flag}")

        elif change.startswith("move_to:"):
            loc = change.split(":")[1]
            lock_flag = rules.get("LOCKS", {}).get(loc)
            if lock_flag and not state["flags"].get(lock_flag, False):
                print(f"The path to {loc} is locked. You need {lock_flag}.")
                success = False
            else:
                state["location"] = loc
                print(f"You moved to {loc}.")

        elif change.startswith("hp_delta:"):
            try:
                delta = int(change.split(":")[1])
                state["hp"] += delta
                print(f"HP changed by {delta}. Current HP: {state['hp']}")
                if state["hp"] <= 0:
                    state["flags"]["hp_zero"] = True
            except ValueError:
                pass

    return state, success

def main():
    rules = load_rules()
    state = load_state(rules["START"])
    print(rules["QUEST"]["intro"])

    turns = 0
    failed_attempts = 0

    while True:
        print(f"\nLocation: {state['location']}")
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
        if cmd not in rules["COMMANDS"]:
            print("Invalid command. Type 'help' for options.")
            failed_attempts += 1
        else:
            turns += 1
            user_prompt = json.dumps({
                "state": state,
                "rules": rules,
                "command": cmd
            }, indent=2)

            reply = call_llm(user_prompt)
            print("\nNarration:")
            print(reply)

            # apply and track success/fail
            state, success = apply_state_changes(state, rules, reply)
            if not success:
                failed_attempts += 1

            append_transcript(f"Player: {cmd}\nModel: {reply}")

        # lose after 3 failed attempts
        if failed_attempts >= 3:
            state["flags"]["hp_zero"] = True
            print("You kept attempting actions that failed. Time runs out, and your journey ends in silence.")
            break

        # check end conditions
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
