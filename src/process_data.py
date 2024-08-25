import copy

from get_data import get_whole_gacha_data_by_type, init


def calculate_pity(data: list[dict]) -> list[dict]:
    local_data = copy.deepcopy(data)

    s_rank_counter = 0
    a_rank_counter = 0
    for item in reversed(local_data):
        if item["rank_type"] == "2":
            item["pity"] = 0
            s_rank_counter += 1
            a_rank_counter += 1
        elif item["rank_type"] == "3":
            item["pity"] = a_rank_counter + 1
            a_rank_counter = 0
            s_rank_counter += 1
        elif item["rank_type"] == "4":
            item["pity"] = s_rank_counter + 1
            a_rank_counter = 0
            s_rank_counter = 0
    return local_data, s_rank_counter, a_rank_counter


gacha_types = {"standart": 1, "event": 2, "weapon": 3, "idk": 4, "banbu": 5}

if __name__ == "__main__":
    game_path, url = init()
    for g_type in gacha_types:
        raw_signal_data = get_whole_gacha_data_by_type(url, g_type)
        signal_data, s_pity, a_pity = calculate_pity(raw_signal_data)
