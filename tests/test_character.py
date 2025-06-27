#!/usr/bin/env python3
"""
Test script for the Character class.
Demonstrates loading, manipulating, and saving D&D 5e character data.
"""

import json
import sys
import os

# Add the parent directory to path to import from src
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.dnd_mcp.character import Character


def main():
    # Test 1: Load the example Dragonborn Sorcerer
    print("=== Loading Example Character ===")
    char = Character()
    char.load("../examples/characters/Dragonborn Sorcerer 1.json")

    print(f"Character: {char}")
    print(f"Level: {char.get_level()}")
    print(f"Charisma Modifier: {char.get_ability_modifier('cha')}")
    print(f"Proficiency Bonus: {char.get_proficiency_bonus()}")
    print(f"Current HP: {char.hit_points['current']}/{char.hit_points['max']}")
    print()
    
    # Test 2: Modify character and save
    print("=== Modifying Character ===")
    char.hit_points['current'] = char.hit_points['max']  # Full heal
    char.xp = 350  # Level up!
    char.treasure['gp'] = 50  # Some gold
    
    # Add a new spell
    new_spell = {
        "name": "Magic Missile",
        "description": "Create three darts of magical force.",
        "level": "1st",
        "casting_time": "1 Action",
        "range_area": "120 ft.",
        "duration": "Instantaneous",
        "damage_effect": "Force",
        "components": ["V", "S"],
        "school": "Evocation"
    }
    char.spells.append(new_spell)
    
    print("Character updated!")
    print(f"New XP: {char.xp}")
    print(f"Current HP: {char.hit_points['current']}/{char.hit_points['max']}")
    print(f"Gold: {char.treasure['gp']} gp")
    print(f"Number of spells: {len(char.spells)}")
    print()
    
    # Test 3: Save modified character
    print("=== Saving Modified Character ===")
    output_file = "../examples/characters/modified_character.json"
    char.write(output_file)
    print(f"Character saved to: {output_file}")
    
    # Test 4: Convert to JSON string
    print("\n=== JSON String Output (first 200 chars) ===")
    json_str = char.to_json()
    print(json_str[:200] + "...")
    
    # Test 5: Create a new character from scratch
    print("\n=== Creating New Character ===")
    new_char = Character()
    new_char.name = "Gandalf the Grey"
    new_char.player["name"] = "Player One"
    new_char.race = {
        "name": "Human",
        "subtype": "Variant"
    }
    new_char.classes = [{
        "name": "Wizard",
        "subtype": "School of Evocation",
        "level": 20,
        "hit_die": 6,
        "spellcasting": "int"
    }]
    new_char.alignment = "neutral good"
    new_char.ability_scores = {
        "str": 10, "dex": 14, "con": 16,
        "int": 20, "wis": 18, "cha": 14
    }
    new_char.hit_points = {"max": 164, "current": 164}
    new_char.armor_class = {"value": 17, "description": "Robe of the Archmagi"}
    
    print(f"New character: {new_char}")
    print(f"Intelligence Modifier: {new_char.get_ability_modifier('int')}")
    
    # Save the new character
    new_char.write("../examples/characters/gandalf.json")
    print("New character saved to: ../examples/characters/gandalf.json")


if __name__ == "__main__":
    main()
