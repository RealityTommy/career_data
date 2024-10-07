from fastapi import FastAPI
from app.career.career import router as career_router
from app.industry.industry import router as industry_router
from app.credential.credential import router as credential_router
from app.skill.skill import router as skill_router


app = FastAPI()

# Include routers
app.include_router(career_router)
app.include_router(industry_router)
app.include_router(credential_router)
app.include_router(skill_router)
