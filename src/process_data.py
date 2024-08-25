import copy


def calculate_pity(data: list[dict]) -> tuple[list[dict], int, int]:
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
