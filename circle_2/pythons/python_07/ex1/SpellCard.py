from ex0.Card import Card


class SpellCard(Card):

    def __init__(self, name: str, cost: int, rarity: str, effect_type: str):
        super().__init__(name, cost, rarity)

        self.effect_type = effect_type

    def play(self, game_state: dict) -> dict:
        return {
            'card_played': self.name,
            'mana_used': self.cost,
            'effect': f'{self.effect_type.capitalize()} spell cast',
            'consumed': True
        }

    def resolve_effect(self, targets: list) -> dict:
        effect_descriptions = {
            'damage': f'Deal damage to {len(targets)} target(s)',
            'heal': f'Heal {len(targets)} target(s)',
            'buff': f'Increase stats of {len(targets)} target(s)',
            'debuff': f'Decrease stats of {len(targets)} target(s)'
        }

        return {
            'spell': self.name,
            'effect_type': self.effect_type,
            'targets': targets,
            'result': effect_descriptions.get(
                self.effect_type, 'Unknown effect'
            )
        }
