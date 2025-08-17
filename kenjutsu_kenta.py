Kenjutsu Kenta 
import time

class StatusEffect:
    def __init__(self):
        self.stunned = 0
        self.bleeding = 0
        self.buff_timer = 0
        self.buff_type = None

class Ability:
    def __init__(self, name, damage, cooldown, description, effect=None, duration=0, one_use=False):
        self.name = name
        self.damage = damage
        self.cooldown = cooldown
        self.remaining_cooldown = 0
        self.description = description
        self.effect = effect
        self.duration = duration
        self.one_use = one_use
        self.used = False

    def use(self, user, target):
        if self.remaining_cooldown > 0:
            print(f"{self.name} is on cooldown for {self.remaining_cooldown} more turns.")
            return False
        if self.one_use and self.used:
            print(f"{self.name} can only be used once per round.")
            return False

        if self.effect == "stun":
            target.status.stunned = self.duration
            print(f"{target.name} is stunned for {self.duration} turns!")
        elif self.effect == "bleed":
            target.status.bleeding = self.duration
            print(f"{target.name} is bleeding for {self.duration} turns!")
        elif self.effect == "buff":
            user.status.buff_timer = self.duration
            user.status.buff_type = self.name
            print(f"{user.name} is buffed by {self.name} for {self.duration} turns!")
        elif self.effect == "regen":
            user.status.buff_timer = self.duration
            user.status.buff_type = "regen"
            print(f"{user.name} will regenerate 50 HP every turn for {self.duration} turns!")

        actual_damage = int(self.damage * (user.atk / (user.atk + target.df)))
        target.hp = max(target.hp - actual_damage, 0)
        print(f"{user.name} uses {self.name} on {target.name} for {actual_damage} damage!")

        self.remaining_cooldown = self.cooldown
        if self.one_use:
            self.used = True
        return True

    def tick(self):
        if self.remaining_cooldown > 0:
            self.remaining_cooldown -= 1

class Character:
    def __init__(self, name, hp, atk, df, abilities):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.atk = atk
        self.df = df
        self.abilities = abilities
        self.status = StatusEffect()
        self.hp_stack = 0

    def is_alive(self):
        return self.hp > 0

    def tick_effects(self):
        if self.status.stunned > 0:
            self.status.stunned -= 1
        if self.status.bleeding > 0:
            bleed_damage = 150
            self.hp = max(self.hp - bleed_damage, 0)
            print(f"{self.name} takes {bleed_damage} bleed damage!")
            self.status.bleeding -= 1
        if self.status.buff_timer > 0:
            if self.status.buff_type == "regen":
                heal = 50
                if self.hp < self.max_hp:
                    self.hp = min(self.hp + heal, self.max_hp)
                    print(f"{self.name} regenerates {heal} HP!")
            self.status.buff_timer -= 1

    def tick_cooldowns(self):
        for ability in self.abilities:
            ability.tick()

    def show_status(self):
        bar = "▓" * int((self.hp / self.max_hp) * 20)
        print(f"{self.name} HP: [{bar:<20}] {self.hp}/{self.max_hp}")

    def show_abilities(self):
        for i, ab in enumerate(self.abilities):
            status = f"(Cooldown: {ab.remaining_cooldown})" if ab.remaining_cooldown > 0 else "(Ready)"
            print(f"{i+1}. {ab.name} {status} - {ab.description}")
def define_characters():
    tank_abilities = [
        Ability("Shield Charge", 250, 3, "Stuns for 3s", effect="stun", duration=1),
        Ability("Rocket Punch", 250, 4, "Knocks back"),
        Ability("Rocket Throw", 500, 5, "Throws rocket"),
        Ability("Rocket Barrage", 1250, 10, "Launches 5 rockets at 250 each")
    ]
    ninja_abilities = [
        Ability("Stun Grenade / Smoke Bomb", 0, 2, "Stuns or disappears", effect="stun", duration=1),
        Ability("Blade Slash", 250, 3, "Dual sword slash"),
        Ability("Deep Cut", 150, 5, "Bleeds for 5s", effect="bleed", duration=5),
        Ability("Void Slash", 2500, 10, "Massive void slash")
    ]
    voidling_abilities = [
        Ability("Transcending", 0, 4, "Boosts all stats x10 for 5s", effect="buff", duration=5),
        Ability("Void Dash", 250, 5, "Void blade dash"),
        Ability("Dead Cold", 0, 10, "+1000 DF, +50 ATK for 10s", effect="buff", duration=10),
        Ability("Ancestral Bond", 9999, 99, "One-tap blood strike", one_use=True)
    ]
    medic_abilities = [
        Ability("Regeneration", 0, 2, "Regens 50 HP every turn for 5s", effect="regen", duration=5),
        Ability("Med-Mist", -250, 4, "Heals 250 HP"),
        Ability("Life Steal", -100, 5, "Steals 100 HP, stacks +1000 if full"),
        Ability("Stink Bomb", 50, 10, "Deals 50 damage over 8s", effect="bleed", duration=8)
    ]

    return {
        "1": Character("The Tank", 5000, 250, 500, tank_abilities),
        "2": Character("Assassin/Ninja", 2500, 250, 500, ninja_abilities),
        "3": Character("Voidling Warrior", 2000, 50, 10, voidling_abilities),
        "4": Character("The Medic", 1500, 150, 100, medic_abilities)
    }

def choose_character(characters):
    print("Choose your warrior:")
    for key, char in characters.items():
        print(f"{key}. {char.name}")
    choice = input("Enter number: ")
    return characters[choice]

def battle(player, enemy):
    turn = 1
    while player.is_alive() and enemy.is_alive():
        print(f"\n--- Turn {turn} ---")
        player.show_status()
        enemy.show_status()

        player.tick_effects()
        enemy.tick_effects()

        if player.status.stunned == 0:
            print("\nYour abilities:")
            player.show_abilities()
            move = int(input("Choose ability number: ")) - 1
            player.abilities[move].use(player, enemy)
        else:
            print(f"{player.name} is stunned and skips this turn!")

        if enemy.is_alive():
            if enemy.status.stunned == 0:
                for ab in enemy.abilities:
                    if ab.remaining_cooldown == 0:
                        ab.use(enemy, player)
                        break
            else:
                print(f"{enemy.name} is stunned and skips this turn!")

        player.tick_cooldowns()
        enemy.tick_cooldowns()
        turn += 1
        time.sleep(1)

    winner = player.name if player.is_alive() else enemy.name
    print(f"\n{winner} wins
def play_game():
    while True:
        characters = define_characters()
        player = choose_character(characters)
        enemy = characters["2"] if player.name != "Assassin/Ninja" else characters["1"]

        # Reset characters with fresh cooldowns
        player = Character(player.name, player.max_hp, player.atk, player.df,
                           [Ability(ab.name, ab.damage, ab.cooldown, ab.description, ab.effect, ab.duration, ab.one_use) for ab in player.abilities])
        enemy = Character(enemy.name, enemy.max_hp, enemy.atk, enemy.df,
                          [Ability(ab.name, ab.damage, ab.cooldown, ab.description, ab.effect, ab.duration, ab.one_use) for ab in enemy.abilities])

        battle(player, enemy)

        again = input("\nDo you wish to play again? (yes/no): ").strip().lower()
        if again != "yes":
            print("Thanks for playing Kenjutsu Kenta!")
            break

# Start game
play_game()
