import pandas as pd
from fastapi import FastAPI

app = FastAPI()


@app.get("/data")
async def get_data():
    df = pd.read_excel("zzz_logs1.xlsx")
    print(df)
    return df.to_dict(orient="records")
