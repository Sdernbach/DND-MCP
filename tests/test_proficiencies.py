#!/usr/bin/env python3
"""
Test script demonstrating proficiencies with Thorin character
"""

import json
import sys
import os

# Add the parent directory to path to import from src
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.dnd_mcp.server import (
    load_character, get_character_info, roll_skill_check, 
    roll_saving_throw
)

def test_proficiencies():
    """Test proficiency bonuses with Thorin"""
    print("=== Testing Proficiencies with Thorin ===\n")
    
    # Load Thorin
    print("Loading Thorin...")
    result = load_character("../examples/characters/thorin.json")
    print(f"Result: {result}\n")
    
    # Get character info
    info = get_character_info()
    print(f"Character Info:\n{info}\n")
    
    print("=== Skill Checks (Proficient vs Non-Proficient) ===")
    
    # Athletics (proficient)
    result = roll_skill_check("athletics")
    print(f"Athletics (PROFICIENT):\n{result}\n")
    
    # Acrobatics (not proficient)
    result = roll_skill_check("acrobatics") 
    print(f"Acrobatics (NOT proficient):\n{result}\n")
    
    # Intimidation (proficient)
    result = roll_skill_check("intimidation")
    print(f"Intimidation (PROFICIENT):\n{result}\n")
    
    print("=== Saving Throws (Proficient vs Non-Proficient) ===")
    
    # Strength save (proficient)
    result = roll_saving_throw("str")
    print(f"Strength Save (PROFICIENT):\n{result}\n")
    
    # Dexterity save (not proficient)
    result = roll_saving_throw("dex")
    print(f"Dexterity Save (NOT proficient):\n{result}\n")

if __name__ == "__main__":
    test_proficiencies()
