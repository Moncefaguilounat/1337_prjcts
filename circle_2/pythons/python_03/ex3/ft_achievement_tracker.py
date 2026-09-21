

print("=== Achievement Tracker System ===\n")

Alice = {'first_kill', 'level_10', 'treasure_hunter', 'speed_demon'}
Bob = {'first_kill', 'level_10', 'boss_slayer', 'collector'}
Charlie = {
 'level_10', 'treasure_hunter', 'boss_slayer', 'speed_demon', 'perfectionist'
}

print(f"Player alice achievements: {Alice}")
print(f"Player bob achievements: {Bob}")
print(f"Player charlie achievements: {Charlie}\n")

all_unique = set().union(Alice, Bob, Charlie)
print("=== Achievement Analytics ===")
print(f"All unique achievements: {all_unique}")
print(f"Total unique achievements: {len(all_unique)}\n")

all_common = set(Alice.intersection(Bob, Charlie))
rare_ach = (
    (Alice - Bob - Charlie)
    | (Bob - Alice - Charlie)
    | (Charlie - Alice - Bob)
)
print(f"Common to all players: {all_common}")
print(f"Rare achievements (1 player): {rare_ach}\n")

ab_common = set(Alice.intersection(Bob))
alice_uni = set(Alice.difference(Bob))
bob_uni = set(Bob.difference(Alice))
print(f"Alice vs Bob common: {ab_common}")
print(f"Alice unique: {alice_uni}")
print(f"Bob unique: {bob_uni}")
