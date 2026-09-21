from ex4.TournamentCard import TournamentCard
import random


class TournamentPlatform:

    def __init__(self):

        self.registered_cards: dict[str, TournamentCard] = {}
        self.matches_played = 0

    def register_card(self, card: TournamentCard) -> str:

        if not isinstance(card, TournamentCard):
            raise TypeError("Can only register TournamentCard objects!")

        card_id = (
            f"{card.name.lower().replace(' ', '_')}_"
            f"{len(self.registered_cards) + 1:03d}"
        )
        self.registered_cards[card_id] = card

        return card_id

    def create_match(self, card1_id: str, card2_id: str) -> dict:

        if card1_id not in self.registered_cards:
            raise ValueError(f"Card {card1_id} not registered!")
        if card2_id not in self.registered_cards:
            raise ValueError(f"Card {card2_id} not registered!")

        card1 = self.registered_cards[card1_id]
        card2 = self.registered_cards[card2_id]

        if card1.attack_power > card2.attack_power:
            winner_id = card1_id
            loser_id = card2_id
        elif card2.attack_power > card1.attack_power:
            winner_id = card2_id
            loser_id = card1_id
        else:
            winner_id = card1_id
            loser_id = card2_id

        winner = self.registered_cards[winner_id]
        loser = self.registered_cards[loser_id]

        winner.update_wins(1)
        loser.update_losses(1)

        self.matches_played += 1

        return {
            'match_number': self.matches_played,
            'winner': winner_id,
            'loser': loser_id,
            'winner_rating': winner.calculate_rating(),
            'loser_rating': loser.calculate_rating()
        }

    def get_leaderboard(self) -> list:

        sorted_cards = sorted(
            self.registered_cards.items(),
            key=lambda x: x[1].calculate_rating(),
            reverse=True
        )

        leaderboard = []
        for rank, (card_id, card) in enumerate(sorted_cards, start=1):
            rank_info = card.get_rank_info()
            rank_info['rank'] = rank
            rank_info['card_id'] = card_id
            leaderboard.append(rank_info)

        return leaderboard

    def generate_tournament_report(self) -> dict:
        if len(self.registered_cards) == 0:
            return {
                'total_cards': 0,
                'matches_played': 0,
                'avg_rating': 0,
                'platform_status': 'empty'
            }

        total_cards = len(self.registered_cards)
        total_rating = sum(
            card.calculate_rating() for card in self.registered_cards.values()
        )
        avg_rating = total_rating // total_cards

        return {
            'total_cards': total_cards,
            'matches_played': self.matches_played,
            'avg_rating': avg_rating,
            'platform_status': 'active'
        }
