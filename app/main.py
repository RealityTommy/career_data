from fastapi import FastAPI, Response
from prisma import Prisma

app = FastAPI()
prisma = Prisma()


@app.on_event("startup")
async def startup():
    await prisma.connect()


@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()


# Server Status
@app.get("/")
def root():
    return Response("Server is running.")
