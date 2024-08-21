import os


def locate_game_path(set_path=None):
    if set_path:
        return set_path

    app_data = os.getenv("APPDATA")
    locallow_path = os.path.abspath(os.path.join(app_data, "..", "LocalLow", "miHoYo", "ZenlessZoneZero"))
    log_path = os.path.join(locallow_path, "Player.log")

    if not os.path.exists(log_path):
        raise Exception("Failed to locate log file!")

    log_lines = []
    with open(log_path) as log_file:
        log_lines = log_file.readlines()[:4]

    if not log_lines:
        log_path = os.path.join(locallow_path, "Player-prev.log")
        if not os.path.exists(log_path):
            raise Exception("Failed to locate log file!")

        with open(log_path) as log_file:
            log_lines = log_file.readlines()[:4]

    if not log_lines:
        raise Exception("Failed to locate game path!")

    game_path = None
    for log_line in log_lines:
        if log_line.startswith("[Subsystems] Discovering subsystems at path "):
            game_path = (
                log_line.replace("[Subsystems] Discovering subsystems at path ", "")
                .replace("UnitySubsystems", "")
                .strip()
            )
            break

    if not game_path:
        raise Exception("Failed to locate game path!")

    return game_path
