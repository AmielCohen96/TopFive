from topFive.models import Player,League,Team,Coach


league = League()
i = 1
for _ in range(10):
    team = Team()
    league.add_team(team)

for team in league.get_teams():
    print(i)
    print(f"Team: {team.name}")
    print(f"  Manager: {team.manager}")
    print(f"  Coach: {team.coach.name} (Defense: {team.coach.defense}, Offense: {team.coach.offense})")
    print(f"  Arena: {team.arena}")
    print(f"  Budget: ${team.budget}")
    team.update_average_rating()
    print(f"  Average Player Rating: {team.average_rating}")
    print(f"  Players:")
    for player in team.players:
        print(f"    - {player.name}, Age: {player.age}, Height: {player.height}m, Position: {player.position}, Rating: {player.rating}")
    print("\n")
    i += 1

