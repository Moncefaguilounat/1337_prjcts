from abc import ABC, abstractmethod
from typing import List, Any, Dict, Optional, Union


class DataStream(ABC):

    def __init__(self, stream_id: str) -> None:
        self.stream_id = stream_id
        self.processed_count = 0

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(
            self, data_batch: List[Any], criteria: Optional[str] = None
    ) -> List[Any]:
        if criteria is None:
            return [item for item in data_batch]
        return [item for item in data_batch if criteria in str(item)]

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {
            "stream_id": self.stream_id,
            "stream_type": self.stream_type,
            "processed_count": self.processed_count,
        }


class SensorStream(DataStream):

    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        self.stream_type = "Environmental Data"
        self.temperature_readings = []

    def process_batch(self, data_batch: List[Any]) -> str:
        try:
            if not data_batch:
                raise ValueError("Empty sensor batch received")

            temps = [
                item["temp"]
                for item in data_batch
                if isinstance(item, dict) and "temp" in item
            ]

            self.processed_count += len(data_batch)
            self.temperature_readings.extend(temps)

            avg_temp = sum(temps) / len(temps) if temps else 0.0

            return (
                f"Sensor analysis: {len(data_batch)} readings processed, "
                f"avg temp: {avg_temp:.1f}°C"
            )

        except ValueError as e:
            return f"Sensor stream error: {e}"
        except Exception as e:
            return f"Unexpected sensor error: {e}"

    def filter_data(
        self, data_batch: List[Any], criteria: Optional[str] = None
                    ) -> List[Any]:
        if criteria == "critical":
            return [
                item
                for item in data_batch
                if isinstance(item, dict)
                and "temp" in item
                and (item["temp"] > 35 or item["temp"] < 0)
            ]
        return super().filter_data(data_batch, criteria)

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        stats = super().get_stats()
        if self.temperature_readings:
            stats["avg_temperature"] = round(
                sum(
                    self.temperature_readings
                    ) / len(self.temperature_readings), 2
                        )
        return stats


class TransactionStream(DataStream):

    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        self.stream_type = "Financial Data"
        self.net_flow = 0.0

    def process_batch(self, data_batch: List[Any]) -> str:
        try:
            if not data_batch:
                raise ValueError("Empty transaction batch received")

            net = 0.0
            for item in data_batch:
                if isinstance(item, dict):
                    if item.get("type") == "buy":
                        net -= item.get("amount", 0)
                    elif item.get("type") == "sell":
                        net += item.get("amount", 0)

            self.net_flow += net
            self.processed_count += len(data_batch)
            sign = "+" if net >= 0 else ""

            return (
                f"Transaction analysis: {len(data_batch)} operations, "
                f"net flow: {sign}{net:.0f} units"
            )

        except ValueError as e:
            return f"Transaction stream error: {e}"
        except Exception as e:
            return f"Unexpected transaction error: {e}"

    def filter_data(
        self, data_batch: List[Any],
        criteria: Optional[str] = None
            ) -> List[Any]:

        if criteria == "large":
            return [
                item
                for item in data_batch
                if isinstance(item, dict) and item.get("amount", 0) > 100
            ]
        return super().filter_data(data_batch, criteria)

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        stats = super().get_stats()
        stats["net_flow"] = self.net_flow
        return stats


class EventStream(DataStream):

    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        self.stream_type = "System Events"
        self.error_count = 0

    def process_batch(self, data_batch: List[Any]) -> str:
        try:
            if not data_batch:
                raise ValueError("Empty event batch received")

            errors = [
                item for item in data_batch
                if isinstance(item, str) and "error" in item.lower()
            ]

            self.error_count += len(errors)
            self.processed_count += len(data_batch)

            return (
                f"Event analysis: {len(data_batch)} events, "
                f"{len(errors)} error detected"
            )

        except ValueError as e:
            return f"Event stream error: {e}"
        except Exception as e:
            return f"Unexpected event error: {e}"

    def filter_data(
        self, data_batch: List[Any], criteria: Optional[str] = None
            ) -> List[Any]:
        if criteria == "error":
            return [
                item for item in data_batch
                if isinstance(item, str) and "error" in item.lower()
            ]
        return super().filter_data(data_batch, criteria)

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        stats = super().get_stats()
        stats["error_count"] = self.error_count
        return stats


