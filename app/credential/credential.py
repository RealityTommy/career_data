from fastapi import APIRouter, HTTPException
from app.prisma import prisma, connect_prisma, disconnect_prisma
from .schema import CredentialCreate, CredentialUpdate
from .model import CredentialModel

# Initialize the router with versioned prefix and specified tags
router = APIRouter(prefix="/v1/credentials", tags=["Credentials", "Version 1"])


# Prisma connection and disconnection lifecycle events
@router.on_event("startup")
async def startup():
    await connect_prisma()


@router.on_event("shutdown")
async def shutdown():
    await disconnect_prisma()


# Get all credentials
@router.get("/", response_model=list[CredentialModel])
async def get_all_credentials():
    """Fetch all credential records."""
    credentials = await prisma.credential.find_many()
    return credentials


# Create a new credential
@router.post("/", response_model=CredentialModel)
async def create_credential(credential_data: CredentialCreate):
    """Create a new credential record."""
    credential = await prisma.credential.create(data=credential_data.dict())
    return credential


# Get a specific credential by ID
@router.get("/{credential_id}", response_model=CredentialModel)
async def get_credential(credential_id: str):
    """Fetch a credential by its ID."""
    credential = await prisma.credential.find_unique(where={"id": credential_id})
    if not credential:
        raise HTTPException(status_code=404, detail="Credential not found")
    return credential


# Update a credential by ID
@router.put("/{credential_id}", response_model=CredentialModel)
async def update_credential(credential_id: str, credential_data: CredentialUpdate):
    """Update an existing credential record."""
    credential = await prisma.credential.update(
        where={"id": credential_id},
        data=credential_data.dict(exclude_unset=True),
    )
    if not credential:
        raise HTTPException(status_code=404, detail="Credential not found")
    return credential


# Delete a specific credential by ID
@router.delete("/{credential_id}")
async def delete_credential(credential_id: str):
    """Delete a credential record by its ID."""
    credential = await prisma.credential.delete(where={"id": credential_id})
    if not credential:
        raise HTTPException(status_code=404, detail="Credential not found")
    return {"message": f"Credential {credential_id} deleted successfully."}


# Delete all credentials
@router.delete("/")
async def delete_all_credentials():
    """Delete all credential records."""
    await prisma.credential.delete_many()
    return {"message": "All credentials deleted successfully."}
