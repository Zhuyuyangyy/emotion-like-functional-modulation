"""
V0.2 - Experience Memory Module

Experience storage and retrieval system. Maintains a memory of past experiences
with emotional tags for recall and pattern matching.
"""

import json
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any


@dataclass
class Experience:
    """Represents a single experience with emotional context."""
    
    id: str
    timestamp: float
    context: str
    emotion_category: str
    valence: float
    arousal: float
    dominance: float
    intensity: float
    tags: List[str]
    summary: str
    duration: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert experience to dictionary."""
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "context": self.context,
            "emotion_category": self.emotion_category,
            "valence": self.valence,
            "arousal": self.arousal,
            "dominance": self.dominance,
            "intensity": self.intensity,
            "tags": self.tags,
            "summary": self.summary,
            "duration": self.duration
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Experience':
        """Create experience from dictionary."""
        return cls(
            id=data["id"],
            timestamp=data["timestamp"],
            context=data["context"],
            emotion_category=data["emotion_category"],
            valence=data["valence"],
            arousal=data["arousal"],
            dominance=data["dominance"],
            intensity=data["intensity"],
            tags=data["tags"],
            summary=data["summary"],
            duration=data.get("duration", 0.0)
        )


class ExperienceMemory:
    """
    Memory system for storing and retrieving experiences.
    
    Features:
    - Episodic memory storage
    - Emotional context indexing
    - Pattern matching for recall
    - Memory consolidation over time
    """
    
    def __init__(self, max_capacity: int = 1000):
        self._experiences: List[Experience] = []
        self._max_capacity = max_capacity
        self._tag_index: Dict[str, List[str]] = {}
        self._emotion_index: Dict[str, List[str]] = {}
    
    def _generate_id(self) -> str:
        """Generate a unique experience ID."""
        return f"exp_{int(time.time() * 1000)}_{len(self._experiences)}"
    
    def add_experience(
        self,
        context: str,
        emotion_category: str,
        valence: float,
        arousal: float,
        dominance: float,
        intensity: float,
        tags: Optional[List[str]] = None,
        summary: str = "",
        duration: float = 0.0
    ) -> str:
        """
        Add a new experience to memory.
        
        Args:
            context: Description of the experience
            emotion_category: Emotion associated with this experience
            valence: Valence dimension (-1 to +1)
            arousal: Arousal dimension (-1 to +1)
            dominance: Dominance dimension (-1 to +1)
            intensity: Emotional intensity (0 to 1)
            tags: Optional tags for categorization
            summary: Brief summary of the experience
            duration: Duration of the experience in seconds
        
        Returns:
            The ID of the added experience
        """
        experience_id = self._generate_id()
        experience = Experience(
            id=experience_id,
            timestamp=time.time(),
            context=context,
            emotion_category=emotion_category,
            valence=valence,
            arousal=arousal,
            dominance=dominance,
            intensity=intensity,
            tags=tags or [],
            summary=summary,
            duration=duration
        )
        
        self._experiences.append(experience)
        
        # Update indexes
        for tag in experience.tags:
            if tag not in self._tag_index:
                self._tag_index[tag] = []
            self._tag_index[tag].append(experience_id)
        
        if emotion_category not in self._emotion_index:
            self._emotion_index[emotion_category] = []
        self._emotion_index[emotion_category].append(experience_id)
        
        # Enforce capacity limit
        self._enforce_capacity()
        
        return experience_id
    
    def _enforce_capacity(self) -> None:
        """Remove oldest experiences if capacity is exceeded."""
        while len(self._experiences) > self._max_capacity:
            oldest = self._experiences.pop(0)
            # Remove from indexes
            for tag in oldest.tags:
                if tag in self._tag_index and oldest.id in self._tag_index[tag]:
                    self._tag_index[tag].remove(oldest.id)
            if oldest.emotion_category in self._emotion_index:
                if oldest.id in self._emotion_index[oldest.emotion_category]:
                    self._emotion_index[oldest.emotion_category].remove(oldest.id)
    
    def retrieve_by_emotion(self, emotion_category: str) -> List[Experience]:
        """Retrieve all experiences with a specific emotion category."""
        if emotion_category not in self._emotion_index:
            return []
        
        result = []
        for exp_id in self._emotion_index[emotion_category]:
            exp = self._get_experience_by_id(exp_id)
            if exp:
                result.append(exp)
        return result
    
    def retrieve_by_tags(self, tags: List[str]) -> List[Experience]:
        """Retrieve experiences matching any of the given tags."""
        matched_ids = set()
        for tag in tags:
            if tag in self._tag_index:
                matched_ids.update(self._tag_index[tag])
        
        result = []
        for exp_id in matched_ids:
            exp = self._get_experience_by_id(exp_id)
            if exp:
                result.append(exp)
        return result
    
    def retrieve_recent(self, limit: int = 10) -> List[Experience]:
        """Retrieve most recent experiences."""
        return list(reversed(self._experiences[-limit:]))
    
    def _get_experience_by_id(self, exp_id: str) -> Optional[Experience]:
        """Find experience by ID."""
        for exp in self._experiences:
            if exp.id == exp_id:
                return exp
        return None
    
    def retrieve_similar(self, valence: float, arousal: float, dominance: float, 
                        threshold: float = 0.5) -> List[Tuple[Experience, float]]:
        """
        Retrieve experiences with similar emotional state.
        
        Args:
            valence: Target valence
            arousal: Target arousal
            dominance: Target dominance
            threshold: Similarity threshold (0-1, higher = more similar)
        
        Returns:
            List of (experience, similarity_score) tuples
        """
        results = []
        for exp in self._experiences:
            similarity = self._emotional_similarity(
                (valence, arousal, dominance),
                (exp.valence, exp.arousal, exp.dominance)
            )
            if similarity >= threshold:
                results.append((exp, similarity))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return results
    
    def _emotional_similarity(self, vec1: Tuple[float, float, float], 
                             vec2: Tuple[float, float, float]) -> float:
        """Calculate cosine similarity between two emotional state vectors."""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = sum(a ** 2 for a in vec1) ** 0.5
        magnitude2 = sum(b ** 2 for b in vec2) ** 0.5
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def consolidate(self) -> None:
        """
        Consolidate memories - reduce redundant memories and strengthen important ones.
        This is a simplified version that removes very similar recent experiences.
        """
        if len(self._experiences) < 2:
            return
        
        to_remove = set()
        recent = self._experiences[-50:]  # Check last 50 experiences
        
        for i, exp1 in enumerate(recent):
            for j, exp2 in enumerate(recent[i+1:], start=i+1):
                if exp1.id == exp2.id:
                    continue
                similarity = self._emotional_similarity(
                    (exp1.valence, exp1.arousal, exp1.dominance),
                    (exp2.valence, exp2.arousal, exp2.dominance)
                )
                if similarity > 0.9 and exp1.context == exp2.context:
                    to_remove.add(exp2.id)
        
        self._experiences = [exp for exp in self._experiences if exp.id not in to_remove]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get memory statistics."""
        emotion_counts = {}
        for exp in self._experiences:
            emotion_counts[exp.emotion_category] = emotion_counts.get(exp.emotion_category, 0) + 1
        
        return {
            "total_experiences": len(self._experiences),
            "emotion_distribution": emotion_counts,
            "tag_count": len(self._tag_index),
            "average_intensity": sum(exp.intensity for exp in self._experiences) / max(1, len(self._experiences))
        }
    
    def to_json(self) -> str:
        """Serialize memory to JSON."""
        return json.dumps({
            "experiences": [exp.to_dict() for exp in self._experiences],
            "max_capacity": self._max_capacity,
            "statistics": self.get_statistics()
        }, indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'ExperienceMemory':
        """Deserialize memory from JSON."""
        data = json.loads(json_str)
        memory = cls(max_capacity=data.get("max_capacity", 1000))
        
        for exp_data in data.get("experiences", []):
            exp = Experience.from_dict(exp_data)
            memory._experiences.append(exp)
            
            for tag in exp.tags:
                if tag not in memory._tag_index:
                    memory._tag_index[tag] = []
                memory._tag_index[tag].append(exp.id)
            
            if exp.emotion_category not in memory._emotion_index:
                memory._emotion_index[exp.emotion_category] = []
            memory._emotion_index[exp.emotion_category].append(exp.id)
        
        return memory
    
    def clear(self) -> None:
        """Clear all memories."""
        self._experiences = []
        self._tag_index = {}
        self._emotion_index = {}
    
    def __len__(self) -> int:
        return len(self._experiences)
