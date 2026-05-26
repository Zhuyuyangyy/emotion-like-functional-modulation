"""
Affective Memory: 情感权重记忆，存储和管理经历对行为的持久影响
基于情感记忆理论：高强度经历产生更强的记忆印记
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime
import json


@dataclass
class AffectiveMemory:
    event_type: str
    risk_category: str
    emotional_intensity: float
    threat_score: float
    outcome: str
    source: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        return {
            "event_type": self.event_type,
            "risk_category": self.risk_category,
            "emotional_intensity": self.emotional_intensity,
            "threat_score": self.threat_score,
            "outcome": self.outcome,
            "source": self.source,
            "timestamp": self.timestamp
        }

    def __str__(self) -> str:
        return (f"AffectiveMemory({self.event_type}, intensity={self.emotional_intensity:.2f}, "
                f"threat={self.threat_score:.2f}, outcome={self.outcome})")


class AffectiveMemoryStore:
    SIMILARITY_THRESHOLD = 0.6
    DECAY_RATE = 0.02
    MIN_INTENSITY = 0.1

    def __init__(self):
        self.memories: List[AffectiveMemory] = []
        self.category_threat_map: Dict[str, float] = {}
        self.source_trust_map: Dict[str, float] = {}

    def write(self, memory: AffectiveMemory) -> None:
        existing = self._find_similar_memory(memory)
        if existing:
            memory.emotional_intensity = max(
                existing.emotional_intensity * 0.7,
                memory.emotional_intensity
            )
            memory.threat_score = max(existing.threat_score, memory.threat_score)
            self.memories.remove(existing)

        self.memories.append(memory)
        self._update_threat_map(memory)
        if memory.source:
            self._update_source_trust(memory)

    def retrieve(
        self,
        event_type: str,
        risk_category: str,
        limit: int = 5
    ) -> List[AffectiveMemory]:
        scored_memories = []
        for mem in self.memories:
            similarity = self._calculate_similarity(mem, event_type, risk_category)
            if similarity >= self.SIMILARITY_THRESHOLD:
                decay_factor = math.exp(-self.DECAY_RATE * self._memory_age(mem))
                effective_intensity = mem.emotional_intensity * decay_factor
                scored_memories.append((mem, effective_intensity * similarity))

        scored_memories.sort(key=lambda x: x[1], reverse=True)
        return [mem for mem, _ in scored_memories[:limit]]

    def get_threat_score(self, risk_category: str, event_type: str) -> float:
        key = f"{event_type}:{risk_category}"
        return self.category_threat_map.get(key, 0.0)

    def get_source_trust(self, source: str) -> float:
        return self.source_trust_map.get(source, 1.0)

    def recover_source_trust(self, source: str, increment: float) -> float:
        current = self.source_trust_map.get(source, 1.0)
        new_trust = min(current + increment, 1.0)
        self.source_trust_map[source] = new_trust
        return new_trust

    def decay_memories(self) -> None:
        for mem in self.memories:
            mem.emotional_intensity = max(
                mem.emotional_intensity - self.DECAY_RATE,
                self.MIN_INTENSITY
            )
            mem.threat_score = max(
                mem.threat_score - self.DECAY_RATE * 0.5,
                0.0
            )

        for key in list(self.category_threat_map.keys()):
            self.category_threat_map[key] = max(
                self.category_threat_map[key] - self.DECAY_RATE * 0.3,
                0.0
            )

    def get_all_memories(self) -> List[AffectiveMemory]:
        return self.memories.copy()

    def _find_similar_memory(self, memory: AffectiveMemory) -> Optional[AffectiveMemory]:
        for mem in self.memories:
            if (mem.risk_category == memory.risk_category and
                mem.event_type == memory.event_type and
                mem.source == memory.source):
                return mem
        return None

    def _calculate_similarity(
        self,
        memory: AffectiveMemory,
        event_type: str,
        risk_category: str
    ) -> float:
        type_match = 1.0 if memory.event_type == event_type else 0.0
        category_match = 1.0 if memory.risk_category == risk_category else 0.5

        return (type_match * 0.6 + category_match * 0.4)

    def _memory_age(self, memory: AffectiveMemory) -> float:
        return len(self.memories) * 0.1

    def _update_threat_map(self, memory: AffectiveMemory) -> None:
        key = f"{memory.event_type}:{memory.risk_category}"
        current = self.category_threat_map.get(key, 0.0)
        self.category_threat_map[key] = max(current, memory.threat_score)

    def _update_source_trust(self, memory: AffectiveMemory) -> None:
        if not memory.source:
            return

        current = self.source_trust_map.get(memory.source, 1.0)
        if memory.outcome == "negative":
            self.source_trust_map[memory.source] = current * 0.5
        elif memory.outcome == "positive":
            self.source_trust_map[memory.source] = min(current + 0.1, 1.0)


import math
