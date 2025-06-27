# Improved D&D Modifier System

## Overview

The new modifier system provides a much more flexible and realistic way to handle D&D 5e dice rolling mechanics. Instead of separate boolean flags for advantage/disadvantage and simple integer modifiers, the system now supports:

1. **Mutually exclusive advantage/disadvantage** using an enum
2. **Multiple dice modifiers** (bardic inspiration, guidance, bless, etc.)
3. **Multiple flat modifiers** with proper naming and descriptions
4. **Complex combinations** of all modifier types

## Key Improvements

### 1. **RollType Enum**
```python
class RollType(Enum):
    NORMAL = "normal"
    ADVANTAGE = "advantage" 
    DISADVANTAGE = "disadvantage"
```
- Prevents impossible combinations like advantage + disadvantage
- Clear, explicit roll type specification

### 2. **DiceModifier Class**
```python
@dataclass
class DiceModifier:
    name: str
    dice: str  # e.g., "1d4", "1d6", "1d8"
    description: str = ""
```
- Supports any dice combination (1d4, 2d6, 1d12, etc.)
- Properly tracks what each modifier represents
- Automatic dice rolling with full result tracking

### 3. **FlatModifier Class**
```python
@dataclass  
class FlatModifier:
    name: str
    value: int
    description: str = ""
```
- Named modifiers instead of anonymous integers
- Support for multiple flat bonuses/penalties
- Clear tracking of modifier sources

### 4. **Flexible String Parser**
The system accepts natural language modifier strings:

```
"advantage +2 guidance:1d4 bardic:1d6"
"disadvantage bless:1d4 -1" 
"+3 inspiration:1d4"
```

## Usage Examples

### Basic Rolls
```python
# Normal skill check
roll_skill_check("athletics")

# With advantage
roll_skill_check("perception", "advantage")

# With disadvantage  
roll_skill_check("stealth", "disadvantage")
```

### Flat Modifiers
```python
# Simple bonus
roll_ability_check("str", "+3")

# Multiple flat modifiers
roll_skill_check("persuasion", "+2 -1")  # Net +1
```

### Dice Modifiers
```python
# Guidance cantrip
roll_skill_check("investigation", "guidance:1d4")

# Bardic inspiration
roll_skill_check("performance", "bardic:1d8")

# Multiple dice
roll_saving_throw("wis", "bless:1d4 guidance:1d4")
```

### Complex Combinations
```python
# Everything together
roll_skill_check("athletics", "advantage +2 bardic:1d8 guidance:1d4")

# Disadvantage with bonuses to compensate
roll_skill_check("stealth", "disadvantage +1 guidance:1d4 bless:1d4")
```

## Output Format

The new system provides comprehensive roll breakdowns:

```json
{
  "roll_name": "Athletics Check",
  "d20_roll": {
    "result": 15,
    "rolls": [15, 8],
    "type": "advantage", 
    "used_roll": 15
  },
  "base_modifier": 6,
  "flat_modifiers": [
    {
      "name": "Magic Weapon",
      "value": 2,
      "description": "Enhancement bonus"
    }
  ],
  "dice_modifiers": [
    {
      "name": "Bardic",
      "dice": "1d8", 
      "rolls": [6],
      "total": 6,
      "description": "Bardic dice"
    }
  ],
  "total": 29,
  "breakdown": "15 (d20) + 6 (base) + +2 (Magic Weapon) + 6 (Bardic) = 29"
}
```

## Common D&D Modifiers

### Dice-Based Modifiers
- **Bardic Inspiration**: 1d6/1d8/1d10/1d12 (scales with bard level)
- **Guidance**: 1d4 (cantrip for ability checks)
- **Bless**: 1d4 (spell for attacks and saves)  
- **Inspiration**: 1d4 (DM-granted inspiration)

### Advantage/Disadvantage Sources
- **Enhance Ability**: Advantage on specific ability checks
- **Help Action**: Advantage when ally assists
- **Flanking**: Advantage on attack rolls (optional rule)
- **Environmental**: Various situational modifiers

### Flat Modifiers
- **Magic Items**: Enhancement bonuses (+1, +2, +3)
- **Spells**: Various spell effects with flat bonuses
- **Class Features**: Expertise, fighting styles, etc.
- **Environmental**: Cover penalties, situational modifiers

## Benefits

1. **Realistic D&D Mechanics**: Matches actual tabletop play
2. **Clear Breakdowns**: See exactly what contributed to each roll
3. **Flexible Input**: Natural language modifier strings
4. **Extensible**: Easy to add new modifier types
5. **Comprehensive Tracking**: Full audit trail of all bonuses
6. **Type Safety**: Prevents invalid combinations

## Migration

Old API calls still work but are deprecated:
```python
# Old (still works)
roll_skill_check("athletics", advantage=True, modifier=2)

# New (preferred)
roll_skill_check("athletics", "advantage +2")
```

The new system is fully backward compatible while providing much more flexibility and realism.
