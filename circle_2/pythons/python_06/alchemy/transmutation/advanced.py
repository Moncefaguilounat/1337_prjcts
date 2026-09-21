from .basic import lead_to_gold
from ..potions import healing_potion


def philosophers_stone() -> str:
    lead_result = lead_to_gold()
    potion_result = healing_potion()
    return f"Philosopher's stone created using {lead_result} and {potion_result}"


def elixir_of_life() -> str:
    return "Elixir of life: eternal youth achieved!"
