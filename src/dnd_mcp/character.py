import json
from typing import List, Dict, Any, Optional


class Character:
    def __init__(self):
        # Basic character info
        self.name: Optional[str] = None
        self.nickname: Optional[str] = None
        
        # Required fields
        self.player: Dict[str, Any] = {"name": "NPC", "id": None}
        self.race: Dict[str, Any] = {}
        
        # Character progression
        self.xp: int = 0
        self.classes: List[Dict[str, Any]] = []
        
        # Character details
        self.alignment: Optional[str] = None
        self.background: Dict[str, Any] = {}
        self.details: Dict[str, Any] = {}
        
        # Combat stats
        self.hit_points: Dict[str, int] = {"max": 0, "current": 0}
        self.armor_class: Dict[str, Any] = {"value": 10, "description": ""}
        self.ability_scores: Dict[str, int] = {
            "str": 10, "dex": 10, "con": 10, 
            "int": 10, "wis": 10, "cha": 10
        }
        self.saving_throws: Dict[str, bool] = {}
        self.skills: Dict[str, bool] = {}
        self.speed: Dict[str, int] = {"Walk": 30}
        
        # Proficiencies
        self.weapon_proficiencies: List[str] = []
        self.armor_proficiencies: List[str] = []
        self.tool_proficiencies: List[str] = []
        
        # Features and abilities
        self.feats: List[Dict[str, Any]] = []
        self.spells: List[Dict[str, Any]] = []
        self.weapons: List[Dict[str, Any]] = []
        self.equipment: List[Dict[str, Any]] = []
        
        # Languages and treasure
        self.languages: List[str] = []
        self.treasure: Dict[str, float] = {
            "pp": 0, "ep": 0, "gp": 0, "sp": 0, "cp": 0
        }
    
    def load(self, file_path: str) -> None:
        """Load character data from a JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self._load_from_dict(data)
        except FileNotFoundError:
            raise FileNotFoundError(f"Character file not found: {file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in character file: {e}")
    
    def load_from_json(self, json_string: str) -> None:
        """Load character data from a JSON string."""
        try:
            data = json.loads(json_string)
            self._load_from_dict(data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON string: {e}")
    
    def _load_from_dict(self, data: Dict[str, Any]) -> None:
        """Load character data from a dictionary."""
        # Basic info
        self.name = data.get("name")
        self.nickname = data.get("nickname")
        
        # Player info (required)
        if "player" in data:
            self.player = {
                "name": data["player"].get("name", "NPC"),
                "id": data["player"].get("id")
            }
        
        # Race (required)
        self.race = data.get("race", {})
        
        # Experience and classes
        self.xp = data.get("xp", 0)
        self.classes = data.get("classes", [])
        
        # Character details
        self.alignment = data.get("alignment")
        self.background = data.get("background", {})
        self.details = data.get("details", {})
        
        # Combat stats
        self.hit_points = data.get("hit_points", {"max": 0, "current": 0})
        self.armor_class = data.get("armor_class", {"value": 10, "description": ""})
        self.ability_scores = data.get("ability_scores", {
            "str": 10, "dex": 10, "con": 10, 
            "int": 10, "wis": 10, "cha": 10
        })
        self.saving_throws = data.get("saving_throws", {})
        self.skills = data.get("skills", {})
        self.speed = data.get("speed", {"Walk": 30})
        
        # Proficiencies
        self.weapon_proficiencies = data.get("weapon_proficiencies", [])
        self.armor_proficiencies = data.get("armor_proficiencies", [])
        self.tool_proficiencies = data.get("tool_proficiencies", [])
        
        # Features and abilities
        self.feats = data.get("feats", [])
        self.spells = data.get("spells", [])
        self.weapons = data.get("weapons", [])
        self.equipment = data.get("equipment", [])
        
        # Languages and treasure
        self.languages = data.get("languages", [])
        self.treasure = data.get("treasure", {
            "pp": 0, "ep": 0, "gp": 0, "sp": 0, "cp": 0
        })
    
    def write(self, file_path: str, indent: int = 4) -> None:
        """Write character data to a JSON file."""
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(self.to_dict(), file, indent=indent, ensure_ascii=False)
        except IOError as e:
            raise IOError(f"Error writing character file: {e}")
    
    def to_json(self, indent: int = 4) -> str:
        """Convert character data to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert character data to dictionary, excluding None values where appropriate."""
        character_dict = {}
        
        # Add non-None basic fields
        if self.name is not None:
            character_dict["name"] = self.name
        if self.nickname is not None:
            character_dict["nickname"] = self.nickname
        
        # Always include required fields
        character_dict["player"] = self.player
        character_dict["race"] = self.race
        
        # Add other fields if they have meaningful values
        if self.xp > 0:
            character_dict["xp"] = self.xp
        
        if self.classes:
            character_dict["classes"] = self.classes
        
        if self.alignment:
            character_dict["alignment"] = self.alignment
        
        if self.background:
            character_dict["background"] = self.background
        
        if self.details:
            character_dict["details"] = self.details
        
        # Combat stats
        character_dict["hit_points"] = self.hit_points
        character_dict["armor_class"] = self.armor_class
        character_dict["ability_scores"] = self.ability_scores
        
        if self.saving_throws:
            character_dict["saving_throws"] = self.saving_throws
        
        if self.skills:
            character_dict["skills"] = self.skills
        
        character_dict["speed"] = self.speed
        
        # Proficiencies (only if not empty)
        if self.weapon_proficiencies:
            character_dict["weapon_proficiencies"] = self.weapon_proficiencies
        
        if self.armor_proficiencies:
            character_dict["armor_proficiencies"] = self.armor_proficiencies
        
        if self.tool_proficiencies:
            character_dict["tool_proficiencies"] = self.tool_proficiencies
        
        # Features and abilities (only if not empty)
        if self.feats:
            character_dict["feats"] = self.feats
        
        if self.spells:
            character_dict["spells"] = self.spells
        
        if self.weapons:
            character_dict["weapons"] = self.weapons
        
        if self.equipment:
            character_dict["equipment"] = self.equipment
        
        # Languages and treasure (only if not empty/zero)
        if self.languages:
            character_dict["languages"] = self.languages
        
        if any(value > 0 for value in self.treasure.values()):
            character_dict["treasure"] = self.treasure
        
        return character_dict
    
    def get_level(self) -> int:
        """Calculate total character level from all classes."""
        return sum(cls.get("level", 0) for cls in self.classes)
    
    def get_ability_modifier(self, ability: str) -> int:
        """Calculate ability modifier for a given ability score."""
        score = self.ability_scores.get(ability.lower(), 10)
        return (score - 10) // 2
    
    def get_proficiency_bonus(self) -> int:
        """Calculate proficiency bonus based on character level."""
        level = self.get_level()
        return 2 + ((level - 1) // 4)
    
    def __str__(self) -> str:
        """String representation of the character."""
        name = self.name or "Unnamed Character"
        race = self.race.get("name", "Unknown Race")
        classes_str = ", ".join([f"{cls.get('name', 'Unknown')} {cls.get('level', 1)}" 
                                for cls in self.classes])
        level = self.get_level()
        
        return f"{name} - Level {level} {race} ({classes_str})"
    
    def __repr__(self) -> str:
        """Developer representation of the character."""
        return f"Character(name='{self.name}', level={self.get_level()})"