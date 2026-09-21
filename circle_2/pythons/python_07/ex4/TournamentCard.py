from ex0.Card import Card
from ex2.Combatable import Combatable
from ex4.Rankable import Rankable


class TournamentCard(Card, Combatable, Rankable):

    def __init__(self, name: str, cost: int, rarity: str,
                 attack: int, defense: int):
        super().__init__(name, cost, rarity)

        if attack <= 0 or defense <= 0:
            raise ValueError("Attack and defense must be positive!")

        self.attack_power = attack
        self.defense_power = defense
        self.current_health = defense

        self.wins = 0
        self.losses = 0
        self.base_rating = 1200

    def play(self, game_state: dict) -> dict:
        return {
            'card_played': self.name,
            'mana_used': self.cost,
            'effect': 'Tournament card ready for competitive play',
            'rating': self.calculate_rating()
        }

    def attack(self, target) -> dict:
        return {
            'attacker': self.name,
            'target': str(target),
            'damage': self.attack_power,
            'attacker_rating': self.calculate_rating()
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

    def calculate_rating(self) -> int:

        rating = self.base_rating + (self.wins * 16) - (self.losses * 16)
        return rating

    def update_wins(self, wins: int) -> None:

        if wins < 0:
            raise ValueError("Wins cannot be negative!")
        self.wins += wins

    def update_losses(self, losses: int) -> None:

        if losses < 0:
            raise ValueError("Losses cannot be negative!")
        self.losses += losses

    def get_rank_info(self) -> dict:

        total_matches = self.wins + self.losses
        if total_matches > 0:
            win_rate = (self.wins / total_matches * 100)
        else:
            win_rate = 0

        return {
            'name': self.name,
            'rating': self.calculate_rating(),
            'wins': self.wins,
            'losses': self.losses,
            'win_rate': round(win_rate, 1),
            'record': f"{self.wins}-{self.losses}"
        }

    def get_tournament_stats(self) -> dict:
        return {
            'card_info': self.get_card_info(),
            'combat_stats': self.get_combat_stats(),
            'rank_info': self.get_rank_info()
        }
