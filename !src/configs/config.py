from switches import SwitchConfig

class Config:
    MAIN: SwitchConfig
    RED: SwitchConfig
    BLUE: SwitchConfig
    
    def __init__(self, ip_dict: dict, admin_pwd: str):
        self.red1 = ip_dict["red_1"]
        self.red2 = ip_dict["red_2"]
        self.red3 = ip_dict["red_3"]
        self.blue1 = ip_dict["blue_1"]
        self.blue2 = ip_dict["blue_2"]
        self.blue3 = ip_dict["blue_3"]
        self.admin_pwd = admin_pwd

        with open("main.txt") as f:
            MAIN = f.read().replace("<ADMIN_PASSWORD>", self.admin_pwd)
            MAIN = MAIN.replace("<RED1>", self.red1)
            MAIN = MAIN.replace("<RED2>", self.red2)
            MAIN = MAIN.replace("<RED3>", self.red3)
            MAIN = MAIN.replace("<BLUE1>", self.blue1)
            MAIN = MAIN.replace("<BLUE2>", self.blue2)
            MAIN = MAIN.replace("<BLUE3>", self.blue3)
            self.MAIN = SwitchConfig(MAIN, "none")

        with open("red.txt") as f:
            RED = f.read().replace("<ADMIN_PASSWORD>", self.admin_pwd)
            self.RED = SwitchConfig(RED, "none")

        with open("blue.txt") as f:
            BLUE = f.read().BLUE.replace("<ADMIN_PASSWORD>", self.admin_pwd)
            self.BLUE = SwitchConfig(BLUE, "none")