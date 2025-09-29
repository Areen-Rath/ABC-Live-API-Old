from fastapi import FastAPI
from mc_fetcher import mc_fetch
from et_fetcher import et_fetch
from bl_fetcher import bl_fetch

app = FastAPI()

@app.get("/moneycontrol")
def mc():
    data = mc_fetch()
    return { "data": data }

@app.get("/economic_times")
def et():
    data = et_fetch()
    return { "data": data }

@app.get("/business_line")
def bl():
    data = bl_fetch()
    return { "data": data }