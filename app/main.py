from fastapi import FastAPI
from app.career.career import router as career_router
from app.industry.industry import router as industry_router

app = FastAPI()

# Include routers
app.include_router(career_router)
app.include_router(industry_router)
