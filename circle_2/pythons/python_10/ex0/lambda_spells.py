

def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(artifacts, key=lambda x: x['power'], reverse=True)


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return list(filter(lambda m: m['power'] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda s: f"* {s} *", spells))


def mage_stats(mages: list[dict]) -> dict:
    return {
        'max_power': max(mages, key=lambda p: p['power'])['power'],
        'min_power': min(mages, key=lambda p: p['power'])['power'],
        'avg_power': round(
                sum(map(lambda p: p['power'], mages)) / len(mages), 2)
    }


def main() -> None:
    artifacts = [
        {'name': 'Crystal Orb', 'power': 85, 'type': 'magic'},
        {'name': 'Fire Staff', 'power': 92, 'type': 'fire'},
        {'name': 'Ice Wand', 'power': 70, 'type': 'ice'},
    ]

    mages = [
        {'name': 'Alex', 'power': 45, 'element': 'fire'},
        {'name': 'Jordan', 'power': 80, 'element': 'water'},
        {'name': 'Riley', 'power': 30, 'element': 'earth'},
        {'name': 'Morgan', 'power': 65, 'element': 'air'},
    ]

    spells = ['fireball', 'heal', 'shield']

    print("Testing artifact sorter...")
    sorted_artifacts = artifact_sorter(artifacts)
    print(
        f"{sorted_artifacts[0]['name']} ({sorted_artifacts[0]['power']} power"
        f") comes before {sorted_artifacts[1]['name']} "
        f"({sorted_artifacts[1]['power']} power)"
    )

    print("\nTesting spell transformer...")
    transformed = spell_transformer(spells)
    print(' '.join(transformed))

    print("\nTesting power filter...")
    powerful = power_filter(mages, 50)
    print(f"Mages with power >= 50: {[m['name'] for m in powerful]}")

    print("\nTesting mage stats...")
    stats = mage_stats(mages)
    print(f"Max: {stats['max_power']}, Min: {stats['min_power']}, "
          f"Avg: {stats['avg_power']}")


if __name__ == "__main__":
    main()
