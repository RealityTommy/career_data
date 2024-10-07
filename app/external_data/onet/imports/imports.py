from fastapi import APIRouter, HTTPException
from app.prisma import prisma, connect_prisma, disconnect_prisma
from .schema import OnetImportModel

# Initialize the router
router = APIRouter(prefix="/v1/onetimports", tags=["ONET", "Imports", "Version 1"])


# Prisma connection and disconnection lifecycle events
@router.on_event("startup")
async def startup():
    await connect_prisma()


@router.on_event("shutdown")
async def shutdown():
    await disconnect_prisma()


# Endpoint to get all Onet imports
@router.get("/", response_model=list[OnetImportModel])
async def get_all_imports():
    """Fetch all imports from the OnetImport table."""
    imports = await prisma.onetimport.find_many()
    if not imports:
        raise HTTPException(status_code=404, detail="No imports found")
    return imports


# Endpoint to get a specific Onet import by ID
@router.get("/{import_id}", response_model=OnetImportModel)
async def get_import(import_id: str):
    """Fetch a specific import by its ID."""
    onet_import = await prisma.onetimport.find_unique(where={"id": import_id})
    if not onet_import:
        raise HTTPException(status_code=404, detail="Import not found")
    return onet_import


# Endpoint to delete a specific Onet import by ID
@router.delete("/{import_id}")
async def delete_import(import_id: str):
    """Delete a specific Onet import by its ID."""
    import_record = await prisma.onetimport.delete(where={"id": import_id})
    if not import_record:
        raise HTTPException(status_code=404, detail="Import not found")
    return {"message": f"Import {import_id} deleted successfully."}
