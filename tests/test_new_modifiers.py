#!/usr/bin/env python3
"""
Test script for the improved modifier system
"""

import json
import sys
import os

# Add the parent directory to path to import from src
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.dnd_mcp.server import (
    load_character, roll_skill_check, roll_ability_check, 
    roll_saving_throw, roll_attack, list_common_modifiers
)

def test_new_modifier_system():
    """Test the new flexible modifier system"""
    print("=== Testing New Modifier System ===\n")
    
    # Load Thorin
    print("Loading Thorin...")
    result = load_character("../examples/characters/thorin.json")
    print(f"Result: {result}\n")
    
    print("=== Basic Rolls ===")
    
    # Normal roll
    result = roll_skill_check("athletics")
    print(f"Normal Athletics:\n{result}\n")
    
    print("=== Advantage/Disadvantage ===")
    
    # Advantage
    result = roll_skill_check("perception", "advantage")
    print(f"Perception with Advantage:\n{result}\n")
    
    # Disadvantage  
    result = roll_skill_check("stealth", "disadvantage")
    print(f"Stealth with Disadvantage:\n{result}\n")
    
    print("=== Flat Modifiers ===")
    
    # Flat bonus
    result = roll_ability_check("str", "+3")
    print(f"Strength check with +3:\n{result}\n")
    
    # Flat penalty
    result = roll_skill_check("acrobatics", "-2")
    print(f"Acrobatics with -2:\n{result}\n")
    
    print("=== Dice Modifiers ===")
    
    # Guidance cantrip
    result = roll_skill_check("investigation", "guidance:1d4")
    print(f"Investigation with Guidance (1d4):\n{result}\n")
    
    # Bardic inspiration  
    result = roll_skill_check("persuasion", "bardic:1d6")
    print(f"Persuasion with Bardic Inspiration (1d6):\n{result}\n")
    
    print("=== Complex Combinations ===")
    
    # Multiple dice modifiers
    result = roll_saving_throw("wis", "bless:1d4 guidance:1d4")
    print(f"Wisdom save with Bless + Guidance:\n{result}\n")
    
    # Advantage + flat + dice
    result = roll_skill_check("athletics", "advantage +2 bardic:1d8")
    print(f"Athletics with Advantage + 2 + Bardic Inspiration:\n{result}\n")
    
    # Disadvantage + multiple bonuses
    result = roll_skill_check("stealth", "disadvantage +1 guidance:1d4 bless:1d4")
    print(f"Stealth with Disadvantage but multiple bonuses:\n{result}\n")
    
    print("=== Attack Rolls ===")
    
    # Basic attack
    result = roll_attack("Battleaxe")
    print(f"Battleaxe attack:\n{result}\n")
    
    # Attack with modifiers
    result = roll_attack("Battleaxe", "advantage bless:1d4")
    print(f"Battleaxe with Advantage + Bless:\n{result}\n")
    
    print("=== Custom Modifiers ===")
    
    # Custom dice modifier (function not yet implemented)
    # result = create_custom_modifier("Divine Favor", "1d4", 0, "Paladin spell bonus damage")
    # print(f"Custom modifier test:\n{result}\n")
    print("Custom modifier functionality not yet implemented\n")
    
    print("=== Common Modifiers Reference ===")
    
    # List common modifiers
    result = list_common_modifiers()
    print(f"Common D&D modifiers:\n{result}\n")
    
    print("=== Test Complete ===")

if __name__ == "__main__":
    test_new_modifier_system()
