from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/echo")
async def get_item(request: Request):
    return await request.json()
