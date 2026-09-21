from ex0.CreatureCard import CreatureCard


def main():
    print("=== DataDeck Card Foundation ===\n")

    dragon = CreatureCard(
        name="Fire Dragon",
        cost=5,
        rarity="Legendary",
        attack=7,
        health=5
    )

    print("CreatureCard Info:")
    info = dragon.get_card_info()
    info['type'] = 'Creature'
    info['attack'] = dragon.attack
    info['health'] = dragon.health
    print(info)

    print("\nPlaying Fire Dragon with 6 mana available:")
    print(f"Playable: {dragon.is_playable(6)}")

    game_state = {'mana': 6}
    result = dragon.play(game_state)
    print(f"Play result: {result}")

    print("\nFire Dragon attacks Goblin Warrior:")
    attack_result = dragon.attack_target("Goblin Warrior")
    print(f"Attack result: {attack_result}")

    print("\nTesting insufficient mana (3 available):")
    print(f"Playable: {dragon.is_playable(3)}")

    print("\nAbstract pattern successfully demonstrated!")


if __name__ == "__main__":
    main()
