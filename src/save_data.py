import pandas as pd

from get_data import get_everything


def clear_data(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop(columns=["lang", "id", "count", "gacha_id", "uid"])


if __name__ == "__main__":
    raw_signal_data = get_everything()
    signal_data_df = pd.DataFrame(raw_signal_data)
    signal_data_df = clear_data(signal_data_df)
    signal_data_df.to_excel("ZZZ_import.xlsx")
