from fastapi import APIRouter, HTTPException
from app.prisma import prisma, connect_prisma, disconnect_prisma
from .schema import BlsImportModel

router = APIRouter(prefix="/v1/bls/imports", tags=["BLS", "Imports", "Version 1"])


# Connect and disconnect prisma
@router.on_event("startup")
async def startup():
    await connect_prisma()


@router.on_event("shutdown")
async def shutdown():
    await disconnect_prisma()


# Get all imports
@router.get("/", response_model=list[BlsImportModel])
async def get_all_imports():
    """Fetch all BLS imports."""
    imports = await prisma.blsimport.find_many()
    return imports


# Get a specific import by ID
@router.get("/{import_id}", response_model=BlsImportModel)
async def get_import(import_id: str):
    """Fetch a specific BLS import by ID."""
    import_record = await prisma.blsimport.find_unique(where={"id": import_id})
    if not import_record:
        raise HTTPException(status_code=404, detail="Import not found")
    return import_record


# Delete a specific import by ID
@router.delete("/{import_id}")
async def delete_import(import_id: str):
    """Delete a BLS import record by ID."""
    import_record = await prisma.blsimport.delete(where={"id": import_id})
    if not import_record:
        raise HTTPException(status_code=404, detail="Import not found")
    return {"message": f"Import {import_id} deleted successfully."}
