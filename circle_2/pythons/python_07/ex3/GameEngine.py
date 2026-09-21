from ex3.CardFactory import CardFactory
from ex3.GameStrategy import GameStrategy


class GameEngine:

    def __init__(self):
        self.factory: CardFactory | None = None
        self.strategy: GameStrategy | None = None
        self.cards_created: list = []
        self.turns_simulated: int = 0

    def configure_engine(
            self, factory: CardFactory, strategy: GameStrategy) -> None:
        self.factory = factory
        self.strategy = strategy

        print("Engine configured:")
        print(f"- Factory: {factory.__class__.__name__}")
        print(f"- Strategy: {strategy.get_strategy_name()}")

    def simulate_turn(self) -> dict:
        if not self.factory or not self.strategy:
            raise RuntimeError(
                "Engine not configured! Call configure_engine() first.")

        hand = [
            self.factory.create_creature(5),
            self.factory.create_creature(2),
            self.factory.create_spell(3)
        ]

        self.cards_created.extend(hand)

        battlefield = [
            self.factory.create_creature(3)
        ]

        turn_result = self.strategy.execute_turn(hand, battlefield)

        self.turns_simulated += 1

        return turn_result

    def get_engine_status(self) -> dict:
        return {
            'turns_simulated': self.turns_simulated,
            'strategy_used': (
                self.strategy.get_strategy_name() if self.strategy else None
                    ),
            'total_damage': 0,
            'cards_created': len(self.cards_created)
        }
