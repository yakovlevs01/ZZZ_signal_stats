from fastapi import FastAPI

from get_data import get_whole_gacha_data_by_type, init
from process_data import calculate_pity

app = FastAPI()
gacha_types = {"standart": 1, "event": 2, "weapon": 3, "idk": 4, "banbu": 5}
game_path, url = init()


@app.get("/data/{gacha_type}")
async def get_data(gacha_type: str) -> dict:
    g_type = gacha_types[gacha_type]
    raw_signal_data = get_whole_gacha_data_by_type(url, g_type)
    signal_data, s_pity, a_pity = calculate_pity(raw_signal_data)

    return {"data": signal_data, "s_pity": s_pity, "a_pity": a_pity}
