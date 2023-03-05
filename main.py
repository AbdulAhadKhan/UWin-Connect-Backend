from fastapi import Request
from fastapi import FastAPI

from routes.user import user_router

app = FastAPI()
app.include_router(user_router)

@app.get("/echo")
async def echo(request: Request):
    """Echo the request body as JSON"""
    return await request.json()


@app.put("/updateprofile", status_code=201)
async def edit_user_profile():
    # record = user.dict()
    # email = record["email"]

    # filter = {"email": email}
    # update = {"$set": record}
    # with MongoClient() as client:
    #     collection = client[DB][USER_COLLECTION]
    #     collection.update_one(filter, update)

    # return {"message": "User profile updated successfully"}
    pass