from typing import Dict, Type

from src.collectors.source_adapter import SourceAdapter


class SourceRegistry:
    """Central registry for AERIS airfare source adapters."""

    def __init__(self):
        self._sources: Dict[str, SourceAdapter] = {}

    def register(self, adapter: SourceAdapter):
        name = adapter.source_name.strip().lower()

        if not name:
            raise ValueError("Source adapter must define source_name.")

        self._sources[name] = adapter

    def get(self, source_name: str):
        return self._sources.get(source_name.strip().lower())

    def available_sources(self):
        return sorted(self._sources.keys())


registry = SourceRegistry()
