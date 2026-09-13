from src.collectors.source_adapter import SourceAdapter
from src.collectors.source_registry import SourceRegistry


class TestAdapter(SourceAdapter):
    source_name = "test"

    def collect(
        self,
        origin,
        destination,
        travel_date,
        booking_window,
    ):
        return []


registry = SourceRegistry()
adapter = TestAdapter()

registry.register(adapter)

print("Registered sources:", registry.available_sources())
print("Adapter:", adapter.describe())
print("Registry test: OK")
