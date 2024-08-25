import pandas as pd
from fastapi import FastAPI

app = FastAPI()


@app.get("/data")
async def get_data() -> list[dict]:
    logs = pd.read_excel("zzz_logs1.xlsx")
    print(logs)

    return logs.to_dict(orient="records")
