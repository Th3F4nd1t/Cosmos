def driverstation_ip(team: int) -> str:
    """
    Returns the Driver Station IP for a given FRC team number.
    Format depends on number of digits in the team number.
    """
    try:
        team = int(team)
    except ValueError:
        raise ValueError("Team number must be an integer for DS IP")

    if not (0 < team <= 25599):
        raise ValueError("Invalid team number for DS IP")
    

    team_str = str(team).zfill(5)  # pad to 5 digits to simplify slicing


    if team < 100:  # 1 or 2 digits
        return f"10.0.{team}.5"
    elif team < 1000:  # 3 digits
        return f"10.{team_str[0]}.{team_str[1:]}.5"
    elif team < 10000:  # 4 digits
        return f"10.{team_str[:2]}.{team_str[2:]}.5"
    else:  # 5 digits
        return f"10.{team_str[:3]}.{team_str[3:]}.5"