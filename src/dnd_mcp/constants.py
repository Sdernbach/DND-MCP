"""
Constants and mappings for D&D 5e game mechanics.
"""

from typing import Dict

# D&D 5e skill to ability mapping
SKILL_ABILITIES: Dict[str, str] = {
    "acrobatics": "dex",
    "animal_handling": "wis", 
    "arcana": "int",
    "athletics": "str",
    "deception": "cha",
    "history": "int",
    "insight": "wis",
    "intimidation": "cha",
    "investigation": "int",
    "medicine": "wis",
    "nature": "int",
    "perception": "wis",
    "performance": "cha",
    "persuasion": "cha",
    "religion": "int",
    "sleight_of_hand": "dex",
    "stealth": "dex",
    "survival": "wis"
}

# Common D&D modifiers and their typical dice
COMMON_MODIFIERS = {
    "Bardic Inspiration": {
        "dice": "1d6 (level 1-4), 1d8 (level 5-9), 1d10 (level 10-14), 1d12 (level 15+)",
        "description": "Bard feature to inspire allies"
    },
    "Guidance": {
        "dice": "1d4", 
        "description": "Cantrip that adds to ability checks"
    },
    "Bless": {
        "dice": "1d4",
        "description": "1st level spell affecting attack rolls and saves"
    },
    "Inspiration": {
        "dice": "1d4 (variant rule)",
        "description": "DM-granted inspiration die"
    },
    "Enhance Ability": {
        "dice": "advantage",
        "description": "2nd level spell granting advantage on ability checks"
    },
    "Lucky": {
        "dice": "reroll",
        "description": "Feat allowing rerolls (use advantage/disadvantage)"
    }
}
