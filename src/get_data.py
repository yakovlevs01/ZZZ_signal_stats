import os

from exceptions import InvalidDataError, LogFileNotFoundError


def read_log_file(file_path: str, num_lines: int = 4) -> list[str]:
    log_lines = []
    if not os.path.exists(file_path):
        raise LogFileNotFoundError(f"Failed to locate log path. Check {file_path}.")
    with open(file_path) as log_file:
        for _ in range(num_lines):
            line = log_file.readline()
            if not line:
                break
            log_lines.append(line)
    return log_lines


def locate_game_path(set_path: str = "") -> str:
    if set_path:
        return set_path

    app_data = os.getenv("APPDATA")
    locallow_path = os.path.abspath(os.path.join(app_data, "..", "LocalLow", "miHoYo", "ZenlessZoneZero"))

    log_path = os.path.join(locallow_path, "Player.log")
    log_lines = read_log_file(log_path)

    if not log_lines:
        log_path = os.path.join(locallow_path, "Player-prev.log")
        log_lines = read_log_file(log_path)

    if not log_lines:
        raise InvalidDataError("Log file returned 0 lines")

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
        raise InvalidDataError(
            f"Failed to get game path from logs. Check {log_path} for game path or pass it manually in this function",
        )

    return game_path
