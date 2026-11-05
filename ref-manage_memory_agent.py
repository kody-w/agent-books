import uuid
from datetime import datetime

from agents.basic_agent import BasicAgent

import importlib
import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
import memory_store as _memory_store
_memory_store = importlib.reload(_memory_store)

insert_memory = _memory_store.insert_memory
init_db = _memory_store.init_db


class ManageMemoryAgent(BasicAgent):
    def __init__(self):
        self.name = 'ManageMemory'
        self.metadata = {
            "name": self.name,
            "description": "Saves information to persistent memory for future conversations. You MUST call this tool whenever the user asks you to remember something, shares personal facts (name, preferences, birthdays, etc.), or tells you something they expect you to recall later. Do not just acknowledge — call this tool or the information will be lost.",
            "parameters": {
                "type": "object",
                "properties": {
                    "memory_type": {
                        "type": "string",
                        "description": "Type of memory to store.",
                        "enum": ["fact", "preference", "insight", "task"]
                    },
                    "content": {
                        "type": "string",
                        "description": "The content to store in memory."
                    },
                    "importance": {
                        "type": "integer",
                        "description": "Importance rating from 1-5.",
                        "minimum": 1,
                        "maximum": 5
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional list of tags to categorize this memory."
                    },
                    "user_guid": {
                        "type": "string",
                        "description": "Optional unique identifier of the user to store memory in a user-specific location."
                    }
                },
                "required": ["memory_type", "content"]
            }
        }
        init_db()
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        memory_type = kwargs.get('memory_type', 'fact')
        content = kwargs.get('content', '')
        importance = kwargs.get('importance', 3)
        tags = kwargs.get('tags', [])
        user_guid = kwargs.get('user_guid')

        if not content:
            return "Error: No content provided for memory storage."

        return self.store_memory(memory_type, content, importance, tags, user_guid)

    def store_memory(self, memory_type, content, importance, tags, user_guid=None):
        memory_id = str(uuid.uuid4())
        try:
            importance = max(1, min(5, int(importance)))
        except (TypeError, ValueError):
            importance = 3
        if not isinstance(tags, list):
            tags = []
        tags = [tag for tag in tags if isinstance(tag, str)]

        now = datetime.now()
        date_s = now.strftime("%Y-%m-%d")
        time_s = now.strftime("%H:%M:%S")
        scope_label = f"for user {user_guid}" if user_guid else "in shared memory"
        metadata = {
            "conversation_id": user_guid or "current",
            "session_id": "current",
            "mood": "neutral",
            "date": date_s,
            "time": time_s,
        }
        insert_memory(
            content=content,
            memory_type=memory_type,
            importance=importance,
            tags=tags,
            user_guid=user_guid,
            memory_id=memory_id,
            source="manage_memory",
            metadata=metadata,
            created_at=now.strftime("%Y-%m-%dT%H:%M:%S"),
            updated_at=now.strftime("%Y-%m-%dT%H:%M:%S"),
        )
        return f'Successfully stored {memory_type} memory {scope_label}: "{content}"'
