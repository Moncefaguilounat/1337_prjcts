from ex4.TournamentCard import TournamentCard
from ex4.TournamentPlatform import TournamentPlatform


def main():
    print("=== DataDeck Tournament Platform ===\n")

    platform = TournamentPlatform()

    dragon = TournamentCard(
        name="Fire Dragon",
        cost=5,
        rarity="Legendary",
        attack=7,
        defense=5
    )

    wizard = TournamentCard(
        name="Ice Wizard",
        cost=4,
        rarity="Rare",
        attack=5,
        defense=4
    )

    print("Registering Tournament Cards...\n")

    dragon_id = platform.register_card(dragon)
    wizard_id = platform.register_card(wizard)

    print(f"{dragon.name} (ID: {dragon_id}):")
    print("- Interfaces: [Card, Combatable, Rankable]")
    print(f"- Rating: {dragon.calculate_rating()}")
    print(f"- Record: {dragon.wins}-{dragon.losses}\n")

    print(f"{wizard.name} (ID: {wizard_id}):")
    print("- Interfaces: [Card, Combatable, Rankable]")
    print(f"- Rating: {wizard.calculate_rating()}")
    print(f"- Record: {wizard.wins}-{wizard.losses}\n")

    print("Creating tournament match...\n")
    match_result = platform.create_match(dragon_id, wizard_id)
    del match_result['match_number']
    print(f"Match result: {match_result}\n")

    print("Tournament Leaderboard:")
    leaderboard = platform.get_leaderboard()
    for entry in leaderboard:
        print(f"{entry['rank']}. {entry['name']} - "
              f"Rating: {entry['rating']} ({entry['record']})")

    print()

    report = platform.generate_tournament_report()
    print("Platform Report:")
    print(report)

    print("\n=== Tournament Platform Successfully Deployed! ===")
    print("All abstract patterns working together harmoniously!")


if __name__ == "__main__":
    main()
