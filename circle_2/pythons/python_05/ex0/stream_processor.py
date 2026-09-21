from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):

    @abstractmethod
    def process(self, data: Any) -> str:
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    def format_output(self, result: str) -> str:
        return f"Output: {result}"


class NumericProcessor(DataProcessor):

    def __init__(self) -> None:
        super().__init__()

    def process(self, data: Any) -> str:
        try:
            print(f"Processing data: {data}")

            if not self.validate(data):
                return "Error: Invalid numeric data"

            print("Validation: Numeric data verified")

            total = sum(data)
            length = len(data)
            avg = total / length

            result = (
                    f"Processed {length} numeric values, "
                    f"sum={total}, avg={avg}"
                )
            return self.format_output(result)

        except Exception as e:
            return f"Error processing numeric data: {e}"

    def validate(self, data: Any) -> bool:
        if not isinstance(data, list):
            return False

        for item in data:
            if not isinstance(item, (int, float)):
                return False

        return len(data) > 0


class TextProcessor(DataProcessor):

    def __init__(self) -> None:
        super().__init__()

    def process(self, data: Any) -> str:
        try:
            print(f'Processing data: "{data}"')

            if not self.validate(data):
                return "Error: Invalid text data"

            print("Validation: Text data verified")

            chars = len(data)
            words = len(data.split())

            result = f"Processed text: {chars} characters, {words} words"
            return self.format_output(result)

        except Exception as e:
            return f"Error processing text data: {e}"

    def validate(self, data: Any) -> bool:
        return isinstance(data, str) and len(data) > 0


class LogProcessor(DataProcessor):

    def __init__(self) -> None:
        super().__init__()

    def process(self, data: Any) -> str:
        try:
            print(f'Processing data: "{data}"')

            if not self.validate(data):
                return "Error: Invalid log entry"

            print("Validation: Log entry verified")

            parts = data.split(":", 1)
            level = parts[0].strip()
            message = parts[1].strip() if len(parts) > 1 else ""

            result = f"[{level}] {level} level detected: {message}"
            return self.format_output(result)

        except Exception as e:
            return f"Error processing log data: {e}"

    def validate(self, data: Any) -> bool:
        if not isinstance(data, str):
            return False

        if "ERROR:" in data or "INFO:" in data or "WARNING:" in data:
            return True

        return False


def main() -> None:
    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===\n")

    print("Initializing Numeric Processor...")
    numeric_processor = NumericProcessor()
    resultone = numeric_processor.process([1, 2, 3, 4, 5])
    print(resultone)
    print()

    print("Initializing Text Processor...")
    text_processor = TextProcessor()
    resulttwo = text_processor.process("Hello Nexus World")
    print(resulttwo)
    print()

    print("Initializing Log Processor...")
    log_processor = LogProcessor()
    resultthree = log_processor.process("ERROR: Connection timeout")
    print(resultthree)
    print()

    print("=== Polymorphic Processing Demo ===")
    print("Processing multiple data types through same interface...\n")

    processors = [
        NumericProcessor(),
        TextProcessor(),
        LogProcessor()
    ]

    test_data = [
        [1, 2, 3],
        "Nexus online",
        "INFO: System ready"
    ]

    for i, (processor, data) in enumerate(zip(processors, test_data), 1):
        result = processor.process(data)
        output_line = result.replace("Output: ", "")
        print(f"Result {i}: {output_line}")

    print("\nFoundation systems online. Nexus ready for advanced streams.")


if __name__ == "__main__":
    main()
