from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "HelloWorld"}


@app.get("/login/sherin")
def about():
    return {"message": "Password"}


loginpage = {
    1: {
        "name": "Cherry",
        "student_id": 3536333,
        "program": "MAC"
    }
}


@app.get("/echo")
def get_item(request: Request):
    print(request.headers)
    args = request.query_params.keys()
    for key in args:
        print(key, ":", request.query_params[key])
    return str(request.headers) + str(args)
