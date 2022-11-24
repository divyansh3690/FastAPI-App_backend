from fastapi import FastAPI
from database import engine
from router import auth, posts
import model

app = FastAPI()

model.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(posts.router)

@app.get("/")
async def hello():
    return {"This is homepage. Please open docs(add /docs with the existing url) or postman "}






