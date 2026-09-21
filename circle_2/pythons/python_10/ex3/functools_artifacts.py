import functools
import operator
from typing import Callable

#  reduce : is a high function that applies a function cumulatively
#           on an iterable reducing the whole iterable into on value


def spell_reducer(spells: list[int], operation: str) -> int:
    operations = {
        'add': operator.add,
        'multiply': operator.mul,
        'max': lambda a, b: a if a > b else b,
        'min': lambda a, b: a if a < b else b,
    }
    return functools.reduce(operations[operation], spells)

#  partial creates a new function using an existing function and freeze its
#  arguments , its useful for reproducibilty


def partial_enchanter(
    base_enchantment: Callable
) -> dict[str, Callable]:
    return {
        'fire_enchant': functools.partial(
            base_enchantment, power=50, element='fire'
        ),
        'ice_enchant': functools.partial(
            base_enchantment, power=50, element='ice'
        ),
        'lightning_enchant': functools.partial(
            base_enchantment, power=50, element='lightning'
        ),
    }

#  lru cache is a memory for function results , it stores previously produced
#  values to reuse them in the next call instead of recomputing the values
#  everytime


@functools.lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


#  single dispatch is a function that behaves differently depending
#  on the type of input (you add behaviors using funcname.register(data type)


def spell_dispatcher() -> Callable:
    @functools.singledispatch
    def cast(spell):
        return f"Unknown spell type: {type(spell)}"

    @cast.register(int)
    def _(spell: int) -> str:
        return f"Damage spell: {spell} points of damage"

    @cast.register(str)
    def _(spell: str) -> str:
        return f"Enchantment: {spell}"

    @cast.register(list)
    def _(spell: list) -> str:
        return f"Multi-cast: {', '.join(str(s) for s in spell)}"

    return cast


def main() -> None:
    spells = [10, 20, 30, 40]

    print("Testing spell reducer...")
    print(f"Sum: {spell_reducer(spells, 'add')}")
    print(f"Product: {spell_reducer(spells, 'multiply')}")
    print(f"Max: {spell_reducer(spells, 'max')}")

    print("\nTesting memoized fibonacci...")
    print(f"Fib(10): {memoized_fibonacci(10)}")
    print(f"Fib(15): {memoized_fibonacci(15)}")

    print("\nTesting partial enchanter...")

    def base_enchantment(target: str, power: int, element: str) -> str:
        return f"{element} enchantment ({power} power) on {target}"

    enchants = partial_enchanter(base_enchantment)
    print(enchants['fire_enchant'](target='Sword'))
    print(enchants['ice_enchant'](target='Shield'))

    print("\nTesting spell dispatcher...")
    dispatcher = spell_dispatcher()
    print(dispatcher(42))
    print(dispatcher("Fireball"))
    print(dispatcher(["heal", "shield", "fireball"]))


if __name__ == "__main__":
    main()
