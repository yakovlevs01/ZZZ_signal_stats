import pandas as pd

from get_data import get_whole_gacha_data_by_type, init


def clear_data(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop(columns=["lang", "id", "count", "gacha_id", "uid"])


if __name__ == "__main__":
    game_path, url = init()
    gacha_types = {"standart": 1, "event": 2, "weapon": 3, "idk": 4, "banbu": 5}
    for g_type in gacha_types:
        raw_signal_data = get_whole_gacha_data_by_type(url, g_type)
        if raw_signal_data:
            signal_data_df = pd.DataFrame(raw_signal_data)
            signal_data_df = clear_data(signal_data_df)
            print(signal_data_df)
            signal_data_df.to_excel(f"ZZZ_import_{g_type}.xlsx")
