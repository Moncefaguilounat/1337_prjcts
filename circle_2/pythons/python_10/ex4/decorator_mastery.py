import time
import functools
from typing import Callable

#  a decorator is a function that wraps another function to add
#  behvaior before or after it runs without modifying the original code

#  the wraps is used inside every decorator so the original function does
#  not lose its name or documentation


def spell_timer(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Casting {func.__name__}...")
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"Spell completed in {elapsed:.3f} seconds")
        return result
    return wrapper

#  this decorator takes an argument and therefore we need an outer function
#  for the argument


def power_validator(min_power: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(self, power: int, *args, **kwargs):
            if power < min_power:
                return "Insufficient power for this spell"
            return func(self, power, *args, **kwargs)
        return wrapper
    return decorator

# this function tries to run the function passed to it up to max_attempts time


def retry_spell(max_attempts: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    print(
                        f"Spell failed, retrying..."
                        f" (attempt {attempt}/{max_attempts})"
                    )
            return f"Spell casting failed after {max_attempts} attempts"
        return wrapper
    return decorator


class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        return len(name) >= 3 and all(c.isalpha() or c == ' ' for c in name)

    @power_validator(min_power=10)
    def cast_spell(self, power: int, spell_name: str) -> str:
        return f"Successfully cast {spell_name} with {power} power"


def main() -> None:
    @spell_timer
    def fireball() -> str:
        time.sleep(0.1)
        return "Fireball cast!"

    print("Testing spell timer...")
    result = fireball()
    print(f"Result: {result}")

    print("\nTesting MageGuild...")
    print(MageGuild.validate_mage_name("Merlin"))
    print(MageGuild.validate_mage_name("X2"))

    guild = MageGuild()
    print(guild.cast_spell(15, "Lightning"))
    print(guild.cast_spell(5, "Thunder"))

    print("\nTesting retry spell...")

    attempt_count = {'n': 0}

    @retry_spell(max_attempts=3)
    def unstable_spell() -> str:
        attempt_count['n'] += 1
        if attempt_count['n'] < 3:
            raise ValueError("Spell unstable")
        return "Spell stabilized!"

    print(unstable_spell())


if __name__ == "__main__":
    main()
