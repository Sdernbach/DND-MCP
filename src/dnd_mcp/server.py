"""
MCP server for D&D 5e character management.

This module provides the main MCP server implementation with tools for
character management, dice rolling, and game mechanics.
"""

import json
import os
from typing import Optional

from mcp.server.fastmcp import FastMCP

from .character import Character
from .dice import parse_modifiers_string, perform_roll, DiceModifier, FlatModifier
from .constants import SKILL_ABILITIES, COMMON_MODIFIERS

# Create the MCP server
server = FastMCP("dnd-character-server")

# Global character storage
current_character: Optional[Character] = None


@server.tool()
def load_character(file_path: str) -> str:
    """Load a D&D character from a JSON file"""
    global current_character
    
    try:
        # Handle relative paths
        if not os.path.isabs(file_path):
            file_path = os.path.join(os.getcwd(), file_path)
            
        current_character = Character()
        current_character.load(file_path)
        
        return f"Successfully loaded character: {current_character.name} (Level {current_character.get_level()})"
    except FileNotFoundError:
        return f"Error: Character file not found at {file_path}"
    except Exception as e:
        return f"Error loading character: {str(e)}"


@server.tool()
def get_character_info() -> str:
    """Get basic information about the currently loaded character"""
    if not current_character:
        return "No character currently loaded. Use load_character() first."
    
    info = {
        "name": current_character.name,
        "nickname": current_character.nickname,
        "race": current_character.race.get("name", "Unknown"),
        "level": current_character.get_level(),
        "classes": [f"{cls.get('name', 'Unknown')} {cls.get('level', 1)}" for cls in current_character.classes],
        "alignment": current_character.alignment,
        "hit_points": current_character.hit_points,
        "armor_class": current_character.armor_class.get("value", 10),
        "ability_scores": current_character.ability_scores,
        "proficiency_bonus": current_character.get_proficiency_bonus()
    }
    
    return json.dumps(info, indent=2)


@server.tool()
def roll_ability_check(ability: str, modifiers: str = "") -> str:
    """Roll an ability check for a specific ability score
    
    Args:
        ability: The ability score to check (str, dex, con, int, wis, cha)
        modifiers: Space-separated modifiers string. Examples:
            - "advantage +2" 
            - "disadvantage guidance:1d4"
            - "+3 bardic:1d4 bless:1d4"
    """
    if not current_character:
        return "No character currently loaded. Use load_character() first."
    
    ability = ability.lower()
    if ability not in current_character.ability_scores:
        return f"Invalid ability: {ability}. Valid abilities: {list(current_character.ability_scores.keys())}"
    
    # Parse modifiers
    roll_modifiers = parse_modifiers_string(modifiers)
    
    # Calculate base modifier
    ability_modifier = current_character.get_ability_modifier(ability)
    
    # Perform the roll
    result = perform_roll(ability_modifier, roll_modifiers, f"{ability.upper()} Check")
    result["ability"] = ability.upper()
    
    return json.dumps(result, indent=2)


@server.tool()
def roll_skill_check(skill: str, modifiers: str = "") -> str:
    """Roll a skill check for a specific skill
    
    Args:
        skill: The skill name (e.g., "perception", "athletics", "sleight_of_hand")
        modifiers: Space-separated modifiers string. Examples:
            - "advantage +2"
            - "disadvantage guidance:1d4" 
            - "+3 bardic:1d8 inspiration:1d4"
    """
    if not current_character:
        return "No character currently loaded. Use load_character() first."
    
    skill = skill.lower().replace(" ", "_")
    
    if skill not in SKILL_ABILITIES:
        available_skills = list(SKILL_ABILITIES.keys())
        return f"Invalid skill: {skill}. Available skills: {available_skills}"
    
    # Get the ability this skill uses
    ability = SKILL_ABILITIES[skill]
    
    # Parse modifiers
    roll_modifiers = parse_modifiers_string(modifiers)
    
    # Calculate base modifier (ability + proficiency if applicable)
    ability_modifier = current_character.get_ability_modifier(ability)
    proficiency_bonus = current_character.get_proficiency_bonus()
    is_proficient = current_character.skills.get(skill, False)
    
    base_modifier = ability_modifier + (proficiency_bonus if is_proficient else 0)
    
    # Perform the roll
    result = perform_roll(base_modifier, roll_modifiers, f"{skill.replace('_', ' ').title()} Check")
    result["skill"] = skill.replace("_", " ").title()
    result["ability"] = ability.upper()
    result["ability_modifier"] = ability_modifier
    result["proficiency_bonus"] = proficiency_bonus if is_proficient else 0
    result["is_proficient"] = is_proficient
    
    return json.dumps(result, indent=2)


