import random


def simulate_game(match):
    home_team = match.home_team
    away_team = match.away_team

    home_team_three_pointers = 0
    away_team_three_pointers = 0
    home_team_two_pointers = 0
    away_team_two_pointers = 0
    home_team_free_throws = 0
    away_team_free_throws = 0

    outcomes = ['score', 'steal', 'turnover', 'block', 'miss_rebound_offense', 'miss_rebound_defense']

    def calculate_shot_success(player, shot_type):
        """Calculate whether the shot was successful based on the player's stats."""
        if shot_type == 'three':
            return random.random() < (player.shooting3 / 100.0)
        elif shot_type == 'two':
            return random.random() < (player.shooting2 / 100.0)
        elif shot_type == 'free_throw':
            return random.random() < (player.shooting2 / 100.0)
        return False

    def handle_rebound(shot_missed, defending_player):
        """Handle rebound logic based on whether the shot was missed."""
        if shot_missed:
            if random.random() < (defending_player.defense / 100.0):
                return 'blocked'
            else:
                return random.choice(['offensive_rebound', 'defensive_rebound'])
        return None

    def simulate_possession(attacking_team, defending_team):
        """Simulate a single possession for the attacking team."""
        attacking_player = random.choice(list(attacking_team.players.all()))
        shot_type = random.choice(['three', 'two', 'free_throw'])
        shot_successful = calculate_shot_success(attacking_player, shot_type)

        if shot_successful:
            if attacking_team == home_team:
                if shot_type == 'three':
                    return 'home_three_pointer'
                elif shot_type == 'two':
                    return 'home_two_pointer'
                elif shot_type == 'free_throw':
                    return 'home_free_throw'
            else:
                if shot_type == 'three':
                    return 'away_three_pointer'
                elif shot_type == 'two':
                    return 'away_two_pointer'
                elif shot_type == 'free_throw':
                    return 'away_free_throw'
        else:
            rebound_result = handle_rebound(shot_missed=True,
                                            defending_player=random.choice(list(defending_team.players.all())))
            return rebound_result

    for _ in range(100):  # Simulate 100 possessions
        attacking_team, defending_team = random.choice([(home_team, away_team), (away_team, home_team)])
        result = simulate_possession(attacking_team, defending_team)

        if result == 'home_three_pointer':
            home_team_three_pointers += 1
        elif result == 'away_three_pointer':
            away_team_three_pointers += 1
        elif result == 'home_two_pointer':
            home_team_two_pointers += 1
        elif result == 'away_two_pointer':
            away_team_two_pointers += 1
        elif result == 'home_free_throw':
            home_team_free_throws += 1
        elif result == 'away_free_throw':
            away_team_free_throws += 1
        # Rebounds and other outcomes are not counted in stats directly

    match.update_scores(
        home_three_pointers=home_team_three_pointers,
        away_three_pointers=away_team_three_pointers,
        home_two_pointers=home_team_two_pointers,
        away_two_pointers=away_team_two_pointers,
        home_free_throws=home_team_free_throws,
        away_free_throws=away_team_free_throws
    )
