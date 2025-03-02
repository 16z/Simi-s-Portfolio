import random
import time
import os

class TextAdventureGame:
    def __init__(self):
        self.player = {
            "name": "",
            "health": 100,
            "inventory": [],
            "score": 0
        }
        
        self.locations = {
            "forest": {
                "description": "A dense forest with towering trees. Sunlight barely filters through the canopy.",
                "items": ["stick", "berries"],
                "enemies": ["wolf"],
                "exits": ["cave", "river"]
            },
            "cave": {
                "description": "A dark, damp cave with strange echoes. Water drips from the ceiling.",
                "items": ["torch", "old coin"],
                "enemies": ["bat"],
                "exits": ["forest", "tunnel"]
            },
            "river": {
                "description": "A clear, rushing river with stones that could be used to cross.",
                "items": ["fish", "smooth stone"],
                "enemies": [],
                "exits": ["forest", "mountain"]
            },
            "tunnel": {
                "description": "A narrow, winding tunnel. The walls are covered in strange symbols.",
                "items": ["ancient key"],
                "enemies": ["giant spider"],
                "exits": ["cave", "treasure room"]
            },
            "mountain": {
                "description": "A steep mountain path with a breathtaking view of the surrounding lands.",
                "items": ["eagle feather"],
                "enemies": ["mountain lion"],
                "exits": ["river", "summit"]
            },
            "treasure room": {
                "description": "A room filled with gold and jewels. The ancient treasure of a forgotten civilization.",
                "items": ["golden crown", "jeweled sword"],
                "enemies": ["guardian statue"],
                "exits": ["tunnel"]
            },
            "summit": {
                "description": "The mountain's summit. You can see for miles in every direction.",
                "items": ["mystical orb"],
                "enemies": ["dragon"],
                "exits": ["mountain"]
            }
        }
        
        self.current_location = "forest"
        self.game_over = False

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_with_delay(self, text, delay=0.03):
        """Print text with a slight delay between characters for effect."""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    def start_game(self):
        """Initialize and start the game."""
        self.clear_screen()
        self.print_with_delay("=== THE MYSTIC QUEST ===", 0.05)
        time.sleep(0.5)
        
        self.print_with_delay("\nYou awaken in a strange forest with no memory of how you got here.")
        self.print_with_delay("Your goal is to explore this mysterious land and find the legendary mystic orb.")
        time.sleep(1)
        
        self.player["name"] = input("\nWhat is your name, adventurer? ")
        self.print_with_delay(f"\nWelcome, {self.player['name']}. Your adventure begins now...")
        time.sleep(1)
        
        while not self.game_over:
            self.game_loop()
            
        self.end_game()

    def show_status(self):
        """Display the current game status."""
        self.clear_screen()
        print(f"=== {self.player['name']}'s Adventure ===")
        print(f"Health: {self.player['health']} | Score: {self.player['score']}")
        print(f"Inventory: {', '.join(self.player['inventory']) if self.player['inventory'] else 'Empty'}")
        print("\n" + "="*40 + "\n")
        
        location = self.locations[self.current_location]
        self.print_with_delay(f"You are in: {self.current_location.upper()}")
        self.print_with_delay(location["description"])
        
        if location["items"]:
            self.print_with_delay(f"\nYou see: {', '.join(location['items'])}")
        
        if location["enemies"]:
            self.print_with_delay(f"\nBeware of: {', '.join(location['enemies'])}")
        
        self.print_with_delay(f"\nPossible exits: {', '.join(location['exits'])}")
        
    def get_command(self):
        """Get and process user commands."""
        print("\n" + "-"*40)
        command = input("\nWhat would you like to do? ").lower().split()
        
        if not command:
            self.print_with_delay("Please enter a command.")
            return
            
        action = command[0]
        
        if action == "help":
            self.show_help()
        elif action == "go" and len(command) > 1:
            self.move_player(command[1])
        elif action == "take" and len(command) > 1:
            self.take_item(command[1])
        elif action == "inventory" or action == "inv":
            self.show_inventory()
        elif action == "examine" and len(command) > 1:
            self.examine_item(command[1])
        elif action == "fight" and len(command) > 1:
            self.fight_enemy(command[1])
        elif action == "quit":
            self.game_over = True
        else:
            self.print_with_delay("I don't understand that command. Type 'help' for commands.")
    
    def show_help(self):
        """Display available commands to the player."""
        self.print_with_delay("\n=== Available Commands ===")
        self.print_with_delay("go [location] - Move to a new location")
        self.print_with_delay("take [item] - Pick up an item")
        self.print_with_delay("inventory/inv - Show your inventory")
        self.print_with_delay("examine [item] - Look closely at an item")
        self.print_with_delay("fight [enemy] - Fight an enemy")
        self.print_with_delay("help - Show this help menu")
        self.print_with_delay("quit - End the game")
        input("\nPress Enter to continue...")
    
    def move_player(self, destination):
        """Move player to a new location if available."""
        current = self.locations[self.current_location]
        
        if destination in current["exits"]:
            self.current_location = destination
            self.player["score"] += 5
            self.print_with_delay(f"You travel to the {destination}.")
            
            # Random event chance when moving
            if random.random() < 0.3:
                self.random_event()
        else:
            self.print_with_delay(f"You can't go to {destination} from here.")
    
    def take_item(self, item):
        """Allow player to pick up items."""
        location = self.locations[self.current_location]
        
        if item in location["items"]:
            location["items"].remove(item)
            self.player["inventory"].append(item)
            self.player["score"] += 10
            self.print_with_delay(f"You picked up the {item}.")
            
            # Special item effects
            if item == "berries":
                self.print_with_delay("You eat some of the berries. They're delicious and nutritious!")
                self.player["health"] += 10
                self.print_with_delay(f"Health increased to {self.player['health']}.")
            elif item == "mystical orb":
                self.print_with_delay("As you take the mystical orb, it glows with an otherworldly light.")
                self.print_with_delay("You feel its ancient power coursing through you.")
                self.player["score"] += 100
                self.print_with_delay("Congratulations! You have found the legendary artifact!")
                self.print_with_delay("You can continue exploring or type 'quit' to end the game.")
        else:
            self.print_with_delay(f"There is no {item} here to take.")
    
    def show_inventory(self):
        """Display the player's inventory."""
        if self.player["inventory"]:
            self.print_with_delay("\n=== Your Inventory ===")
            for item in self.player["inventory"]:
                self.print_with_delay(f"- {item}")
        else:
            self.print_with_delay("Your inventory is empty.")
        input("\nPress Enter to continue...")
    
    def examine_item(self, item):
        """Examine an item for more information."""
        # Player can examine items in their inventory or in the current location
        location = self.locations[self.current_location]
        
        if item in self.player["inventory"] or item in location["items"]:
            self.print_with_delay(f"You examine the {item} closely.")
            
            # Custom descriptions for each item
            descriptions = {
                "stick": "A sturdy wooden stick. Could be useful as a basic weapon.",
                "berries": "Red, juicy berries. They look safe to eat.",
                "torch": "An old torch that could be lit to provide light in dark places.",
                "old coin": "A coin with strange markings. Might be valuable to a collector.",
                "fish": "A fresh fish from the river. Could restore some health if eaten.",
                "smooth stone": "A perfectly smooth stone, polished by the river. It feels lucky.",
                "ancient key": "An ornate key with mysterious symbols. Must unlock something important.",
                "eagle feather": "A magnificent feather from a large eagle. Perhaps it has magical properties.",
                "golden crown": "A crown made of pure gold. Fit for royalty.",
                "jeweled sword": "A sword with jewels embedded in the hilt. Looks very powerful.",
                "mystical orb": "The legendary artifact you sought. It pulses with ancient energy."
            }
            
            if item in descriptions:
                self.print_with_delay(descriptions[item])
            else:
                self.print_with_delay("It's just an ordinary " + item + ".")
        else:
            self.print_with_delay(f"You don't see any {item} to examine.")
    
    def fight_enemy(self, enemy):
        """Fight an enemy in the current location."""
        location = self.locations[self.current_location]
        
        if enemy in location["enemies"]:
            self.print_with_delay(f"You engage the {enemy} in battle!")
            
            # Check if player has a weapon
            weapon = None
            for item in self.player["inventory"]:
                if item in ["stick", "jeweled sword"]:
                    weapon = item
                    break
            
            # Calculate battle outcome based on weapon and enemy type
            enemy_strength = {
                "wolf": 20,
                "bat": 10,
                "giant spider": 30,
                "mountain lion": 40,
                "guardian statue": 50,
                "dragon": 70
            }
            
            weapon_power = {
                "stick": 10,
                "jeweled sword": 40,
                None: 5  # bare hands
            }
            
            player_power = weapon_power[weapon]
            enemy_power = enemy_strength.get(enemy, 15)
            
            # Add some randomness
            player_roll = random.randint(1, 20) + player_power
            enemy_roll = random.randint(1, 20) + enemy_power
            
            if weapon:
                self.print_with_delay(f"You attack with your {weapon}!")
            else:
                self.print_with_delay("You attack with your bare hands!")
            
            time.sleep(1)
            
            if player_roll >= enemy_roll:
                self.print_with_delay(f"You defeated the {enemy}!")
                location["enemies"].remove(enemy)
                self.player["score"] += 20
                
                # Chance to find an item
                if random.random() < 0.5:
                    loot = random.choice(["health potion", "gold coins", "magic dust"])
                    self.print_with_delay(f"The {enemy} dropped: {loot}")
                    self.player["inventory"].append(loot)
            else:
                damage = enemy_power // 3
                self.player["health"] -= damage
                self.print_with_delay(f"The {enemy} wounds you! You lose {damage} health.")
                self.print_with_delay(f"Your health is now {self.player['health']}.")
                
                if self.player["health"] <= 0:
                    self.print_with_delay("You have been defeated...")
                    self.game_over = True
                else:
                    self.print_with_delay(f"The {enemy} retreats but is still in the area.")
        else:
            self.print_with_delay(f"There is no {enemy} here to fight.")
    
    def random_event(self):
        """Generate a random event during travel."""
        events = [
            "You find a small cache of supplies hidden under some rocks.",
            "You trip and fall, taking minor damage.",
            "A sudden rain shower passes overhead.",
            "You hear strange noises in the distance.",
            "You discover a shortcut that will make future travel easier."
        ]
        
        event = random.choice(events)
        self.print_with_delay("\nRandom event: " + event)
        
        if event == events[0]:  # supply cache
            item = random.choice(["bandage", "water flask", "dried meat"])
            self.player["inventory"].append(item)
            self.print_with_delay(f"You found: {item}")
        elif event == events[1]:  # trip and fall
            damage = random.randint(5, 10)
            self.player["health"] -= damage
            self.print_with_delay(f"You lose {damage} health. Current health: {self.player['health']}")
            if self.player["health"] <= 0:
                self.print_with_delay("Your injuries are too severe...")
                self.game_over = True
    
    def game_loop(self):
        """Main game loop."""
        self.show_status()
        self.get_command()
        time.sleep(0.5)
    
    def end_game(self):
        """Handle end of game and display final score."""
        self.clear_screen()
        self.print_with_delay("\n=== GAME OVER ===")
        
        if self.player["health"] <= 0:
            self.print_with_delay(f"Sorry, {self.player['name']}, your adventure has come to an end.")
            self.print_with_delay("You have been defeated in your quest.")
        else:
            self.print_with_delay(f"Thank you for playing, {self.player['name']}!")
        
        self.print_with_delay(f"\nFinal Score: {self.player['score']}")
        self.print_with_delay(f"Items collected: {len(self.player['inventory'])}")
        
        if "mystical orb" in self.player["inventory"]:
            self.print_with_delay("\nCongratulations! You completed your quest to find the mystical orb!")
            self.print_with_delay("You are a true hero!")
        
        self.print_with_delay("\nThanks for playing THE MYSTIC QUEST!")

# Run the game if this script is executed
if __name__ == "__main__":
    game = TextAdventureGame()
    try:
        game.start_game()
    except KeyboardInterrupt:
        print("\n\nGame terminated by user. Thanks for playing!")