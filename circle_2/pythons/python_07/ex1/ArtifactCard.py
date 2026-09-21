from ex0.Card import Card


class ArtifactCard(Card):

    def __init__(
        self, name: str, cost: int, rarity: str, durability: int, effect: str
    ):
        super().__init__(name, cost, rarity)

        if durability <= 0:
            raise ValueError("Durability must be positive!")

        self.durability = durability
        self.effect = effect
        self.current_durability = durability

    def play(self, game_state: dict) -> dict:
        return {
            'card_played': self.name,
            'mana_used': self.cost,
            'effect': f'Artifact placed on battlefield: {self.effect}',
            'permanent': True  # Artifacts stay in play!
        }

    def activate_ability(self) -> dict:
        if self.current_durability <= 0:
            return {
                'artifact': self.name,
                'status': 'destroyed',
                'effect': 'Artifact has no durability remaining'
            }

        return {
            'artifact': self.name,
            'effect': self.effect,
            'durability_remaining': self.current_durability,
            'status': 'active'
        }

    def take_damage(self, damage: int) -> bool:
        self.current_durability -= damage
        return self.current_durability > 0
