from ex0.CreatureCard import CreatureCard
from ex1.SpellCard import SpellCard
from ex1.ArtifactCard import ArtifactCard
from ex1.Deck import Deck


def main():
    print("=== DataDeck Deck Builder ===\n")

    deck = Deck()

    dragon = CreatureCard(
        name="Fire Dragon",
        cost=5,
        rarity="Legendary",
        attack=7,
        health=5
    )

    lightning = SpellCard(
        name="Lightning Bolt",
        cost=3,
        rarity="Common",
        effect_type="damage"
    )

    mana_crystal = ArtifactCard(
        name="Mana Crystal",
        cost=2,
        rarity="Uncommon",
        durability=5,
        effect="+1 mana per turn"
    )

    print("Building deck with different card types...")
    deck.add_card(dragon)
    deck.add_card(lightning)
    deck.add_card(mana_crystal)

    stats = deck.get_deck_stats()
    print(f"Deck stats: {stats}\n")

    deck.shuffle()

    print("Drawing and playing cards:\n")

    card1 = deck.draw_card()
    if card1:
        print(f"Drew: {card1.name} ", end="")
        print(f"({card1.__class__.__name__.replace('Card', '')})")
        result = card1.play({'mana': 10})
        print(f"Play result: {result}\n")

    card2 = deck.draw_card()
    if card2:
        print(f"Drew: {card2.name} ", end="")
        print(f"({card2.__class__.__name__.replace('Card', '')})")
        result = card2.play({'mana': 10})
        print(f"Play result: {result}\n")

    card3 = deck.draw_card()
    if card3:
        print(f"Drew: {card3.name} ", end="")
        print(f"({card3.__class__.__name__.replace('Card', '')})")
        result = card3.play({'mana': 10})
        print(f"Play result: {result}\n")

    print("Polymorphism in action: Same interface, different card behaviors!")


if __name__ == "__main__":
    main()
