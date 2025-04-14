from arena import Arena

if __name__ == "__main__":
    arena = Arena()
    arena.log("Arena started", "INFO")
    arena.run()
    while True:
        cmd = input(">>> ")
        if cmd == "stop":
            arena.running = False
            break

        elif cmd == "setds":
            cmd = cmd.split(" ")
            arena.driverstations["object"][cmd[1]].station_number = int(cmd[2])

        elif cmd == "setteam":
            cmd = cmd.split(" ")
            arena.driverstations["object"][cmd[1]].set_team_num(int(cmd[2]))

        elif cmd == "enable" or cmd == "e":
            for ds in arena.driverstations["object"]:
                ds.isEnabled = True

        elif cmd == "disable" or cmd == "d":
            for ds in arena.driverstations["object"]:
                ds.isEnabled = False

        else:
            print("Unknown command: E-Stopping")
            for ds in arena.driverstations["object"]:
                ds.isEstop = True