@server.tool()
def roll_saving_throw(ability: str, modifiers: str = "") -> str:
    """Roll a saving throw for a specific ability
    
    Args:
        ability: The ability for the save (str, dex, con, int, wis, cha)
        modifiers: Space-separated modifiers string. Examples:
            - "advantage +2"
            - "disadvantage bless:1d4"
            - "+1 guidance:1d4 bardic:1d8"
    """
    if not current_character:
        return "No character currently loaded. Use load_character() first."
    
    ability = ability.lower()
    if ability not in current_character.ability_scores:
        return f"Invalid ability: {ability}. Valid abilities: {list(current_character.ability_scores.keys())}"
    
    # Parse modifiers
    roll_modifiers = parse_modifiers_string(modifiers)
    
    # Calculate base modifier (ability + proficiency if applicable)
    ability_modifier = current_character.get_ability_modifier(ability)
    proficiency_bonus = current_character.get_proficiency_bonus()
    is_proficient = current_character.saving_throws.get(ability, False)
    
    base_modifier = ability_modifier + (proficiency_bonus if is_proficient else 0)
    
    # Perform the roll
    result = perform_roll(base_modifier, roll_modifiers, f"{ability.upper()} Saving Throw")
    result["saving_throw"] = ability.upper()
    result["ability_modifier"] = ability_modifier
    result["proficiency_bonus"] = proficiency_bonus if is_proficient else 0
    result["is_proficient"] = is_proficient
    
    return json.dumps(result, indent=2)


@server.tool()
def roll_attack(weapon_name: str = "", modifiers: str = "") -> str:
    """Roll an attack roll
    
    Args:
        weapon_name: Name of weapon to attack with (optional)
        modifiers: Space-separated modifiers string. Examples:
            - "advantage +1"
            - "disadvantage bless:1d4"
            - "+2 guidance:1d4"
    """
    if not current_character:
        return "No character currently loaded. Use load_character() first."
    
    # For now, just roll a generic attack (could be enhanced to use weapon stats)
    # Assuming STR-based attack for simplicity
    ability = "str"
    
    # Parse modifiers
    roll_modifiers = parse_modifiers_string(modifiers)
    
    # Calculate base modifier (ability + proficiency)
    ability_modifier = current_character.get_ability_modifier(ability)
    proficiency_bonus = current_character.get_proficiency_bonus()
    base_modifier = ability_modifier + proficiency_bonus
    
    # Perform the roll
    result = perform_roll(base_modifier, roll_modifiers, f"Attack Roll")
    result["weapon"] = weapon_name if weapon_name else "Generic Attack"
    result["ability"] = ability.upper()
    result["ability_modifier"] = ability_modifier
    result["proficiency_bonus"] = proficiency_bonus
    
    return json.dumps(result, indent=2)


@server.tool()
def get_character_spells() -> str:
    """Get all spells known by the character"""
    if not current_character:
        return "No character currently loaded. Use load_character() first."
    
    if not current_character.spells:
        return "Character has no spells."
    
    spells_by_level = {}
    for spell in current_character.spells:
        level = spell.get("level", 0)
        if level not in spells_by_level:
            spells_by_level[level] = []
        spells_by_level[level].append(spell)
    
    return json.dumps(spells_by_level, indent=2)


@server.tool()
def get_character_equipment() -> str:
    """Get all equipment carried by the character"""
    if not current_character:
        return "No character currently loaded. Use load_character() first."
    
    equipment_info = {
        "weapons": current_character.weapons,
        "equipment": current_character.equipment,
        "treasure": current_character.treasure
    }
    
    return json.dumps(equipment_info, indent=2)


@server.tool()
def update_hit_points(new_current: int) -> str:
    """Update the character's current hit points"""
    if not current_character:
        return "No character currently loaded. Use load_character() first."
    
    max_hp = current_character.hit_points.get("max", 0)
    
    if new_current < 0:
        new_current = 0
    elif new_current > max_hp:
        new_current = max_hp
    
    old_hp = current_character.hit_points.get("current", 0)
    current_character.hit_points["current"] = new_current
    
    return f"Hit points updated: {old_hp} -> {new_current} (Max: {max_hp})"


@server.tool()
def save_character(file_path: str) -> str:
    """Save the current character to a JSON file"""
    if not current_character:
        return "No character currently loaded. Use load_character() first."
    
    try:
        # Handle relative paths
        if not os.path.isabs(file_path):
            file_path = os.path.join(os.getcwd(), file_path)
            
        current_character.write(file_path)
        return f"Character saved successfully to {file_path}"
    except Exception as e:
        return f"Error saving character: {str(e)}"


@server.tool()
def list_available_skills() -> str:
    """List all available D&D 5e skills and their associated abilities"""
    skills_info = {}
    for skill, ability in SKILL_ABILITIES.items():
        skills_info[skill.replace("_", " ").title()] = ability.upper()
    
    return json.dumps(skills_info, indent=2)


@server.tool()
def create_custom_modifier(name: str, dice: str = "", flat: int = 0, description: str = "") -> str:
    """Create and apply a custom modifier for testing
    
    Args:
        name: Name of the modifier
        dice: Dice expression (e.g., "1d4", "2d6") 
        flat: Flat numeric bonus
        description: Description of what this modifier represents
    """
    modifiers = []
    
    if dice:
        try:
            dice_mod = DiceModifier(name, dice, description)
            result = dice_mod.roll()
            modifiers.append(f"Dice: {result}")
        except ValueError as e:
            return f"Error: {e}"
    
    if flat != 0:
        flat_mod = FlatModifier(name, flat, description)
        modifiers.append(f"Flat: +{flat} ({name})")
    
    if not modifiers:
        return "No modifier created. Specify either dice or flat value."
    
    return json.dumps({
        "modifier_name": name,
        "description": description,
        "results": modifiers
    }, indent=2)


@server.tool()
def list_common_modifiers() -> str:
    """List common D&D modifiers and their typical dice"""
    return json.dumps(COMMON_MODIFIERS, indent=2)


def run_server():
    """Run the MCP server"""
    server.run()


if __name__ == "__main__":
    run_server()
