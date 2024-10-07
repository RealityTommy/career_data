from fastapi import APIRouter, HTTPException
from app.prisma import prisma, connect_prisma, disconnect_prisma
from .schema import SkillCreate, SkillUpdate
from .model import SkillModel

# Initialize the router with a versioned prefix
router = APIRouter(prefix="/v1/skills", tags=["Skills", "Version 1"])


# Prisma connection and disconnection lifecycle events
@router.on_event("startup")
async def startup():
    await connect_prisma()


@router.on_event("shutdown")
async def shutdown():
    await disconnect_prisma()


# Get all skills
@router.get("/", response_model=list[SkillModel])
async def get_all_skills():
    """Fetch all skill records."""
    skills = await prisma.skill.find_many()
    return skills


# Create a new skill
@router.post("/", response_model=SkillModel)
async def create_skill(skill_data: SkillCreate):
    """Create a new skill record."""
    skill = await prisma.skill.create(data=skill_data.dict())
    return skill


# Get a specific skill by ID
@router.get("/{skill_id}", response_model=SkillModel)
async def get_skill(skill_id: str):
    """Fetch a skill by its ID."""
    skill = await prisma.skill.find_unique(where={"id": skill_id})
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill


# Update a skill by ID
@router.put("/{skill_id}", response_model=SkillModel)
async def update_skill(skill_id: str, skill_data: SkillUpdate):
    """Update an existing skill record."""
    skill = await prisma.skill.update(
        where={"id": skill_id},
        data=skill_data.dict(exclude_unset=True),
    )
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill


# Delete a specific skill by ID
@router.delete("/{skill_id}")
async def delete_skill(skill_id: str):
    """Delete a skill record by its ID."""
    skill = await prisma.skill.delete(where={"id": skill_id})
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return {"message": f"Skill {skill_id} deleted successfully."}


# Delete all skills
@router.delete("/")
async def delete_all_skills():
    """Delete all skill records."""
    await prisma.skill.delete_many()
    return {"message": "All skills deleted successfully."}
