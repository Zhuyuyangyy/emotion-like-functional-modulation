"""
Event Parser: 解析行为事件，提取关键属性用于后果评估
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum


class EventType(Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    EXECUTE = "execute"
    QUERY = "query"
    TRANSFER = "transfer"
    GRANT = "grant"
    OTHER = "other"


@dataclass
class ParsedEvent:
    raw_description: str
    event_type: EventType
    target_resource: str
    risk_category: str
    is_potentially_destructive: bool
    is_reversible: bool
    is_batched: bool
    requires_confirmation: bool


class EventParser:
    DESTRUCTIVE_PATTERNS = [
        "delete", "drop", "remove", "truncate", "rm", "del",
        "overwrite", "force", "cascade", "purge", "wipe"
    ]

    BATCH_PATTERNS = [
        "batch", "bulk", "mass", "multi", "all", "*", "?"
    ]

    def __init__(self):
        self.event_type_keywords = {
            EventType.CREATE: ["create", "new", "add", "insert", "mkdir", "touch"],
            EventType.READ: ["read", "get", "fetch", "select", "show", "list", "cat", "view"],
            EventType.UPDATE: ["update", "edit", "modify", "set", "replace", "patch"],
            EventType.DELETE: ["delete", "drop", "remove", "rm", "truncate"],
            EventType.EXECUTE: ["run", "execute", "call", "invoke", "apply"],
            EventType.QUERY: ["query", "search", "find", "filter"],
            EventType.TRANSFER: ["move", "copy", "mv", "cp", "transfer", "send"],
            EventType.GRANT: ["grant", "permission", "chmod", "chown", "allow"],
        }

    def parse(self, event_description: str) -> ParsedEvent:
        description_lower = event_description.lower()

        event_type = self._detect_event_type(description_lower)
        target_resource = self._extract_target_resource(description_lower)
        risk_category = self._categorize_risk(description_lower)
        is_destructive = self._is_destructive(description_lower)
        is_reversible = self._is_reversible(description_lower, event_type)
        is_batched = self._is_batched(description_lower)
        requires_confirmation = self._requires_confirmation(is_destructive, is_batched)

        return ParsedEvent(
            raw_description=event_description,
            event_type=event_type,
            target_resource=target_resource,
            risk_category=risk_category,
            is_potentially_destructive=is_destructive,
            is_reversible=is_reversible,
            is_batched=is_batched,
            requires_confirmation=requires_confirmation
        )

    def _detect_event_type(self, description: str) -> EventType:
        for event_type, keywords in self.event_type_keywords.items():
            if any(kw in description for kw in keywords):
                return event_type
        return EventType.OTHER

    def _extract_target_resource(self, description: str) -> str:
        for pattern in ["file", "table", "database", "user", "role", "resource"]:
            if pattern in description:
                return pattern
        return "unknown"

    def _categorize_risk(self, description: str) -> str:
        if any(p in description for p in ["file", "filesystem"]):
            return "filesystem"
        elif any(p in description for p in ["database", "table", "db"]):
            return "database"
        elif any(p in description for p in ["permission", "user", "role", "auth"]):
            return "security"
        elif any(p in description for p in ["network", "http", "api", "transfer"]):
            return "network"
        return "general"

    def _is_destructive(self, description: str) -> bool:
        return any(pattern in description for pattern in self.DESTRUCTIVE_PATTERNS)

    def _is_reversible(self, description: str, event_type: EventType) -> bool:
        if event_type == EventType.DELETE:
            return False
        if "overwrite" in description:
            return True
        return True

    def _is_batched(self, description: str) -> bool:
        return any(pattern in description for pattern in self.BATCH_PATTERNS)

    def _requires_confirmation(self, is_destructive: bool, is_batched: bool) -> bool:
        return is_destructive or is_batched
