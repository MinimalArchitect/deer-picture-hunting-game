import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

class ScoreEntry:
    """Represents a single score entry"""
    def __init__(self, player_name: str, score: int, level: int, 
                 date: str = None, time_taken: float = 0):
        self.player_name = player_name
        self.score = score
        self.level = level
        self.date = date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_taken = max(0, float(time_taken))  # Ensure it's a positive float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'player_name': self.player_name,
            'score': self.score,
            'level': self.level,
            'date': self.date,
            'time_taken': float(self.time_taken)  # Ensure it's saved as float
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ScoreEntry':
        """Create ScoreEntry from dictionary"""
        return cls(
            player_name=data.get('player_name', 'Anonymous'),
            score=data.get('score', 0),
            level=data.get('level', 1),
            date=data.get('date', ''),
            time_taken=float(data.get('time_taken', 0))  # Ensure it's a float
        )

class ScoreManager:
    """Manages high scores for the game"""
    
    def __init__(self, scores_file: str = "level_scores.json"):
        self.scores_file = scores_file
        self.scores = self._load_scores()
        self.current_player_name = "Player"  # Default name
    
    def _load_scores(self) -> Dict[int, List[ScoreEntry]]:
        """Load scores from JSON file"""
        if not os.path.exists(self.scores_file):
            return {}
        
        try:
            with open(self.scores_file, 'r') as f:
                data = json.load(f)
            
            # Convert from old format if necessary
            scores = {}
            for level_str, entries in data.items():
                level = int(level_str)
                if isinstance(entries, list):
                    # New format
                    scores[level] = [ScoreEntry.from_dict(entry) for entry in entries]
                else:
                    # Old format - single score
                    scores[level] = [ScoreEntry("Legacy Player", entries, level)]
            
            return scores
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            print(f"Error loading scores: {e}")
            return {}
    
    def _save_scores(self):
        """Save scores to JSON file"""
        try:
            # Convert ScoreEntry objects to dictionaries
            data = {}
            for level, entries in self.scores.items():
                data[str(level)] = [entry.to_dict() for entry in entries]
            
            with open(self.scores_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving scores: {e}")
    
    def add_score(self, level: int, score: int, time_taken: float = 0, 
              player_name: str = None) -> bool:
        """Add a new score entry"""
        if player_name is None:
            player_name = self.current_player_name
        
        # Ensure we have valid data
        player_name = player_name.strip() if player_name else "Player"
        time_taken = float(time_taken) if time_taken else 0.0
        
        print(f"ScoreManager.add_score called: Level={level}, Player='{player_name}', Score={score}, Time={time_taken:.2f}")
        
        if level not in self.scores:
            self.scores[level] = []
        
        new_entry = ScoreEntry(player_name, score, level, time_taken=time_taken)
        print(f"Created ScoreEntry: name='{new_entry.player_name}', score={new_entry.score}, time={new_entry.time_taken}")
        
        self.scores[level].append(new_entry)
        
        # Keep only top 10 scores per level
        self.scores[level].sort(key=lambda x: (-x.score, x.time_taken))
        self.scores[level] = self.scores[level][:10]
        
        self._save_scores()
        
        # Verify the save worked
        print(f"Score saved. Scores for level {level}: {len(self.scores[level])} entries")
        return True
    
    def get_high_scores(self, level: int, limit: int = 10) -> List[ScoreEntry]:
        """Get high scores for a specific level"""
        if level not in self.scores:
            return []
        
        # Sort by score (descending), then by time (ascending)
        sorted_scores = sorted(self.scores[level], 
                             key=lambda x: (-x.score, x.time_taken))
        return sorted_scores[:limit]
    
    def get_all_high_scores(self) -> Dict[int, List[ScoreEntry]]:
        """Get all high scores for all levels"""
        return self.scores.copy()
    
    def get_personal_best(self, level: int, player_name: str = None) -> Optional[ScoreEntry]:
        """Get personal best score for a player on a specific level"""
        if player_name is None:
            player_name = self.current_player_name
        
        if level not in self.scores:
            return None
        
        player_scores = [entry for entry in self.scores[level] 
                        if entry.player_name == player_name]
        
        if not player_scores:
            return None
        
        return max(player_scores, key=lambda x: x.score)
    
    def is_high_score(self, level: int, score: int) -> bool:
        """Check if a score would be a high score"""
        high_scores = self.get_high_scores(level, 10)
        
        if len(high_scores) < 10:
            return True
        
        return score > min(entry.score for entry in high_scores)
    
    def get_level_record(self, level: int) -> Optional[ScoreEntry]:
        """Get the record (highest score) for a level"""
        high_scores = self.get_high_scores(level, 1)
        return high_scores[0] if high_scores else None
    
    def set_player_name(self, name: str):
        """Set current player name"""
        self.current_player_name = name.strip() or "Player"
    
    def get_player_name(self) -> str:
        """Get current player name"""
        return self.current_player_name