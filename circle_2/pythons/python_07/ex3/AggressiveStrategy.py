from ex3.GameStrategy import GameStrategy


class AggressiveStrategy(GameStrategy):

    def execute_turn(self, hand: list, battlefield: list) -> dict:
        actions = {
            'strategy': 'AggressiveStrategy',
            'cards_played': [],
            'mana_used': 0,
            'targets_attacked': [],
            'damage_dealt': 0
        }

        sorted_hand = sorted(hand, key=lambda card: card.cost)

        available_mana = 10
        for card in sorted_hand:
            if card.cost <= 3 and available_mana >= card.cost:
                actions['cards_played'].append(card.name)
                actions['mana_used'] += card.cost
                available_mana -= card.cost

        total_damage = 0
        for card in battlefield:

            if hasattr(card, 'attack_power') or hasattr(card, 'attack'):
                attack_val = getattr(
                    card, 'attack_power', None) or getattr(card, 'attack', 0)
                total_damage += attack_val
                actions['targets_attacked'].append('Enemy Player')

        actions['damage_dealt'] = total_damage

        return actions

    def get_strategy_name(self) -> str:
        return "AggressiveStrategy"

    def prioritize_targets(self, available_targets: list) -> list:

        creatures = [
            t for t in available_targets if 'creature' in str(t).lower()]
        players = [t for t in available_targets if 'player' in str(t).lower()]

        return creatures + players
