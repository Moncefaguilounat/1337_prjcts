from ex0.Card import Card
import random
from typing import Optional


class Deck:

    def __init__(self):

        self.cards: list[Card] = []  # List to hold all cards

    def add_card(self, card: Card) -> None:

        if not isinstance(card, Card):
            raise TypeError("Can only add Card objects to deck!")

        self.cards.append(card)

    def remove_card(self, card_name: str) -> bool:

        for i, card in enumerate(self.cards):
            if card.name == card_name:
                self.cards.pop(i)  # Remove the card
                return True

        return False  # Card not found

    def shuffle(self) -> None:

        random.shuffle(self.cards)

    def draw_card(self) -> Optional[Card]:

        if len(self.cards) == 0:
            return None  # Empty deck

        return self.cards.pop(0)  # Remove and return first card

    def get_deck_stats(self) -> dict:

        if len(self.cards) == 0:
            return {
                'total_cards': 0,
                'creatures': 0,
                'spells': 0,
                'artifacts': 0,
                'avg_cost': 0.0
            }

        # Count card types
        creatures = sum(
            type(card).__name__ == 'CreatureCard' for card in self.cards)
        spells = sum(
            type(card).__name__ == 'SpellCard' for card in self.cards)
        artifacts = sum(
            type(card).__name__ == 'ArtifactCard' for card in self.cards)

        # Calculate average cost
        total_cost = sum(card.cost for card in self.cards)
        avg_cost = total_cost / len(self.cards)

        return {
            'total_cards': len(self.cards),
            'creatures': creatures,
            'spells': spells,
            'artifacts': artifacts,
            'avg_cost': round(avg_cost, 1)
        }
