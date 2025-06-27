# D&D Character MCP Server Usage Guide

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the server:**
   ```bash
   python character_server.py
   ```

## Tool Reference

### Character Management

#### `load_character(file_path: str)`
Load a character from a JSON file.
- **file_path**: Path to the character JSON file
- **Returns**: Success/error message

```json
load_character("gandalf.json")
```

#### `save_character(file_path: str)`
Save the current character to a JSON file.
- **file_path**: Path where to save the character
- **Returns**: Success/error message

#### `get_character_info()`
Get comprehensive character information.
- **Returns**: JSON with character stats, abilities, level, etc.

#### `update_hit_points(new_current: int)`
Update character's current hit points.
- **new_current**: New current HP value (clamped to 0-max)
- **Returns**: Update confirmation

### Dice Rolling & Checks

#### `roll_skill_check(skill: str, advantage: bool = False, disadvantage: bool = False, modifier: int = 0)`
Roll a skill check with all modifiers.
- **skill**: Skill name (e.g., "perception", "athletics", "sleight_of_hand")
- **advantage**: Roll with advantage (take higher of 2d20)
- **disadvantage**: Roll with disadvantage (take lower of 2d20)  
- **modifier**: Additional modifier to add
- **Returns**: Detailed roll breakdown

**Examples:**
```json
roll_skill_check("perception")
roll_skill_check("stealth", advantage=True)
roll_skill_check("athletics", disadvantage=True, modifier=-2)
```

#### `roll_ability_check(ability: str, advantage: bool = False, disadvantage: bool = False, modifier: int = 0)`
Roll a raw ability check.
- **ability**: Ability score ("str", "dex", "con", "int", "wis", "cha")
- **advantage/disadvantage/modifier**: Same as skill checks
- **Returns**: Detailed roll breakdown

**Examples:**
```json
roll_ability_check("str", modifier=5)
roll_ability_check("dex", advantage=True)
```

#### `roll_saving_throw(ability: str, advantage: bool = False, disadvantage: bool = False, modifier: int = 0)`
Roll a saving throw.
- **ability**: Ability score for the save
- **advantage/disadvantage/modifier**: Same as other rolls
- **Returns**: Detailed roll breakdown including proficiency

**Examples:**
```json
roll_saving_throw("wis", advantage=True)
roll_saving_throw("con", modifier=3)
```

### Character Information

#### `get_character_spells()`
Get all character spells organized by spell level.
- **Returns**: JSON with spells grouped by level

#### `get_character_equipment()`
Get character's weapons, equipment, and treasure.
- **Returns**: JSON with weapons, equipment, and treasure

#### `list_available_skills()`
List all D&D 5e skills and their associated abilities.
- **Returns**: JSON mapping skills to abilities

## Roll Results Format

All dice roll tools return detailed information:

```json
{
  "skill": "Perception",           // What was rolled
  "ability": "WIS",               // Associated ability
  "roll": {
    "result": 15,                 // Final die result used
    "rolls": [15, 8],            // All dice rolled
    "type": "advantage",          // normal/advantage/disadvantage
    "used_roll": 15              // Which roll was used
  },
  "ability_modifier": 4,          // Ability score modifier
  "proficiency_bonus": 3,         // Proficiency bonus (if applicable)
  "is_proficient": true,          // Whether proficient in this skill
  "additional_modifier": 0,       // Any extra modifiers
  "total": 22,                   // Final total
  "breakdown": "15 (roll) + 4 (wis) + 3 (prof) + 0 (modifier) = 22"
}
```

## Character JSON Format

Characters use the D&D 5e JSON schema. Key fields:

```json
{
  "name": "Character Name",
  "player": {
    "name": "Player Name",
    "id": null
  },
  "race": {
    "name": "Human",
    "subtype": "Variant"
  },
  "classes": [
    {
      "name": "Fighter", 
      "level": 5,
      "hit_die": 10
    }
  ],
  "ability_scores": {
    "str": 16, "dex": 14, "con": 15,
    "int": 12, "wis": 13, "cha": 10
  },
  "skills": {
    "athletics": true,      // Proficient skills
    "perception": true
  },
  "saving_throws": {
    "str": true,           // Proficient saves
    "con": true
  }
}
```

## Skills Reference

**Strength**
- Athletics

**Dexterity** 
- Acrobatics
- Sleight of Hand
- Stealth

**Intelligence**
- Arcana
- History  
- Investigation
- Nature
- Religion

**Wisdom**
- Animal Handling
- Insight
- Medicine
- Perception
- Survival

**Charisma**
- Deception
- Intimidation
- Performance
- Persuasion

## Example Session

```python
# Load a character
load_character("thorin.json")

# Check character info
get_character_info()

# Roll some checks
roll_skill_check("athletics")                    # Proficient skill
roll_skill_check("stealth", disadvantage=True)   # With disadvantage  
roll_saving_throw("con", advantage=True)         # Proficient save
roll_ability_check("str", modifier=2)            # Raw ability + modifier

# Update character
update_hit_points(45)

# Save changes
save_character("thorin_updated.json")
```
