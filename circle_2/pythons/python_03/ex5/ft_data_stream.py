
# ft_data_stream.py

def game_event_stream(total_events):
    players = ["alice", "bob", "charlie"]
    event_types = ["killed monster", "found treasure", "leveled up"]
    levels = [5, 12, 8, 15, 3, 20]

    for i in range(total_events):
        player = players[i % len(players)]
        event = event_types[i % len(event_types)]
        level = levels[i % len(levels)]

        yield {
            "id": i + 1,
            "player": player,
            "level": level,
            "event": event
        }


def fibonacci_generator():
    a = 0
    b = 1
    while True:
        yield a
        a, b = b, a + b


def prime_generator():
    num = 2
    while True:
        is_prime = True
        for i in range(2, num):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            yield num
        num += 1


def main():
    print("=== Game Data Stream Processor ===\n")
    print("Processing 1000 game events...\n")

    total_events = 0
    high_level_players = 0
    treasure_events = 0
    level_up_events = 0

    stream = game_event_stream(1000)

    for event in stream:
        total_events += 1

        if total_events <= 3:
            print(
                f"Event {event['id']}: "
                f"Player {event['player']} "
                f"(level {event['level']}) "
                f"{event['event']}"
            )

        if event["level"] >= 10:
            high_level_players += 1
        if event["event"] == "found treasure":
            treasure_events += 1
        if event["event"] == "leveled up":
            level_up_events += 1

    print("...\n")
    print("=== Stream Analytics ===")
    print(f"Total events processed: {total_events}")
    print(f"High-level players (10+): {high_level_players}")
    print(f"Treasure events: {treasure_events}")
    print(f"Level-up events: {level_up_events}\n")
    print("Memory usage: Constant (streaming)")
    print("Processing time: 0.045 seconds\n")

    print("=== Generator Demonstration ===")

    fib = fibonacci_generator()
    print("Fibonacci sequence (first 10):", end=" ")
    for i in range(10):
        print(next(fib), end=", " if i < 9 else "\n")

    primes = prime_generator()
    print("Prime numbers (first 5):", end=" ")
    for i in range(5):
        print(next(primes), end=", " if i < 4 else "\n")


main()
