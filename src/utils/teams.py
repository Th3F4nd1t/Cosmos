from dataclasses import dataclass

@dataclass
class TeamData:
    name: str
    number: int
    matches_played: int = 0
    wins: int = 0
    losses: int = 0
    ties: int = 0
    matches: list[int] = None

class TeamsManager:
    def __init__(self, teams_file: str = "./src/data/teams.json"):
        self.teams_file = teams_file
        self.data = self._load_teams()

    def _load_teams(self):
        import json
        try:
            with open(self.teams_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Teams file {self.teams_file} not found.")
            return {}
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {self.teams_file}.")
            return {}
        
    def _save_teams(self):
        import json
        try:
            with open(self.teams_file, 'w') as file:
                json.dump(self.data, file, indent=4)
        except IOError as e:
            print(f"Error saving teams to {self.teams_file}: {e}")

    def get_team(self, team_number: int) -> TeamData | None:
        """
        Returns the team data for the given team number.
        If the team does not exist, returns None.
        """
        team_info = self.data.get(str(team_number), None)
        if team_info is None:
            return None
        return TeamData(**team_info)

    def get_all_teams(self) -> list[TeamData]:
        """
        Returns a list of all teams.
        """
        return [TeamData(**team) for team in self.data.values()]

    def add_team(self, team_number: int, team_data: TeamData):
        """
        Adds a new team or updates an existing team with the given data.
        team_data should be a dictionary containing team information.
        """
        self.data[str(team_number)] = {
            "name": team_data.name,
            "number": team_data.number,
            "matches_played": team_data.matches_played,
            "wins": team_data.wins,
            "losses": team_data.losses,
            "ties": team_data.ties,
            "matches": team_data.matches or []
        }
        self._save_teams()

    def remove_team(self, team_number: int):
        """
        Removes a team by its number.
        """
        if str(team_number) in self.data:
            del self.data[str(team_number)]
            self._save_teams()
        else:
            print(f"Team {team_number} does not exist.")

    def update_team_stats(self, team_number: int, matches_played: int, wins: int, losses: int, ties: int):
        """
        Updates the statistics for a team.
        """
        team = self.get_team(team_number)
        if team:
            team.matches_played += matches_played
            team.wins += wins
            team.losses += losses
            team.ties += ties
            self.add_team(team_number, team)
        else:
            print(f"Team {team_number} does not exist.")