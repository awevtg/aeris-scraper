from src.collectors.source_registry import registry
from src.collectors.sample_source import SampleSourceAdapter


def register_default_sources():
    registry.register(SampleSourceAdapter())
    return registry


if __name__ == "__main__":
    source_registry = register_default_sources()
    print("Registered sources:", source_registry.available_sources())
