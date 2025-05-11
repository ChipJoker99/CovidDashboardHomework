from fastapi import FastAPI

app = FastAPI(
    title="COVID-19 Data API",
    description="API to fetch and display epidemiological data for Italian regions.",
    version="0.1.0",
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to Italy's COVID-19 Data API!"}