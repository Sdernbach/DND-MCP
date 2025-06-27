"""
Dice rolling and modifier system for D&D 5e.

This module provides classes and functions for handling complex D&D 5e dice rolls
including advantage, disadvantage, and various modifiers like bardic inspiration.
"""

import random
from typing import Dict, List, Any
from enum import Enum
from dataclasses import dataclass


class RollType(Enum):
    """Type of d20 roll"""
    NORMAL = "normal"
    ADVANTAGE = "advantage"
    DISADVANTAGE = "disadvantage"


@dataclass
class DiceModifier:
    """Represents a dice modifier like bardic inspiration, guidance, etc."""
    name: str
    dice: str  # e.g., "1d4", "1d6", "1d8", "1d10", "1d12"
    description: str = ""
    
    def roll(self) -> Dict[str, Any]:
        """Roll this dice modifier"""
        # Parse dice string (e.g., "1d6" -> num=1, sides=6)
        if 'd' not in self.dice:
            raise ValueError(f"Invalid dice format: {self.dice}")
        
        num_str, sides_str = self.dice.split('d')
        num_dice = int(num_str) if num_str else 1
        sides = int(sides_str)
        
        rolls = [random.randint(1, sides) for _ in range(num_dice)]
        total = sum(rolls)
        
        return {
            "name": self.name,
            "dice": self.dice,
            "rolls": rolls,
            "total": total,
            "description": self.description
        }


@dataclass
class FlatModifier:
    """Represents a flat numeric modifier"""
    name: str
    value: int
    description: str = ""


@dataclass
class RollModifiers:
    """Collection of all modifiers for a roll"""
    flat_modifiers: List[FlatModifier] = None
    dice_modifiers: List[DiceModifier] = None
    roll_type: RollType = RollType.NORMAL
    
    def __post_init__(self):
        if self.flat_modifiers is None:
            self.flat_modifiers = []
        if self.dice_modifiers is None:
            self.dice_modifiers = []
    
    def get_flat_total(self) -> int:
        """Get total of all flat modifiers"""
        return sum(mod.value for mod in self.flat_modifiers)
    
    def roll_dice_modifiers(self) -> List[Dict[str, Any]]:
        """Roll all dice modifiers and return results"""
        return [mod.roll() for mod in self.dice_modifiers]
    
    def get_dice_total(self) -> int:
        """Get total from all dice modifier rolls"""
        return sum(result["total"] for result in self.roll_dice_modifiers())


def roll_d20(roll_type: RollType = RollType.NORMAL) -> Dict[str, Any]:
    """Roll a d20 with optional advantage/disadvantage"""
    roll1 = random.randint(1, 20)
    
    if roll_type == RollType.ADVANTAGE:
        roll2 = random.randint(1, 20)
        result = max(roll1, roll2)
        return {
            "result": result,
            "rolls": [roll1, roll2],
            "type": roll_type.value,
            "used_roll": result
        }
    elif roll_type == RollType.DISADVANTAGE:
        roll2 = random.randint(1, 20)
        result = min(roll1, roll2)
        return {
            "result": result,
            "rolls": [roll1, roll2], 
            "type": roll_type.value,
            "used_roll": result
        }
    else:  # NORMAL
        return {
            "result": roll1,
            "rolls": [roll1],
            "type": roll_type.value,
            "used_roll": roll1
        }


def perform_roll(base_modifier: int, modifiers: RollModifiers, roll_name: str) -> Dict[str, Any]:
    """Perform a complete roll with all modifiers"""
    # Roll the d20
    d20_result = roll_d20(modifiers.roll_type)
    
    # Roll dice modifiers
    dice_results = modifiers.roll_dice_modifiers()
    dice_total = sum(result["total"] for result in dice_results)
    
    # Calculate totals
    flat_total = modifiers.get_flat_total()
    total = d20_result["result"] + base_modifier + flat_total + dice_total
    
    # Build breakdown string
    breakdown_parts = [f"{d20_result['result']} (d20)"]
    if base_modifier != 0:
        breakdown_parts.append(f"{base_modifier} (base)")
    
    for mod in modifiers.flat_modifiers:
        sign = "+" if mod.value >= 0 else ""
        breakdown_parts.append(f"{sign}{mod.value} ({mod.name})")
    
    for result in dice_results:
        breakdown_parts.append(f"{result['total']} ({result['name']})")
    
    breakdown = " + ".join(breakdown_parts).replace("+ -", "- ")
    breakdown += f" = {total}"
    
    return {
        "roll_name": roll_name,
        "d20_roll": d20_result,
        "base_modifier": base_modifier,
        "flat_modifiers": [{"name": mod.name, "value": mod.value, "description": mod.description} 
                          for mod in modifiers.flat_modifiers],
        "dice_modifiers": dice_results,
        "total": total,
        "breakdown": breakdown
    }


def parse_modifiers_string(modifiers_str: str) -> RollModifiers:
    """Parse a string of modifiers into RollModifiers object
    
    Format examples:
    - "advantage +2 guidance:1d4 bardic:1d6"
    - "disadvantage -1 bless:1d4"
    - "+3 inspiration:1d4"
    """
    if not modifiers_str:
        return RollModifiers()
    
    parts = modifiers_str.lower().split()
    roll_type = RollType.NORMAL
    flat_mods = []
    dice_mods = []
    
    for part in parts:
        if part == "advantage":
            roll_type = RollType.ADVANTAGE
        elif part == "disadvantage":
            roll_type = RollType.DISADVANTAGE
        elif ":" in part:
            # Dice modifier like "guidance:1d4"
            name, dice = part.split(":", 1)
            dice_mods.append(DiceModifier(name.title(), dice, f"{name.title()} dice"))
        elif part.startswith(("+", "-")) and part[1:].isdigit():
            # Flat modifier like "+2" or "-1"
            value = int(part)
            flat_mods.append(FlatModifier("Modifier", value, f"Flat modifier {part}"))
        elif part.isdigit():
            # Flat modifier without sign
            value = int(part)
            flat_mods.append(FlatModifier("Modifier", value, f"Flat modifier +{part}"))
    
    return RollModifiers(flat_mods, dice_mods, roll_type)
