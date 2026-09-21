#!/usr/bin/env python3

def main():
    players_data = [
        {'name': 'alice', 'score': 2300, 'status': 'active'},
        {'name': 'bob', 'score': 1800, 'status': 'active'},
        {'name': 'charlie', 'score': 2150, 'status': 'active'},
        {'name': 'diana', 'score': 2050, 'status': 'inactive'},
    ]

    achievements_data = [
        {'player': 'alice', 'achievement': 'first_kill'},
        {'player': 'alice', 'achievement': 'level_10'},
        {'player': 'alice', 'achievement': 'speedrun'},
        {'player': 'alice', 'achievement': 'explorer'},
        {'player': 'alice', 'achievement': 'champion'},
        {'player': 'bob', 'achievement': 'first_kill'},
        {'player': 'bob', 'achievement': 'level_10'},
        {'player': 'bob', 'achievement': 'explorer'},
        {'player': 'charlie', 'achievement': 'first_kill'},
        {'player': 'charlie', 'achievement': 'level_10'},
        {'player': 'charlie', 'achievement': 'speedrun'},
        {'player': 'charlie', 'achievement': 'boss_slayer'},
        {'player': 'charlie', 'achievement': 'explorer'},
        {'player': 'charlie', 'achievement': 'champion'},
        {'player': 'charlie', 'achievement': 'legendary'},
        {'player': 'diana', 'achievement': 'headshot'},
        {'player': 'diana', 'achievement': 'stealth'},
        {'player': 'diana', 'achievement': 'combo'},
        {'player': 'diana', 'achievement': 'treasure'},
        {'player': 'diana', 'achievement': 'ninja'},
    ]

    print("=== Game Analytics Dashboard ===\n")

    print("=== List Comprehension Examples ===")

    high_scorers = []
    for p in players_data:
        if p['score'] > 2000:
            high_scorers.append(p['name'])
    print(f"High scorers (>2000): {high_scorers}")

    scores_doubled = []
    for p in players_data:
        scores_doubled.append(p['score'] * 2)
    print(f"Scores doubled: {scores_doubled}")

    active_players = []
    for p in players_data:
        if p['status'] == 'active':
            active_players.append(p['name'])
    print(f"Active players: {active_players}\n")

    print("=== Dict Examples (simplified) ===")

    top_three = ['alice', 'bob', 'charlie']
    player_scores = {}

    for p in players_data:
        if p['name'] in top_three:
            player_scores[p['name']] = p['score']
    print(f"Player scores: {player_scores}")

    score_categories = {
        'high': 0,
        'medium': 0,
        'low': 0
    }

    for p in players_data:
        if p['score'] > 2000:
            score_categories['high'] += 1
        elif p['score'] >= 1500:
            score_categories['medium'] += 1
        else:
            score_categories['low'] += 1

    print(f"Score categories: {score_categories}")

    achievement_counts = {}

    for name in top_three:
        count = 0
        for a in achievements_data:
            if a['player'] == name:
                count += 1
        achievement_counts[name] = count

    print(f"Achievement counts: {achievement_counts}\n")

    print("=== Set Examples (simplified) ===")

    unique_players = set()
    for p in players_data:
        unique_players.add(p['name'])
    print(f"Unique players: {unique_players}")

    unique_achievements = set()
    for a in achievements_data:
        unique_achievements.add(a['achievement'])
    print(f"Unique achievements: {unique_achievements}\n")

    print("=== Combined Analysis ===")

    total_players = len(unique_players)
    print(f"Total players: {total_players}")

    total_unique_achievements = len(unique_achievements)
    print(f"Total unique achievements: {total_unique_achievements}")

    all_scores = []
    for p in players_data:
        all_scores.append(p['score'])
    average_score = sum(all_scores) / len(all_scores)
    print(f"Average score: {average_score}")

    top_player = players_data[0]
    for p in players_data:
        if p['score'] > top_player['score']:
            top_player = p

    top_name = top_player['name']
    top_score = top_player['score']

    top_achievements = 0
    for a in achievements_data:
        if a['player'] == top_name:
            top_achievements += 1

    print(f"Top performer: {top_name} ({top_score} points, {top_achievements} achievements)")


if __name__ == "__main__":
    main()

