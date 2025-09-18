from dataclasses import dataclass
from tools.terminal.decorators import user_run, system_run
from tools.terminal.shell_handler import MessageLevel


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
    @system_run
    def __init__(self, fms, teams_file: str = "./src/data/teams.json"):
        self.fms = fms
        self.teams_file = teams_file
        self.data = self._load_teams()

    @user_run
    def _load_teams(self, instance_id: int|None = None):
        self.fms.shell_handler.check_instance(instance_id)

        import json
        try:
            with open(self.teams_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            self.fms.shell_handler.send_message(instance_id, f"Teams file {self.teams_file} not found.", MessageLevel.ERROR)
            return {}
        except json.JSONDecodeError:
            self.fms.shell_handler.send_message(instance_id, f"Error decoding JSON from {self.teams_file}.", MessageLevel.ERROR)
            return {}

    @user_run
    def _save_teams(self, instance_id: int|None = None):
        self.fms.shell_handler.check_instance(instance_id)
        
        import json
        try:
            with open(self.teams_file, 'w') as file:
                json.dump(self.data, file, indent=4)
        except IOError as e:
            self.fms.shell_handler.send_message(instance_id, f"Error saving teams to {self.teams_file}: {e}", MessageLevel.ERROR)

    @user_run
    def get_team(self, team_number: int, instance_id: int|None = None) -> TeamData | None:
        """
        Returns the team data for the given team number.
        If the team does not exist, returns None.
        """
        self.fms.shell_handler.check_instance(instance_id)

        team_info = self.data.get(str(team_number), None)
        if team_info is None:
            return None
        return TeamData(**team_info)

    def get_all_teams(self, instance_id: int|None = None) -> list[TeamData]:
        """
        Returns a list of all teams.
        """
        self.fms.shell_handler.check_instance(instance_id)

        return [TeamData(**team) for team in self.data.values()]

    @user_run
    def add_team(self, team_number: int, team_data: TeamData, instance_id: int|None = None):
        """
        Adds a new team or updates an existing team with the given data.
        team_data should be a dictionary containing team information.
        """
        self.fms.shell_handler.check_instance(instance_id)

        self.data[str(team_number)] = {
            "name": team_data.name,
            "number": team_data.number,
            "matches_played": team_data.matches_played,
            "wins": team_data.wins,
            "losses": team_data.losses,
            "ties": team_data.ties,
            "matches": team_data.matches or []
        }
        self._save_teams(instance_id)

    @user_run
    def remove_team(self, team_number: int, instance_id: int|None = None):
        """
        Removes a team by its number.
        """
        self.fms.shell_handler.check_instance(instance_id)

        if str(team_number) in self.data:
            del self.data[str(team_number)]
            self._save_teams(instance_id)
        else:
            self.fms.shell_handler.send_message(instance_id, f"Team {team_number} does not exist.", MessageLevel.ERROR)

    @user_run
    def update_team_stats(self, team_number: int, matches_played: int, wins: int, losses: int, ties: int, instance_id: int|None = None):
        """
        Updates the statistics for a team.
        """
        self.fms.shell_handler.check_instance(instance_id)

        team = self.get_team(team_number, instance_id)
        if team:
            team.matches_played += matches_played
            team.wins += wins
            team.losses += losses
            team.ties += ties
            self.add_team(team_number, team)
        else:
            self.fms.shell_handler.send_message(instance_id, f"Team {team_number} does not exist.", MessageLevel.ERROR)