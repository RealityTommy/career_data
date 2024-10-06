from fastapi import APIRouter, HTTPException
from app.prisma import prisma, connect_prisma, disconnect_prisma
from .schema import CareerCreate, CareerUpdate
from .model import CareerModel

# Initialize the router with a prefix for all career endpoints
router = APIRouter(
    prefix="/v1/careers",  # All endpoints will be prefixed with /careers
    tags=["Careers", "Version 1"],  # Optionally, you can add tags for documentation purposes
)


# Use the connect/disconnect from prisma.py
@router.on_event("startup")
async def startup():
    await connect_prisma()


@router.on_event("shutdown")
async def shutdown():
    await disconnect_prisma()


# Get all careers
@router.get("/", response_model=list[CareerModel])
async def get_all_careers():
    """Fetch all career records."""
    careers = await prisma.career.find_many()
    return careers


# Create a career
@router.post("/", response_model=CareerModel)
async def create_career(career_data: CareerCreate):
    """Create a new career record."""
    career = await prisma.career.create(data=career_data.dict())
    return career


# Get a specific career by ID
@router.get("/{career_id}", response_model=CareerModel)
async def get_career(career_id: str):
    """Fetch a career by its ID."""
    career = await prisma.career.find_unique(where={"id": career_id})
    if not career:
        raise HTTPException(status_code=404, detail="Career not found")
    return career


# Update a career by ID
@router.put("/{career_id}", response_model=CareerModel)
async def update_career(career_id: str, career_data: CareerUpdate):
    """Update an existing career record."""
    career = await prisma.career.update(
        where={"id": career_id},
        data=career_data.dict(exclude_unset=True),
    )
    if not career:
        raise HTTPException(status_code=404, detail="Career not found")
    return career


# Delete a specific career by ID
@router.delete("/{career_id}")
async def delete_career(career_id: str):
    """Delete a career record by its ID."""
    career = await prisma.career.delete(where={"id": career_id})
    if not career:
        raise HTTPException(status_code=404, detail="Career not found")
    return {"message": f"Career {career_id} deleted successfully."}


# Delete all careers
@router.delete("/")
async def delete_all_careers():
    """Delete all career records."""
    await prisma.career.delete_many()
    return {"message": "All careers deleted successfully."}
