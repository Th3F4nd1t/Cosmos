from enum import Enum
import json

class UserRole(Enum):
    DEFAULT = 0
    TEAM_MEMBER = 1
    FIELD_HELPER = 2
    FIELD_MANAGER = 3
    FIELD_ADMIN = 4

class UserData:
    def __init__(self, filepath='fms/webserver/data/user.json'):
        self.filepath = filepath
        self.data = self.load_user_data(filepath)

    def load_user_data(self, filepath='fms/webserver/data/user.json'):
        # load json, replacing role with enum
        with open(filepath, 'r') as f:
            data = json.load(f)
        for user, info in data.items():
            info['role'] = UserRole[info['role']]
        return data

    def save_user_data(self, data):
        # save json, replacing enum with role string
        serializable_data = {}
        for user, info in data.items():
            serializable_info = info.copy()
            serializable_info['role'] = info['role'].name
            serializable_data[user] = serializable_info
        with open(self.filepath, 'w') as f:
            json.dump(serializable_data, f, indent=4)

    def get_user_info(self, email):
        return self.data.get(email, None)
    
    def update_user_info(self, email, name=None, role=None, teams=None, pending_role_request=None, pending_team_requests=None):
        if email not in self.data:
            self.data[email] = {'name': name or '', 'role': UserRole.DEFAULT, 'teams': []}
        if name is not None:
            self.data[email]['name'] = name
        if role is not None:
            self.data[email]['role'] = role
        if teams is not None:
            self.data[email]['teams'] = teams
        if pending_role_request is not None:
            if pending_role_request == "":
                pending_role_request = None
            self.data[email]['pending_role_request'] = pending_role_request
        if pending_team_requests is not None:
            self.data[email]['pending_team_requests'] = pending_team_requests
        self.save_user_data(self.data)

    def is_admin(self, email):
        user_info = self.get_user_info(email)
        if user_info and user_info['role'] == UserRole.FIELD_ADMIN:
            return True
        return False
    
    def is_pending_request(self, email):
        user_info = self.get_user_info(email)
        if user_info and user_info['pending_role_request'] is not None:
            return True
        return False
    
    def request_role(self, email, requested_role):
        if email in self.data:
            self.data[email]['pending_role_request'] = requested_role
            self.save_user_data(self.data)

    def request_team(self, email, team):
        if email in self.data:
            if 'pending_team_requests' not in self.data[email]:
                self.data[email]['pending_team_requests'] = []
            self.data[email]['pending_team_requests'].append(team)
            self.save_user_data(self.data)
    
    def is_pending_team_request(self, email):
        user_info = self.get_user_info(email)
        if user_info and user_info.get('pending_team_requests'):
            return True
        return False
    
    def does_user_exist(self, email):
        return email in self.data
    
    def create_new_user(self, email, name):
        if email not in self.data:
            self.data[email] = {'name': name, 'role': UserRole.DEFAULT, 'pending_role_request': None, 'teams': [], 'pending_team_requests': []}
            self.save_user_data(self.data)

    def get_all_pending_role_requests(self):
        pending_requests = {}
        for email, info in self.data.items():
            if info.get('pending_role_request'):
                pending_requests[email] = info['pending_role_request']
        return pending_requests
    
    def get_all_pending_team_requests(self):
        pending_requests = {}
        for email, info in self.data.items():
            if info.get('pending_team_requests'):
                pending_requests[email] = info['pending_team_requests']
        return pending_requests

if __name__ == "__main__":
    user_data = UserData()
    print(user_data.get_user_info("<email>"))
    user_data.update_user_info("<email>", name="New Name", role=UserRole.TEAM_MEMBER, teams=["Team A", "Team B"])
    print(user_data.get_user_info("<email>"))