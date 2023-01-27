from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/echo")
def get_item(request: Request):
    print(request.headers)
    args = request.query_params.keys()
    for key in args:
        print(key, ":", request.query_params[key])
    return str(request.headers) + str(args)
