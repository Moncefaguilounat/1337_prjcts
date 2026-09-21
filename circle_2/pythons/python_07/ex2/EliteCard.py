from ex0.Card import Card
from ex2.Combatable import Combatable
from ex2.Magical import Magical


class EliteCard(Card, Combatable, Magical):

    def __init__(self, name: str, cost: int, rarity: str,
                 attack: int, defense: int, mana_pool: int):
        super().__init__(name, cost, rarity)

        if attack <= 0 or defense <= 0:
            raise ValueError("Attack and defense must be positive!")

        if mana_pool <= 0:
            raise ValueError("Mana pool must be positive!")

        self.attack_power = attack
        self.defense_power = defense
        self.current_health = defense

        self.max_mana = mana_pool
        self.current_mana = mana_pool

    def play(self, game_state: dict) -> dict:
        return {
            'card_played': self.name,
            'mana_used': self.cost,
            'effect': 'Elite card summoned with combat and magic abilities',
            'combat_ready': True,
            'magic_ready': True
        }

    def attack(self, target) -> dict:
        return {
            'attacker': self.name,
            'target': str(target),
            'damage': self.attack_power,
            'combat_type': 'melee'
        }

    def defend(self, incoming_damage: int) -> dict:
        damage_blocked = min(self.defense_power, incoming_damage)
        damage_taken = incoming_damage - damage_blocked

        self.current_health -= damage_taken

        return {
            'defender': self.name,
            'damage_taken': damage_taken,
            'damage_blocked': damage_blocked,
            'still_alive': self.current_health > 0
        }

    def get_combat_stats(self) -> dict:
        return {
            'attack': self.attack_power,
            'defense': self.defense_power,
            'health': self.current_health
        }

    def cast_spell(self, spell_name: str, targets: list) -> dict:
        mana_cost = 4

        if self.current_mana < mana_cost:
            return {
                'caster': self.name,
                'spell': spell_name,
                'status': 'failed',
                'reason': 'Not enough mana'
            }

        self.current_mana -= mana_cost

        return {
            'caster': self.name,
            'spell': spell_name,
            'targets': targets,
            'mana_used': mana_cost,
            'status': 'success'
        }

    def channel_mana(self, amount: int) -> dict:
        old_mana = self.current_mana
        self.current_mana = min(self.current_mana + amount, self.max_mana)
        actual_channeled = self.current_mana - old_mana

        return {
            'channeled': actual_channeled,
            'total_mana': self.current_mana,
            'max_mana': self.max_mana
        }

    def get_magic_stats(self) -> dict:
        return {
            'current_mana': self.current_mana,
            'max_mana': self.max_mana,
            'mana_percent': round((self.current_mana / self.max_mana) * 100)
        }

    def get_all_capabilities(self) -> dict:
        return {
            'card_methods': ['play', 'get_card_info', 'is_playable'],
            'combat_methods': ['attack', 'defend', 'get_combat_stats'],
            'magic_methods': ['cast_spell', 'channel_mana', 'get_magic_stats']
        }
