from ex2.EliteCard import EliteCard


def main():
    print("=== DataDeck Ability System ===\n")

    warrior = EliteCard(
        name="Arcane Warrior",
        cost=6,
        rarity="Mythic",
        attack=5,
        defense=8,
        mana_pool=10
    )

    print("EliteCard capabilities:")
    capabilities = warrior.get_all_capabilities()
    print(f"- Card: {capabilities['card_methods']}")
    print(f"- Combatable: {capabilities['combat_methods']}")
    print(f"- Magical: {capabilities['magic_methods']}\n")

    print(f"Playing {warrior.name} (Elite Card):")
    play_result = warrior.play({'mana': 10})
    print(f"{play_result}\n")

    print("Combat phase:")

    attack_result = warrior.attack("Enemy")
    print(f"Attack result: {attack_result}")

    defense_result = warrior.defend(5)
    print(f"Defense result: {defense_result}")

    combat_stats = warrior.get_combat_stats()
    print(f"Combat stats: {combat_stats}\n")

    print("Magic phase:")

    spell_result = warrior.cast_spell("Fireball", ["Enemy1", "Enemy2"])
    print(f"Spell cast: {spell_result}")

    mana_result = warrior.channel_mana(3)
    print(f"Mana channel: {mana_result}")

    magic_stats = warrior.get_magic_stats()
    print(f"Magic stats: {magic_stats}\n")

    print("Multiple interface implementation successful!")


if __name__ == "__main__":
    main()
