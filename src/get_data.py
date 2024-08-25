import re
import subprocess
import time
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse

import requests
from dotenv import get_key, set_key

from exceptions import HoYoAPIError, InvalidDataError, LogFileNotFoundError


def read_log_file(file_path: Path, num_lines: int = 4) -> list[str]:
    log_lines = []
    log_file = Path(file_path)

    if not log_file.exists():
        raise LogFileNotFoundError(f"Failed to locate log path. Check {file_path}.")

    with log_file.open() as log_file:
        for _ in range(num_lines):
            line = log_file.readline()
            if not line:
                break
            log_lines.append(line)
    return log_lines


def copy_used_file(cache_path: str, copy_path: str) -> None:
    command = f"Copy-Item -Path '{cache_path}' -Destination '{copy_path}'"
    try:
        subprocess.run(["powershell", "-Command", command], check=True)  # noqa: S603, S607
        print(f"Successfully copied from {cache_path} to {copy_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")


def locate_game_path(
    set_path: str,
) -> str:
    if set_path:
        return set_path

    app_data_path = Path.home() / "AppData"
    locallow_path = (app_data_path / "LocalLow" / "miHoYo" / "ZenlessZoneZero").resolve()

    log_path = locallow_path / "Player.log"
    log_lines = read_log_file(log_path)

    if not log_lines:
        log_path = locallow_path / "Player-prev.log"
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


def extract_url_from_datafile(game_path: Path | str) -> str:
    web_caches_path = Path(game_path) / "webCaches"
    if not web_caches_path.exists():
        raise LogFileNotFoundError(
            f"Could not locate webCaches folder. Check your game path at {game_path}.\n"
            "Make sure to open the Search history before running the script.",
        )

    cache_folders = [f for f in web_caches_path.iterdir() if f.is_dir()]
    max_version = 0
    cache_path = None

    for folder in cache_folders:
        if re.match(r"^\d+\.\d+\.\d+\.\d+$", folder.name):
            version = int("".join(folder.name.split(".")))
            if version >= max_version:
                max_version = version
                cache_path = web_caches_path / folder.name / "Cache" / "Cache_Data" / "data_2"

    if cache_path and cache_path.exists():
        copy_path = Path(game_path) / "temp_data_2"
        copy_used_file(cache_path, copy_path)

        with copy_path.open(encoding="utf-8", errors="ignore") as cache_file:
            cache_data = cache_file.read()

        Path(copy_path).unlink()

        cache_data_split = cache_data.split("1/0/")

        for line in reversed(cache_data_split):
            if line.startswith("http") and "getGachaLog" in line:
                url = line.split("\0")[0]
                res = requests.get(url, timeout=5)

                if res.status_code == 200:  # noqa: PLR2004
                    print(url)
                    uri = urlparse(url)
                    query = parse_qs(uri.query)
                    print(query)
                    required_keys = [
                        "authkey",
                        "authkey_ver",
                        "sign_type",
                        "game_biz",
                        "lang",
                        "plat_type",
                        "region",
                        # "page",
                        # "size",
                        # "real_gacha_type",
                        # "end_id",
                    ]
                    filtered_query = {key: query[key] for key in query if key in required_keys}

                    latest_url = f"{uri.scheme}://{uri.netloc}{uri.path}?" + urlencode(filtered_query, doseq=True)
                    print(latest_url)
                    print("Search History Url Found!")
                    return latest_url

    raise LogFileNotFoundError(f"Could not find Seach History Url in {cache_path}.")


def get_gacha_log(
    url: str,
    page: int = 1,
    size: int = 20,
    end_id: int | None = None,
    gacha_type: int = 2,
) -> tuple[list, int]:
    current_url = f"{url}&page={page}&size={size}&real_gacha_type={gacha_type}"
    if end_id:
        current_url += f"&end_id={end_id}"

    response = requests.get(current_url, timeout=5)
    response_data = response.json()

    if response_data["retcode"] != 0:
        raise HoYoAPIError(f"Error from HoYo API:\n {response_data['message']}")

    items = response_data["data"]["list"]
    if not items:
        print(f"Got everything from {gacha_type}")
        return None
    data = items  # temp_df = pd.DataFrame(items)
    return data, items[-1]["id"]


def get_everything() -> list:
    all_gacha_logs = []

    for gacha_type in gacha_types:
        all_gacha_logs += get_whole_gacha_data_by_type(url, gacha_type)
    return all_gacha_logs


def get_whole_gacha_data_by_type(url: str, gacha_type: str) -> list:
    assert gacha_type in gacha_types

    all_gacha_logs = []
    page = 1
    end_id = None
    while True:
        result = get_gacha_log(url, page=page, size=20, end_id=end_id, gacha_type=gacha_type)
        if not result:
            break
        temp_df, end_id = result

        all_gacha_logs += temp_df
        page += 1
        time.sleep(0.2)
    return all_gacha_logs


def init() -> tuple:
    env_file_path = Path.cwd() / ".env"

    if env_file_path.exists():
        zzz_game_path = get_key(str(env_file_path), "ZZZ_GAME_PATH")
        url = get_key(str(env_file_path), "API_URL")
    else:
        zzz_game_path = locate_game_path()
        url = extract_url_from_datafile(zzz_game_path)
        set_key(str(env_file_path), "ZZZ_GAME_PATH", str(zzz_game_path))
        set_key(str(env_file_path), "API_URL", str(url))

    return zzz_game_path, url


gacha_types = {"standart": 1, "event": 2, "weapon": 3, "idk": 4, "banbu": 5}
zzz_game_path, url = init()

if __name__ == "__main__":
    print(get_everything())
