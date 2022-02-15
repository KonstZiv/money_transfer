from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    """
    test function 1 to check if it works
    """
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    """
    test function 2 to check if it works
    """
    return {"item_id": item_id}
