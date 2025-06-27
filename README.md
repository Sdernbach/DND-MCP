# D&D Character MCP Server

An MCP (Model Context Protocol) server for managing Dungeons & Dragons 5th Edition characters. This server provides tools for loading characters, performing dice rolls, skill checks, ability checks, saving throws, and managing character state.

## Features

- **Character Management**: Load and save D&D 5e characters from JSON files
- **Advanced Dice Rolling**: Flexible modifier system supporting advantage, disadvantage, and custom modifiers
- **Skill Checks**: All 18 D&D 5e skills with proficiency and ability modifier calculations
- **Ability Checks**: Direct ability score checks with modifiers
- **Saving Throws**: Saving throws with proficiency bonuses where applicable
- **Attack Rolls**: Weapon attack rolls with proficiency bonuses
- **Complex Modifiers**: Support for dice modifiers (bardic inspiration, guidance, bless) and flat bonuses
- **Character Information**: Access to character stats, spells, equipment, and more
- **Hit Point Management**: Update and track character hit points

## Modifier System

The server uses a flexible modifier string system that supports:
- **Advantage/Disadvantage**: `"advantage"` or `"disadvantage"`
- **Flat Modifiers**: `"+2"`, `"-1"`, `"+3"`
- **Dice Modifiers**: `"guidance:1d4"`, `"bardic:1d8"`, `"bless:1d4"`
- **Combinations**: `"advantage +2 bardic:1d6 guidance:1d4"`

### Examples:
```python
# Simple advantage
roll_skill_check("perception", "advantage")

# Complex combination
roll_skill_check("athletics", "advantage +2 bardic:1d8 guidance:1d4")

# Multiple dice bonuses
roll_saving_throw("wis", "bless:1d4 guidance:1d4")
```

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python character_server.py
```

## Available Tools

### Character Management
- `load_character(file_path)` - Load a character from a JSON file
- `get_character_info()` - Get basic character information
- `save_character(file_path)` - Save the current character to a JSON file
- `update_hit_points(new_current)` - Update character's current hit points

### Dice Rolling & Checks
- `roll_skill_check(skill, modifiers="")` - Roll a skill check with flexible modifiers
- `roll_ability_check(ability, modifiers="")` - Roll an ability check with flexible modifiers
- `roll_saving_throw(ability, modifiers="")` - Roll a saving throw with flexible modifiers
- `roll_attack(weapon_name="", modifiers="")` - Roll an attack with weapon proficiency
- `list_common_modifiers()` - Reference for common D&D modifiers
- `create_custom_modifier(name, dice="", flat=0, description="")` - Create custom modifiers

### Character Information
- `get_character_spells()` - Get all character spells organized by level
- `get_character_equipment()` - Get weapons, equipment, and treasure
- `list_available_skills()` - List all D&D 5e skills and their associated abilities

## Usage Examples

### Loading a Character
```python
load_character("gandalf.json")
```

### Rolling Skill Checks
```python
# Normal skill check
roll_skill_check("perception")

# Skill check with advantage
roll_skill_check("stealth", "advantage")

# Skill check with disadvantage and flat modifier
roll_skill_check("athletics", "disadvantage -2")

# Complex combination
roll_skill_check("persuasion", "advantage +1 bardic:1d8 guidance:1d4")
```

### Rolling Ability Checks
```python
# Strength check with flat bonus
roll_ability_check("str", "+3")

# Dexterity check with advantage and guidance
roll_ability_check("dex", "advantage guidance:1d4")
```

### Rolling Saving Throws
```python
# Wisdom saving throw with advantage
roll_saving_throw("wis", "advantage")

# Constitution saving throw with multiple bonuses
roll_saving_throw("con", "bless:1d4 +2")
```

### Attack Rolls
```python
# Basic weapon attack
roll_attack("Longsword")

# Attack with advantage and bless
roll_attack("Longbow", "advantage bless:1d4")
```

## Supported Skills

The server supports all 18 D&D 5e skills:
- **Strength**: Athletics
- **Dexterity**: Acrobatics, Sleight of Hand, Stealth  
- **Intelligence**: Arcana, History, Investigation, Nature, Religion
- **Wisdom**: Animal Handling, Insight, Medicine, Perception, Survival
- **Charisma**: Deception, Intimidation, Performance, Persuasion

## Character JSON Format

Characters should be saved in JSON format following the D&D 5e schema. See `gandalf.json` for an example character file.

Required fields:
- `player` - Player information
- `race` - Character race information

Optional fields include ability scores, classes, skills, spells, equipment, and more.

## Testing

Run the test script to see the server in action:
```bash
python test_server.py
```

This will load the example Gandalf character and demonstrate various server capabilities.

## Character Class

The underlying `Character` class provides:
- JSON serialization/deserialization
- Level calculation from multiclass levels
- Ability modifier calculation
- Proficiency bonus calculation based on level
- Comprehensive character data management

## License
GNU GENERAL PUBLIC LICENSE
See LICENSE file for details.
