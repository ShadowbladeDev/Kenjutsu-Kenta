import random
import time
import json

# Splash screen animation
def splash_screen():
    print("⚔️ Kenjutsu Kenta ⚔️")
    for c in "A samurai adventure begins...":
        print(c, end='', flush=True)
        time.sleep(0.05)
    print("\n")

# Player setup
player = {
    "name": "",
    "class": "",
    "health": 100,
    "inventory": [],
    "location": "dojo",
    "quests": {"Find the Hidden Cave": False},
    "position": [0, 0]  # x, y coordinates
}

# Character classes
classes = {
    "Samurai": {"health": 120, "bonus": "defense"},
    "Ninja": {"health": 90, "bonus": "speed"},
    "Ronin": {"health": 100, "bonus": "attack"}
}

# Terrain map
terrain_map = {
    (0, 0): "dojo",
    (1, 0): "village",
    (2, 1): "forest",
    (3, 2): "cave"
}

# Locations and actions
locations = {
    "dojo": {"description": "You stand in the quiet dojo. Your master awaits.", "actions": ["train", "leave", "save"]},
    "forest": {"description": "The forest is dense and mysterious. Danger lurks.", "actions": ["explore", "return"]},
    "village": {"description": "The village is peaceful. You hear whispers of bandits.", "actions": ["talk", "return"]},
    "cave": {"description": "You found the hidden cave. A boss awaits!", "actions": ["fight_boss", "return"]}
}

# Game functions
def choose_class():
    print("Choose your class:")
    for c in classes:
        print(f"- {c}: {classes[c]['bonus']} bonus")
    choice = input("Class: ").title()
    if choice in classes:
        player["class"] = choice
        player["health"] = classes[choice]["health"]
        print(f"You are now a {choice} with {player['health']} health.")
    else:
        print("Invalid class. Defaulting to Ronin.")
        player["class"] = "Ronin"

def train():
    print("You train with your master. Your skills improve.")
    if "katana" not in player["inventory"]:
        player["inventory"].append("katana")
        print("You received a katana!")

def explore():
    print("You explore the forest...")
    if not player["quests"]["Find the Hidden Cave"]:
        print("You discover a hidden path to a cave!")
        player["quests"]["Find the Hidden Cave"] = True
        locations["forest"]["actions"].append("enter cave")
    else:
        encounter = random.choice(["bandit", "scroll", "nothing"])
        if encounter == "bandit":
            print("A bandit attacks!")
            fight()
        elif encounter == "scroll":
            print("You found a magic scroll!")
            player["inventory"].append("scroll")
        else:
            print("The forest is calm today.")

def talk():
    print("Villagers speak of a hidden cave in the forest.")

def fight():
    if "katana" in player["inventory"]:
        print("You fight bravely and defeat the bandit!")
    else:
        print("You have no weapon! You lose 20 health.")
        player["health"] -= 20

def fight_boss():
    print("You face the Shadow Ronin!")
    if "katana" in player["inventory"]:
        print("With your katana, you defeat the Shadow Ronin! Quest complete.")
        player["quests"]["Find the Hidden Cave"] = "Completed"
    else:
        print("You are unarmed and fall in battle.")
        player["health"] = 0

def move(location):
    if location in locations:
        player["location"] = location
        print(locations[location]["description"])
    else:
        print("You can't go there.")

def save_game():
    with open("savefile.json", "w") as f:
        json.dump(player, f)
    print("Game saved!")

def load_game():
    try:
        with open("savefile.json", "r") as f:
            data = json.load(f)
            player.update(data)
        print("Game loaded!")
    except FileNotFoundError:
        print("No save file found.")

def use_scroll():
    if "scroll" in player["inventory"]:
        print("You use a magic scroll and restore 30 health!")
        player["health"] = min(player["health"] + 30, classes[player["class"]]["health"])
        player["inventory"].remove("scroll")
    else:
        print("You have no scrolls.")

def move_3d():
    print(f"Current position: {player['position']}")
    direction = input("Move (north/south/east/west): ").lower()
    x, y = player["position"]
    if direction == "north" and y < 4:
        y += 1
    elif direction == "south" and y > 0:
        y -= 1
    elif direction == "east" and x < 4:
        x += 1
    elif direction == "west" and x > 0:
        x -= 1
    else:
        print("You can't move that way.")
        return
    player["position"] = [x, y]
    print(f"New position: {player['position']}")

    # Terrain event
    terrain = terrain_map.get((x, y), "wilderness")
    print(f"You arrive at: {terrain}")
    if terrain == "forest":
        explore()
    elif terrain == "village":
        talk()
    elif terrain == "cave":
        if player["quests"]["Find the Hidden Cave"]:
            fight_boss()
        else:
            print("The cave is sealed by magic.")
    elif terrain == "dojo":
        train()
    else:
        if random.random() < 0.3:
            print("A rogue enemy patrol spots you!")
            fight()

def show_map():
    x, y = player["position"]
    print("\n🗺️ Map:")
    for j in range(4, -1, -1):
        row = ""
        for i in range(5):
            if [i, j] == [x, y]:
                row += "🧍 "
            elif (i, j) in terrain_map:
                row += "🏯 "
            else:
                row += "⬜ "
        print(row)
    print("⬜ = empty space, 🧍 = you, 🏯 = location\n")

def game_loop():
    splash_screen()
    choice = input("Load previous game? (yes/no): ").lower()
    if choice == "yes":
        load_game()
    else:
        player["name"] = input("Enter your samurai name: ")
        choose_class()

    while player["health"] > 0:
        loc = player["location"]
        print(f"\nYou are at the {loc}.")
        print("Available actions:", locations[loc]["actions"] + ["move_3d", "use_scroll", "show_map"])
        action = input("What will you do? ").lower()

        if loc == "dojo":
            if action == "train":
                train()
            elif action == "leave":
                move("forest")
            elif action == "save":
                save_game()
        elif loc == "forest":
            if action == "explore":
                explore()
            elif action == "return":
                move("dojo")
            elif action == "enter cave" and player["quests"]["Find the Hidden Cave"]:
                move("cave")
        elif loc == "village":
            if action == "talk":
                talk()
            elif action == "return":
                move("dojo")
        elif loc == "cave":
            if action == "fight_boss":
                fight_boss()
            elif action == "return":
                move("forest")

        if action == "move_3d":
            move_3d()
        elif action == "use_scroll":
            use_scroll()
        elif action == "show_map":
            show_map()

    print("You have fallen in battle. Game over.")

# Start the game
game_loop()
