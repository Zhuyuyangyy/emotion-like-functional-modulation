"""
Tests for AffectiveMemory
"""

import sys
sys.path.insert(0, '/workspace/src')

import pytest
from affective_agent.affective_memory import AffectiveMemoryStore, AffectiveMemory


class TestAffectiveMemoryStore:
    def test_write_memory(self):
        store = AffectiveMemoryStore()
        memory = AffectiveMemory(
            event_type="delete",
            risk_category="filesystem",
            emotional_intensity=0.8,
            threat_score=0.7,
            outcome="negative"
        )

        store.write(memory)
        memories = store.get_all_memories()

        assert len(memories) == 1
        assert memories[0].event_type == "delete"

    def test_similar_memory_update(self):
        store = AffectiveMemoryStore()

        memory1 = AffectiveMemory(
            event_type="delete",
            risk_category="filesystem",
            emotional_intensity=0.5,
            threat_score=0.5,
            outcome="negative"
        )
        memory2 = AffectiveMemory(
            event_type="delete",
            risk_category="filesystem",
            emotional_intensity=0.8,
            threat_score=0.8,
            outcome="negative"
        )

        store.write(memory1)
        store.write(memory2)

        memories = store.get_all_memories()
        assert len(memories) == 1
        assert memories[0].threat_score == 0.8

    def test_retrieve_memories(self):
        store = AffectiveMemoryStore()

        memories_data = [
            ("delete", "filesystem", 0.8, 0.7),
            ("read", "filesystem", 0.2, 0.1),
            ("delete", "database", 0.6, 0.5),
        ]

        for et, rc, ei, ts in memories_data:
            store.write(AffectiveMemory(
                event_type=et,
                risk_category=rc,
                emotional_intensity=ei,
                threat_score=ts,
                outcome="neutral"
            ))

        retrieved = store.retrieve("delete", "filesystem")
        assert len(retrieved) >= 1

        for mem in retrieved:
            assert mem.event_type == "delete" or mem.risk_category == "filesystem"

    def test_get_threat_score(self):
        store = AffectiveMemoryStore()

        store.write(AffectiveMemory(
            event_type="delete",
            risk_category="filesystem",
            emotional_intensity=0.8,
            threat_score=0.7,
            outcome="negative"
        ))

        threat = store.get_threat_score("filesystem", "delete")
        assert threat == 0.7

    def test_get_threat_score_nonexistent(self):
        store = AffectiveMemoryStore()
        threat = store.get_threat_score("unknown", "unknown")
        assert threat == 0.0

    def test_source_trust_map(self):
        store = AffectiveMemoryStore()

        store.write(AffectiveMemory(
            event_type="execute",
            risk_category="general",
            emotional_intensity=0.8,
            threat_score=0.6,
            outcome="negative",
            source="unreliable_source"
        ))

        trust = store.get_source_trust("unreliable_source")
        assert trust < 1.0

    def test_decay_memories(self):
        store = AffectiveMemoryStore()

        store.write(AffectiveMemory(
            event_type="delete",
            risk_category="filesystem",
            emotional_intensity=0.8,
            threat_score=0.7,
            outcome="negative"
        ))

        initial_intensity = store.get_all_memories()[0].emotional_intensity
        store.decay_memories()
        decayed_intensity = store.get_all_memories()[0].emotional_intensity

        assert decayed_intensity < initial_intensity
