"""
Tests for EventParser
"""

import sys
sys.path.insert(0, '/workspace/src')

import pytest
from affective_agent.event_parser import EventParser, EventType


class TestEventParser:
    def test_parse_delete_event(self):
        parser = EventParser()
        event = parser.parse("delete file /tmp/test.txt")

        assert event.event_type == EventType.DELETE
        assert event.is_potentially_destructive == True
        assert event.risk_category == "filesystem"

    def test_parse_batch_delete(self):
        parser = EventParser()
        event = parser.parse("batch delete records")

        assert event.event_type == EventType.DELETE
        assert event.is_batched == True
        assert event.requires_confirmation == True

    def test_parse_read_event(self):
        parser = EventParser()
        event = parser.parse("read file /tmp/test.txt")

        assert event.event_type == EventType.READ
        assert event.is_potentially_destructive == False

    def test_parse_update_event(self):
        parser = EventParser()
        event = parser.parse("update database table")

        assert event.event_type == EventType.UPDATE
        assert event.risk_category == "database"

    def test_parse_force_overwrite(self):
        parser = EventParser()
        event = parser.parse("force overwrite file /data/config")

        assert event.is_potentially_destructive == True
        assert event.requires_confirmation == True

    def test_parse_unknown_event(self):
        parser = EventParser()
        event = parser.parse("do something unknown")

        assert event.event_type == EventType.OTHER
        assert event.target_resource == "unknown"

    def test_parse_execute_event(self):
        parser = EventParser()
        event = parser.parse("execute script /tmp/run.sh")

        assert event.event_type == EventType.EXECUTE

    def test_parse_query_event(self):
        parser = EventParser()
        event = parser.parse("query database for records")

        assert event.event_type == EventType.QUERY
        assert event.risk_category == "database"
