from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import read_db, read_extra_info, save_extra_info, save_logs_to_db
from get_data import get_whole_gacha_data_by_type, init
from process_data import calculate_pity

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


gacha_types = {"standart": 1, "event": 2, "weapon": 3, "idk": 4, "banbu": 5}
game_path, url = init()


@app.get("/data/{gacha_type}")
async def get_data(gacha_type: str) -> dict:
    signal_data = read_db(gacha_type)
    other_data = read_extra_info(gacha_type)

    return {"data": signal_data, "other": other_data}


@app.get("/save_all_data")
async def save_full_data() -> None:
    for gacha_type in gacha_types:
        raw_signal_data = get_whole_gacha_data_by_type(url, gacha_type)
        signal_data, s_pity, a_pity = calculate_pity(raw_signal_data)
        save_logs_to_db(gacha_type, signal_data)
        save_extra_info(gacha_type, {"s_pity": s_pity, "a_pity": a_pity})
    return {"status": "All is ok, data saved"}
