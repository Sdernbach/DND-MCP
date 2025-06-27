# D&D 5e Character Class

A Python class for managing D&D 5e character data based on the provided JSON schema.

## Features

- Load character data from JSON files or strings
- Save character data to JSON files or convert to JSON strings
- Support for all D&D 5e character properties including:
  - Basic info (name, race, classes, background)
  - Ability scores and derived stats
  - Combat stats (HP, AC, saving throws, skills)
  - Equipment, weapons, spells, and proficiencies
  - Character details and treasure

## Usage

### Loading a Character

```python
from character import Character

# Load from file
char = Character()
char.load("path/to/character.json")

# Or load from JSON string
json_data = '{"name": "Example", "player": {"name": "Player"}, "race": {"name": "Human"}}'
char = Character()
char.load_from_json(json_data)
```

### Accessing Character Data

```python
print(f"Character: {char.name}")
print(f"Level: {char.get_level()}")
print(f"Charisma Modifier: {char.get_ability_modifier('cha')}")
print(f"Proficiency Bonus: {char.get_proficiency_bonus()}")
```

### Modifying Character Data

```python
# Update basic stats
char.hit_points['current'] = 25
char.xp = 1000
char.treasure['gp'] = 100

# Add equipment or spells
char.spells.append({
    "name": "Fireball",
    "level": "3rd",
    "school": "Evocation"
})
```

### Saving Character Data

```python
# Save to file
char.write("character_backup.json")

# Or get as JSON string
json_string = char.to_json()
```

## Class Structure

The Character class includes:

- **Basic Properties**: name, nickname, player info, race, classes
- **Progression**: XP, level calculation, background
- **Combat Stats**: HP, AC, ability scores, saves, skills, speed
- **Features**: spells, weapons, equipment, feats, proficiencies
- **Character Details**: personality, backstory, physical description
- **Treasure**: coin purse (pp, ep, gp, sp, cp)

## Methods

- `load(file_path)`: Load character from JSON file
- `load_from_json(json_string)`: Load character from JSON string
- `write(file_path)`: Save character to JSON file
- `to_json()`: Convert character to JSON string
- `to_dict()`: Convert character to dictionary
- `get_level()`: Calculate total character level
- `get_ability_modifier(ability)`: Calculate ability modifier
- `get_proficiency_bonus()`: Calculate proficiency bonus

## Testing

Run the test script to see examples:

```bash
python test_character.py
```

This will demonstrate loading the example Dragonborn Sorcerer, modifying data, and creating new characters.
