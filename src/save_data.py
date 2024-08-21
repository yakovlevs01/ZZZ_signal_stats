import pandas as pd

from get_data import main


def clear_data(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop(columns=["lang", "id", "count", "gacha_id", "uid"])


if __name__ == "__main__":
    d = main()
    df = pd.DataFrame(d)
    df = clear_data(df)
    df.to_excel("ZZZ_import.xlsx")
