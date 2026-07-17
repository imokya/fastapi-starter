from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/apps/{app_id}")
async def root(app_id: int):
  return {"message": f"Hello World {app_id}"}
