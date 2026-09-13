from abc import ABC, abstractmethod
from typing import List

from src.models import AirfareObservation


class SourceAdapter(ABC):
    """
    Common interface for every AERIS airfare source.

    Each source must convert its data into the same
    AirfareObservation schema.

    Sources should only be automated when their API,
    Terms of Service, robots policy, or written permission
    permits the required access.
    """

    source_name = "unknown"

    @abstractmethod
    def collect(
        self,
        origin: str,
        destination: str,
        travel_date: str,
        booking_window: int,
    ) -> List[AirfareObservation]:
        """Collect normalized airfare observations."""
        raise NotImplementedError

    def describe(self):
        return {
            "source": self.source_name,
            "adapter": self.__class__.__name__,
        }
