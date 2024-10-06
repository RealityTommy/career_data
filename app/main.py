from fastapi import FastAPI
from app.career.career import router as career_router

app = FastAPI()

# Include the career router (prefix is already set in the router)
app.include_router(career_router)
