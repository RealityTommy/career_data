from fastapi import APIRouter, HTTPException
from app.prisma import prisma, connect_prisma, disconnect_prisma
from .schema import IndustryCreate, IndustryUpdate
from .model import IndustryModel

# Initialize the router with a versioned prefix
router = APIRouter(prefix="/v1/industries", tags=["Industries", "Version 1"])


# Prisma connection and disconnection lifecycle events
@router.on_event("startup")
async def startup():
    await connect_prisma()


@router.on_event("shutdown")
async def shutdown():
    await disconnect_prisma()


# Get all industries
@router.get("/", response_model=list[IndustryModel])
async def get_all_industries():
    """Fetch all industry records."""
    industries = await prisma.industry.find_many()
    return industries


# Create a new industry
@router.post("/", response_model=IndustryModel)
async def create_industry(industry_data: IndustryCreate):
    """Create a new industry record."""
    industry = await prisma.industry.create(data=industry_data.dict())
    return industry


# Get a specific industry by ID
@router.get("/{industry_id}", response_model=IndustryModel)
async def get_industry(industry_id: str):
    """Fetch an industry by its ID."""
    industry = await prisma.industry.find_unique(where={"id": industry_id})
    if not industry:
        raise HTTPException(status_code=404, detail="Industry not found")
    return industry


# Update an industry by ID
@router.put("/{industry_id}", response_model=IndustryModel)
async def update_industry(industry_id: str, industry_data: IndustryUpdate):
    """Update an existing industry record."""
    industry = await prisma.industry.update(
        where={"id": industry_id},
        data=industry_data.dict(exclude_unset=True),
    )
    if not industry:
        raise HTTPException(status_code=404, detail="Industry not found")
    return industry


# Delete a specific industry by ID
@router.delete("/{industry_id}")
async def delete_industry(industry_id: str):
    """Delete an industry record by its ID."""
    industry = await prisma.industry.delete(where={"id": industry_id})
    if not industry:
        raise HTTPException(status_code=404, detail="Industry not found")
    return {"message": f"Industry {industry_id} deleted successfully."}


# Delete all industries
@router.delete("/")
async def delete_all_industries():
    """Delete all industry records."""
    await prisma.industry.delete_many()
    return {"message": "All industries deleted successfully."}
