from topFive.classes.Player import Player
from topFive.classes.League import League
from topFive.classes.Team import Team
from topFive.classes.Coach import Coach

teams = [Team() for _ in range(10)]
print("\nTeams:")
for team in teams:
    print("name: " + team.name + " league: " + str(team.league) + " budget: " + str(team.budget))
    print("Players in team:")
    for player in team.players:
        print(vars(player))
    print("Coach:")
    print(vars(team.coach))
    team.update_average_rating()
    print("Rating: " + str(team.average_rating))
