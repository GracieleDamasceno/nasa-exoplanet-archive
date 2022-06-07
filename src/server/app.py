from fastapi import FastAPI

app = FastAPI()


@app.get("/", tags=["main"])
async def main():
    return {"message": "Nasa Exoplanet Archive is on!"}
