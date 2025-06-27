#!/usr/bin/env python3
"""
Test script for     # Skill check with advantage
    result = roll_skill_check("perception", "advantage")
    print(f"Perception check (advantage):\n{result}\n")
    
    # Skill check with disadvantage and modifier
    result = roll_skill_check("stealth", "disadvantage +2")
    print(f"Stealth check (disadvantage +2):\n{result}\n") Character MCP Server
This demonstrates the basic functionality of the character server.
"""

import json
import sys
import os

# Add the parent directory to path to import from src
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.dnd_mcp.server import (
    load_character, get_character_info, roll_skill_check, 
    roll_ability_check, roll_saving_throw, update_hit_points,
    get_character_spells, get_character_equipment, list_available_skills
)

def test_character_server():
    """Test the character server functionality"""
    print("=== D&D Character MCP Server Test ===\n")
    
    # Test loading a character
    print("1. Loading Gandalf character...")
    result = load_character("../examples/characters/gandalf.json")
    print(f"Result: {result}\n")
    
    # Get character info
    print("2. Getting character information...")
    info = get_character_info()
    print(f"Character Info:\n{info}\n")
    
    # List available skills
    print("3. Available skills:")
    skills = list_available_skills()
    print(f"{skills}\n")
    
    # Test skill checks
    print("4. Rolling skill checks...")
    
    # Normal skill check
    result = roll_skill_check("arcana")
    print(f"Arcana check (normal):\n{result}\n")
    
    # Skill check with advantage
    result = roll_skill_check("perception", "advantage")
    print(f"Perception check (advantage):\n{result}\n")
    
    # Skill check with disadvantage and modifier
    result = roll_skill_check("stealth", "disadvantage -2")
    print(f"Stealth check (disadvantage, -2):\n{result}\n")
    
    # Test ability checks
    print("5. Rolling ability checks...")
    result = roll_ability_check("int", "+5")
    print(f"Intelligence check (+5):\n{result}\n")
    
    # Test saving throws
    print("6. Rolling saving throws...")
    result = roll_saving_throw("wis", "advantage")
    print(f"Wisdom saving throw (advantage):\n{result}\n")
    
    # Test equipment and spells
    print("7. Getting character spells...")
    spells = get_character_spells()
    print(f"Spells:\n{spells}\n")
    
    print("8. Getting character equipment...")
    equipment = get_character_equipment()
    print(f"Equipment:\n{equipment}\n")
    
    # Test HP update
    print("9. Testing hit point update...")
    result = update_hit_points(150)
    print(f"HP Update: {result}\n")
    
    print("=== Test Complete ===")

if __name__ == "__main__":
    test_character_server()
