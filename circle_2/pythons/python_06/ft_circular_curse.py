from alchemy.grimoire.validator import validate_ingredients
from alchemy.grimoire.spellbook import record_spell


def main():
    print("=== Circular Curse Breaking ===\n")

    print("Testing ingredient validation:")
    print("validate_ingredients(\"fire air\"):", end =" ")
    print(validate_ingredients("fire air"))
    print("validate_ingredients(\"dragon scales\"): ", end="")
    print(validate_ingredients("dragon scales"))

    print()

    print("Testing spell recording with validation:")
    print("record_spell(\"Fireball\", \"fire air\"): ", end="")
    print(record_spell("Fireball", "fire air"))
    print("record_spell(\"Dark Magic\", \"shadow\"): ", end="")
    print(record_spell("Dark Magic", "shadow"))

    print()

    print("Testing late import technique:")
    print("record_spell(\"Lightning\", \"air\"): ", end="")
    print(record_spell("Lightning", "air"))

    print()

    print("Circular dependency curse avoided using late imports!")
    print("All spells processed safely!")


main()