class StreamProcessor:

    def __init__(self) -> None:
        self.streams = []

    def add_stream(self, stream: DataStream) -> None:
        self.streams.append(stream)

    def process_all(self, data_batches: Dict[str, List[Any]]) -> List[str]:
        results = []

        for stream in self.streams:
            if isinstance(stream, SensorStream) and "sensor" in data_batches:
                batch = data_batches["sensor"]
            elif isinstance(stream, TransactionStream):
                if "transaction" in data_batches:
                    batch = data_batches["transaction"]
            elif isinstance(stream, EventStream) and "event" in data_batches:
                batch = data_batches["event"]
            else:
                continue

            result = stream.process_batch(batch)
            results.append(f"- {stream.stream_type}: {result}")

        return results

    def filter_all(
        self, data_batches: Dict[str, List[Any]], criteria: Dict[str, str]
            ) -> Dict[str, List[Any]]:
        filtered = {}

        for stream in self.streams:
            if isinstance(stream, SensorStream):
                key = "sensor"
                batch = data_batches.get("sensor", [])
                crit = criteria.get("sensor")
            elif isinstance(stream, TransactionStream):
                key = "transaction"
                batch = data_batches.get("transaction", [])
                crit = criteria.get("transaction")
            elif isinstance(stream, EventStream):
                key = "event"
                batch = data_batches.get("event", [])
                crit = criteria.get("event")
            else:
                continue

            filtered[key] = stream.filter_data(batch, crit)

        return filtered

    def get_all_stats(self) -> List[Dict[str, Union[str, int, float]]]:
        return [stream.get_stats() for stream in self.streams]


def main() -> None:
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===\n")

    print("Initializing Sensor Stream...")
    sensor = SensorStream("SENSOR_001")
    print(f"Stream ID: {sensor.stream_id}, Type: {sensor.stream_type}")
    sensor_batch_one = [
        {"temp": 22.5, "label": "temp:22.5"},
        {"humidity": 65, "label": "humidity:65"},
        {"pressure": 1013, "label": "pressure:1013"},
    ]
    print("Processing sensor batch: [temp:22.5, humidity:65, pressure:1013]")
    print(sensor.process_batch(sensor_batch_one))

    print("\nInitializing Transaction Stream...")
    transaction = TransactionStream("TRANS_001")
    print(
        f"Stream ID: {transaction.stream_id}, Type: {transaction.stream_type}"
    )
    trans_batch_one = [
        {"type": "buy", "amount": 100},
        {"type": "sell", "amount": 150},
        {"type": "buy", "amount": 75},
    ]
    print("Processing transaction batch: [buy:100, sell:150, buy:75]")
    print(transaction.process_batch(trans_batch_one))

    print("\nInitializing Event Stream...")
    event = EventStream("EVENT_001")
    print(f"Stream ID: {event.stream_id}, Type: {event.stream_type}")
    event_batch_one = ["login", "error", "logout"]
    print("Processing event batch: [login, error, logout]")
    print(event.process_batch(event_batch_one))

    print("\n=== Polymorphic Stream Processing ===")
    print("Processing mixed stream types through unified interface...\n")

    processor = StreamProcessor()
    processor.add_stream(SensorStream("SENSOR_002"))
    processor.add_stream(TransactionStream("TRANS_002"))
    processor.add_stream(EventStream("EVENT_002"))

    batch_two = {
        "sensor": [
            {"temp": 38.0, "label": "high-temp-alert"},
            {"temp": 21.0, "label": "normal"},
        ],
        "transaction": [
            {"type": "buy", "amount": 200},
            {"type": "sell", "amount": 50},
            {"type": "buy", "amount": 300},
            {"type": "sell", "amount": 120},
        ],
        "event": ["login", "error", "logout"],
    }

    print("Batch two Results:")
    results = processor.process_all(batch_two)
    for r in results:
        print(r)

    print("\nStream filtering active: High-priority data only")
    criteria = {
        "sensor": "critical",
        "transaction": "large",
        "event": "error",
    }
    filtered = processor.filter_all(batch_two, criteria)
    sensor_critical = filtered.get("sensor", [])
    trans_large = filtered.get("transaction", [])

    print(
        f"Filtered results: {len(sensor_critical)} critical sensor alerts, "
        f"{len(trans_large)} large transaction"
    )

    print("\nAll streams processed successfully. Nexus throughput optimal.")


if __name__ == "__main__":
    main()
