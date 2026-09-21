from ex3.FantasyCardFactory import FantasyCardFactory
from ex3.AggressiveStrategy import AggressiveStrategy
from ex3.GameEngine import GameEngine


def main():
    print("=== DataDeck Game Engine ===\n")

    factory = FantasyCardFactory()
    strategy = AggressiveStrategy()

    engine = GameEngine()

    print("Configuring Fantasy Card Game...")
    engine.configure_engine(factory, strategy)

    supported = factory.get_supported_types()
    print(f"Available types: {supported}\n")

    print("Simulating aggressive turn...")

    hand = [
        factory.create_creature(5),
        factory.create_creature(2),
        factory.create_spell(3)
    ]

    print(f"Hand: [{hand[0].name} ({hand[0].cost}), "
          f"{hand[1].name} ({hand[1].cost}), "
          f"{hand[2].name} ({hand[2].cost})]\n")

    turn_result = engine.simulate_turn()

    print("Turn execution:")
    print(f"Strategy: {turn_result['strategy']}")
    print(f"Actions: {turn_result}\n")

    status = engine.get_engine_status()
    print("Game Report:")
    print(status)

    print("\nAbstract Factory + Strategy Pattern: ", end="")
    print("Maximum flexibility achieved!")


if __name__ == "__main__":
    main()
