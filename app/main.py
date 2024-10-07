from fastapi import FastAPI

# Import app routers
from app.career.career import router as career_router
from app.industry.industry import router as industry_router
from app.credential.credential import router as credential_router
from app.skill.skill import router as skill_router

# Import ONET routers
from app.onet.imports.imports import router as imports_router
from app.onet.industry.industry import router as onet_industry_router
from app.onet.occupation.occupation import router as onet_occupation_router


app = FastAPI()

# Include app routers
app.include_router(career_router)
app.include_router(industry_router)
app.include_router(credential_router)
app.include_router(skill_router)

# Include ONET routers
app.include_router(imports_router)
app.include_router(onet_industry_router)
app.include_router(onet_occupation_router)
